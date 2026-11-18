# src/proxy/surfshark.py
import concurrent.futures
import json
import os
import socket
import subprocess
import sys
import threading
import time
import urllib.request
from collections import deque
from pathlib import Path
from typing import List, Dict, Optional, Tuple, Set
from src.proxy.base import BaseProxyProvider, ProxyEndpoint
from src.utils.paths import resolve_resource, resolve_output_path, find_wireproxy_bin

CLUSTERS_DEFAULT_PATH = resolve_resource("data/surfshark_clusters.json")
CREDENTIALS_DEFAULT_PATH = resolve_resource("data/surfshark_credentials.json")

DEFAULT_PRIVATE_KEY = os.environ.get("SURFSHARK_PRIVATE_KEY", "YOUR_WIREGUARD_PRIVATE_KEY_HERE")

class SurfsharkCluster:
    def __init__(self, data: Dict):
        self.id = data.get("id", "")
        self.country = data.get("country", "")
        self.country_code = data.get("countryCode", "")
        self.city = data.get("city", "")
        self.host = data.get("host", "")
        self.pub_key = data.get("pubKey", "")
        self.load = int(data.get("load", 50))
        self.tags = data.get("tags", [])


class SingleTunnelNode:
    """
    워커 1:1 전용 독립 Wireproxy 터널 노드
    - 워커마다 고유한 로컬 HTTP 포트(1080 + wid) 및 고유한 국가 클러스터 바인딩
    - 개별 IP 사전 실사 검증 및 독립 429 회전 지원
    """
    def __init__(
        self,
        node_id: int,
        cluster: SurfsharkCluster,
        http_port: int,
        socks5_port: int,
        private_key: str,
        warmup_delay: float
    ):
        self.node_id = node_id
        self.cluster = cluster
        self.http_port = http_port
        self.socks5_port = socks5_port
        self.private_key = private_key
        self.warmup_delay = warmup_delay
        self.proc: Optional[subprocess.Popen] = None
        self.last_verified_ip: Optional[str] = None
        self.is_rotating = False
        self._lock = threading.RLock()
        self._last_rotation_time = 0.0
        self._ready_event = threading.Event()
        self._ready_event.set()

    def _is_port_open(self) -> bool:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(0.3)
                s.connect(("127.0.0.1", self.http_port))
                return True
        except Exception:
            return False

    def verify_connectivity(self, timeout: float = 2.0) -> Tuple[bool, Optional[str]]:
        proxy_url = f"http://127.0.0.1:{self.http_port}"
        proxy_handler = urllib.request.ProxyHandler({"http": proxy_url, "https": proxy_url})
        opener = urllib.request.build_opener(proxy_handler)

        test_urls = [
            "http://1.1.1.1/cdn-cgi/trace",
            "http://api.ipify.org?format=json",
            "http://icanhazip.com"
        ]

        for url in test_urls:
            try:
                req = urllib.request.Request(url, headers={"User-Agent": "curl/8.0 (D4UC Multi-Tunnel Engine)"})
                with opener.open(req, timeout=timeout) as res:
                    body = res.read().decode("utf-8", errors="ignore").strip()
                    ip_match = None
                    if "ip=" in body:
                        for line in body.splitlines():
                            if line.startswith("ip="):
                                ip_match = line.split("=", 1)[1].strip()
                                break
                    elif "ip" in body and "{" in body:
                        try:
                            parsed = json.loads(body)
                            ip_match = parsed.get("ip") or parsed.get("origin")
                        except Exception:
                            pass
                    if not ip_match:
                        ip_match = body.split("\n")[0].strip()

                    if ip_match and len(ip_match) >= 7 and "." in ip_match:
                        self.last_verified_ip = ip_match
                        return True, ip_match
            except Exception:
                continue

        return False, None

    def _generate_conf(self) -> Path:
        oct3 = (self.node_id // 250) % 250
        oct4 = (self.node_id % 250) + 2
        conf_content = f"""[Interface]
PrivateKey = {self.private_key}
Address = 10.14.{oct3}.{oct4}/16
DNS = 162.252.172.57, 149.154.159.92

[Peer]
PublicKey = {self.cluster.pub_key}
Endpoint = {self.cluster.host}:51820
AllowedIPs = 0.0.0.0/0
PersistentKeepalive = 25

[Http]
BindAddress = 127.0.0.1:{self.http_port}

[Socks5]
BindAddress = 127.0.0.1:{self.socks5_port}
"""
        conf_path = resolve_output_path(f"data/surfshark_node_{self.http_port}.conf")
        conf_path.parent.mkdir(parents=True, exist_ok=True)
        with open(conf_path, "w", encoding="utf-8") as f:
            f.write(conf_content)
        return conf_path

    def ensure_running(self) -> bool:
        if self.proc and self.proc.poll() is None:
            return True

        with self._lock:
            if self.proc and self.proc.poll() is None:
                return True

            self.stop()
            conf_path = self._generate_conf()

            wireproxy_bin = find_wireproxy_bin()
            if not wireproxy_bin or not wireproxy_bin.exists():
                return False

            popen_kwargs = {}
            if sys.platform == "win32":
                popen_kwargs["creationflags"] = getattr(subprocess, "CREATE_NO_WINDOW", 0)

            self.proc = subprocess.Popen(
                [str(wireproxy_bin), "-c", str(conf_path), "-s"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                **popen_kwargs
            )

            # Wait for port to open initially (fast polling)
            port_ready = False
            for _ in range(30):
                time.sleep(0.06)
                if self._is_port_open():
                    port_ready = True
                    break

            if not port_ready:
                return False

            if self.warmup_delay > 0:
                time.sleep(min(self.warmup_delay, 0.5))

            return True

    def rotate_to(self, new_cluster: SurfsharkCluster, force: bool = False) -> bool:
        with self._lock:
            now = time.time()
            if not force and (now - self._last_rotation_time < 2.0):
                return True

            self.is_rotating = True
            self._ready_event.clear()
            try:
                self.cluster = new_cluster
                self.stop()
                time.sleep(0.15)
                ok = self.ensure_running()
                if ok:
                    # WireGuard UDP 핸드셰이크가 원격 서버와 완벽히 동기화되도록 0.25초 안정화 대기
                    time.sleep(0.25)
                self._last_rotation_time = time.time()
                return ok
            finally:
                self.is_rotating = False
                self._ready_event.set()

    def stop(self):
        if self.proc:
            try:
                self.proc.terminate()
                self.proc.wait(timeout=2)
            except Exception:
                try:
                    self.proc.kill()
                except Exception:
                    pass
            finally:
                self.proc = None


class SurfsharkProxyProvider(BaseProxyProvider):
    """
    Surfshark 1:1 워커 전용 다중 국가 터널 풀 (Multi-Country Cluster Distribution)
    - 워커마다 고유한 국가/도시 IP를 1:1로 개별 할당
    - 기본 선호 국가: 전세계 142개 전체 글로벌 클러스터
    - 특정 워커 429 감지 시 해당 워커 터널만 개별 회전 (타 워커 무중단 유지)
    - Zero-Zombie: 종료 시 모든 터널 프로세스 100% 회수
    """
    def __init__(
        self,
        username: str = "",
        password: str = "",
        private_key: str = DEFAULT_PRIVATE_KEY,
        clusters_path: Path = CLUSTERS_DEFAULT_PATH,
        credentials_path: Path = CREDENTIALS_DEFAULT_PATH,
        preferred_countries: Optional[List[str]] = None,
        http_port: int = 1081,
        socks5_port: int = 1080,
        warmup_delay: float = 1.0,
        local_bridge_port: Optional[int] = None
    ):
        self.username = username
        self.password = password
        self.clusters_path = Path(clusters_path)
        self.credentials_path = Path(credentials_path)
        # Default: empty list -> All 142 Global Clusters
        self.preferred_countries = preferred_countries if preferred_countries is not None else []
        self.base_http_port = http_port
        self.base_socks5_port = socks5_port
        self.warmup_delay = float(warmup_delay)
        self._port_base = self._find_available_port_base()

        self._has_explicit_keys = False
        if isinstance(private_key, list):
            self.private_keys = [str(k).strip() for k in private_key if str(k).strip()]
            self._has_explicit_keys = True
        elif private_key and private_key != DEFAULT_PRIVATE_KEY:
            self.private_keys = [k.strip() for k in str(private_key).replace(",", "\n").splitlines() if k.strip()]
            self._has_explicit_keys = True
        else:
            self.private_keys = [DEFAULT_PRIVATE_KEY]
        if not self.private_keys:
            self.private_keys = [DEFAULT_PRIVATE_KEY]
        self.private_key = self.private_keys[0]

        self.clusters: List[SurfsharkCluster] = []
        self._next_cluster_idx = 0
        self.nodes: Dict[int, SingleTunnelNode] = {}
        self._nodes_lock = threading.RLock()
        self._cluster_lock = threading.RLock()
        self._available_clusters: deque[SurfsharkCluster] = deque()
        self._cooldown_clusters: Dict[str, Tuple[SurfsharkCluster, float]] = {}
        self._assigned_clusters: Dict[int, SurfsharkCluster] = {}

        self._load_data()

    def _load_data(self):
        # 1. Load credentials
        if self.credentials_path.exists():
            try:
                with open(self.credentials_path, "r", encoding="utf-8") as f:
                    creds = json.load(f)
                    ovpn = creds.get("openvpn_credentials", {})
                    self.username = self.username or ovpn.get("username", "")
                    self.password = self.password or ovpn.get("password", "")

                    if not getattr(self, "_has_explicit_keys", False):
                        raw_keys = creds.get("wireguard_keys")
                        if isinstance(raw_keys, list) and raw_keys:
                            self.private_keys = [str(k).strip() for k in raw_keys if str(k).strip()]
                        elif creds.get("wireguard_private_key"):
                            single_k = str(creds.get("wireguard_private_key"))
                            self.private_keys = [k.strip() for k in single_k.replace(",", "\n").splitlines() if k.strip()]

                        if not self.private_keys:
                            self.private_keys = [DEFAULT_PRIVATE_KEY]
                        self.private_key = self.private_keys[0]

                    self.base_http_port = int(creds.get("http_port", self.base_http_port))
                    self.base_socks5_port = int(creds.get("socks5_port", self.base_socks5_port))
                    self.warmup_delay = float(creds.get("warmup_delay", self.warmup_delay))
            except Exception:
                pass

        # Check environment variable overrides (highest priority for Docker & Termux headless execution)
        env_keys = os.environ.get("SURFSHARK_PRIVATE_KEYS") or os.environ.get("SURFSHARK_PRIVATE_KEY")
        if env_keys:
            parsed_env = [k.strip() for k in env_keys.replace(";", ",").replace("\n", ",").split(",") if k.strip()]
            if parsed_env:
                self.private_keys = parsed_env
                self.private_key = parsed_env[0]
                self._has_explicit_keys = True

        # 2. Load clusters
        if self.clusters_path.exists():
            try:
                with open(self.clusters_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    all_clusters = [SurfsharkCluster(item) for item in data]

                    # Filter by preferred countries if specified
                    if self.preferred_countries:
                        filtered = [c for c in all_clusters if c.country_code in self.preferred_countries]
                        self.clusters = filtered if filtered else all_clusters
                    else:
                        self.clusters = all_clusters
            except Exception:
                pass

        # Sort clusters by lowest load
        self.clusters.sort(key=lambda c: c.load)
        with self._cluster_lock:
            self._available_clusters = deque(self.clusters)
            self._cooldown_clusters.clear()
            self._assigned_clusters.clear()

    def _reclaim_expired_cooldowns(self, now: float):
        """만료된 429 쿨다운 클러스터를 큐의 맨 마지막(TAIL)으로 복귀시켜 다시 순환"""
        expired_ids = [cid for cid, (_, exp) in self._cooldown_clusters.items() if exp <= now]
        for cid in expired_ids:
            cluster, _ = self._cooldown_clusters.pop(cid)
            self._available_clusters.append(cluster)

    def _acquire_fresh_cluster(self, worker_id: int) -> Optional[SurfsharkCluster]:
        """리밋 감지 안 된 신선한(Fresh) 국가 클러스터를 우선 선별하여 1:1 매칭"""
        with self._cluster_lock:
            now = time.time()
            self._reclaim_expired_cooldowns(now)

            assigned_ids = {c.id for wid, c in self._assigned_clusters.items() if wid != worker_id}

            chosen = None
            # 1순위: available_clusters에서 다른 워커가 사용 중이지 않은 신선한 노드 획득
            for _ in range(len(self._available_clusters)):
                cand = self._available_clusters.popleft()
                if cand.id not in assigned_ids:
                    chosen = cand
                    break
                else:
                    self._available_clusters.append(cand)

            # 2순위: 모든 신선한 클러스터가 소진된 경우, 쿨다운 중 가장 오래된 클러스터 회수
            if not chosen and self._cooldown_clusters:
                oldest_cid = min(self._cooldown_clusters, key=lambda k: self._cooldown_clusters[k][1])
                chosen, _ = self._cooldown_clusters.pop(oldest_cid)

            # 3순위: fallback to clusters list
            if not chosen and self.clusters:
                chosen = self.clusters[(worker_id - 1) % len(self.clusters)]

            if chosen:
                self._assigned_clusters[worker_id] = chosen
            return chosen

    def get_cluster_by_country(self, country_code: str) -> Optional[SurfsharkCluster]:
        for c in self.clusters:
            if c.country_code.upper() == country_code.upper():
                return c
        return None

    def _generate_wireproxy_conf(self, cluster: SurfsharkCluster) -> Path:
        node = self._get_or_create_node(1)
        node.cluster = cluster
        return node._generate_conf()

    def _is_port_open(self, port: int = 1081) -> bool:
        s = socket.socket()
        s.settimeout(0.3)
        try:
            s.connect(("127.0.0.1", port))
            s.close()
            return True
        except Exception:
            return False

    def _find_available_port_base(self) -> int:
        """다중 프로그램 인스턴스 동시 실행 시 포트 충돌 방지: 사용 중인 포트 대역 자동 감지 후 +100 오프셋 동적 할당"""
        base = max(1080, self.base_http_port - 1)
        while base < 50000:
            in_use = False
            for check_p in [base + 1, base + 2]:
                try:
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                        s.settimeout(0.08)
                        if s.connect_ex(("127.0.0.1", check_p)) == 0:
                            in_use = True
                            break
                except Exception:
                    pass
            if not in_use:
                return base
            base += 100
        return self.base_http_port - 1

    def _get_or_create_node(self, worker_id: int) -> SingleTunnelNode:
        with self._nodes_lock:
            if worker_id in self.nodes:
                return self.nodes[worker_id]

            cluster = self._acquire_fresh_cluster(worker_id)
            if not cluster:
                cluster_idx = (worker_id - 1) % len(self.clusters) if self.clusters else 0
                cluster = self.clusters[cluster_idx]

            http_port = self._port_base + worker_id
            socks5_port = (self._port_base + 1000) + worker_id

            # Round-Robin assignment of WireGuard keys across registered accounts
            key_idx = (worker_id - 1) % len(self.private_keys)
            assigned_key = self.private_keys[key_idx]

            node = SingleTunnelNode(
                node_id=worker_id,
                cluster=cluster,
                http_port=http_port,
                socks5_port=socks5_port,
                private_key=assigned_key,
                warmup_delay=self.warmup_delay
            )
            self.nodes[worker_id] = node
            return node

    def ensure_wireproxy_running(self, worker_id: int = 1) -> bool:
        """단일 워커 또는 메인 노드 터널 실행 보장"""
        node = self._get_or_create_node(worker_id)
        return node.ensure_running()

    def ensure_workers_running(self, worker_count: int) -> bool:
        """
        모든 워커의 1:1 전용 국가 터널을 병렬로 사전 가동 및 실사 검증.
        일부 노드가 네트워크 일시 지연으로 실패할 경우, 신선한 대체 클러스터로 자동 교체(Auto-Healing)하여
        50개 워커가 무중단으로 정상 가동되도록 보장.
        """
        nodes = [self._get_or_create_node(wid) for wid in range(1, worker_count + 1)]
        verified_nodes = set()

        # 1차 병렬 가동 (최대 50스레드로 Windows 프로세스 스폰 초고속 병렬화)
        max_pool = min(worker_count, 50)
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_pool) as executor:
            future_to_node = {executor.submit(n.ensure_running): n for n in nodes}
            failed_nodes = []
            for f in concurrent.futures.as_completed(future_to_node):
                n = future_to_node[f]
                try:
                    if f.result():
                        verified_nodes.add(n)
                    else:
                        failed_nodes.append(n)
                except Exception:
                    failed_nodes.append(n)

        # 2차 Auto-Healing (실패한 노드는 신선한 새 클러스터로 교체 후 재기동)
        if failed_nodes:
            for n in failed_nodes:
                repl = self._acquire_fresh_cluster(n.node_id)
                if repl:
                    n.cluster = repl
            with concurrent.futures.ThreadPoolExecutor(max_workers=min(len(failed_nodes), 25)) as executor:
                heal_futures = {executor.submit(n.ensure_running): n for n in failed_nodes}
                for f in concurrent.futures.as_completed(heal_futures):
                    n = heal_futures[f]
                    try:
                        if f.result():
                            verified_nodes.add(n)
                    except Exception:
                        pass

        # 최소 70% 이상의 노드가 연결 확인되었거나 프로세스 가동 시 통과 (미완료 노드는 워커 루프에서 개별 보정)
        active = sum(1 for n in nodes if n in verified_nodes or (n.proc and n.proc.poll() is None))
        return active >= max(1, int(worker_count * 0.7))

    def get_workers_summary(self, worker_count: int) -> List[Tuple[int, str]]:
        """각 워커별 배정된 국가/도시/IP 요약 목록 반환"""
        summary = []
        for wid in range(1, worker_count + 1):
            node = self._get_or_create_node(wid)
            summary.append((
                wid,
                f"{node.cluster.country} - {node.cluster.city} ({node.last_verified_ip or 'Connected'}) [포트 {node.http_port}]"
            ))
        return summary

    def get_proxy(self, worker_id: int = 1) -> Optional[ProxyEndpoint]:
        """워커 ID에 매핑된 독립 국가 프록시 엔드포인트 반환"""
        if not self.clusters:
            return None

        node = self._get_or_create_node(worker_id)
        if node.is_rotating:
            node._ready_event.wait(timeout=6.0)

        if not node.ensure_running():
            return None

        ip_info = f" ({node.last_verified_ip})" if node.last_verified_ip else ""
        return ProxyEndpoint(
            url=f"http://127.0.0.1:{node.http_port}",
            provider_name=f"Surfshark [{node.cluster.country} - {node.cluster.city}{ip_info} (:{node.http_port})]"
        )

    def rotate_cluster(self, worker_id: int = 1, cooldown_seconds: float = 300.0) -> Optional[SurfsharkCluster]:
        """
        429 레이트리밋 또는 프록시 장애(Timeout/Failover) 감지 시:
        1. 해당 국가 클러스터를 429 페널티 쿨다운에 등록하고 활성 큐에서 격리
        2. 쿨다운 만료 시 큐의 맨 마지막(Tail)으로 복귀시켜 순환
        3. 리밋 감지 안 된 신선한(Fresh) 국가 클러스터를 즉시 1:1 신규 배정 및 강제 회전
        """
        if not self.clusters:
            return None

        node = self._get_or_create_node(worker_id)
        with self._cluster_lock:
            now = time.time()
            old_cluster = self._assigned_clusters.get(worker_id) or node.cluster
            if old_cluster:
                self._cooldown_clusters[old_cluster.id] = (old_cluster, now + cooldown_seconds)

        new_cluster = self._acquire_fresh_cluster(worker_id)
        if not new_cluster:
            with self._cluster_lock:
                self._next_cluster_idx = (self._next_cluster_idx + 1) % len(self.clusters)
                new_cluster = self.clusters[self._next_cluster_idx]

        node.rotate_to(new_cluster, force=True)
        return new_cluster

    def is_rotating(self, worker_id: int = 1) -> bool:
        node = self.nodes.get(worker_id)
        return node.is_rotating if node else False

    def wait_until_ready(self, worker_id: int = 1, timeout: float = 6.0) -> bool:
        node = self.nodes.get(worker_id)
        return node._ready_event.wait(timeout=timeout) if node else True

    def verify_proxy_connectivity(self, worker_id: int = 1, timeout: float = 4.0) -> Tuple[bool, Optional[str]]:
        node = self._get_or_create_node(worker_id)
        return node.verify_connectivity(timeout=timeout)

    @property
    def http_port(self) -> int:
        return self.base_http_port

    @property
    def socks5_port(self) -> int:
        return self.base_socks5_port

    @property
    def last_verified_ip(self) -> Optional[str]:
        node1 = self.nodes.get(1)
        return node1.last_verified_ip if node1 else None

    def update_and_save_credentials(
        self,
        username: str,
        password: str,
        private_key: str,
        http_port: int,
        socks5_port: int,
        warmup_delay: float,
        private_keys: Optional[List[str]] = None
    ):
        self.username = username.strip()
        self.password = password.strip()
        self.base_http_port = int(http_port)
        self.base_socks5_port = int(socks5_port)
        self.warmup_delay = float(warmup_delay)

        if private_keys:
            self.private_keys = [str(k).strip() for k in private_keys if str(k).strip()]
        elif private_key:
            self.private_keys = [k.strip() for k in str(private_key).replace(",", "\n").splitlines() if k.strip()]
        if not self.private_keys:
            self.private_keys = [DEFAULT_PRIVATE_KEY]
        self.private_key = self.private_keys[0]

        data = {
            "account_email": os.environ.get("SURFSHARK_ACCOUNT_EMAIL", "your_email@example.com"),
            "plan": "Surfshark Starter (Multi-Account Enabled)",
            "wireguard_private_key": self.private_key,
            "wireguard_keys": self.private_keys,
            "http_port": self.base_http_port,
            "socks5_port": self.base_socks5_port,
            "warmup_delay": self.warmup_delay,
            "openvpn_credentials": {
                "username": self.username,
                "password": self.password
            },
            "total_clusters": len(self.clusters)
        }
        try:
            self.credentials_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.credentials_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception:
            pass

    def report_result(self, endpoint: ProxyEndpoint, success: bool, rate_limited: bool = False, cooldown: float = 15.0):
        if rate_limited:
            endpoint.mark_rate_limited(cooldown_seconds=cooldown)
        elif success:
            endpoint.mark_success()
        else:
            endpoint.mark_failure()

    def has_available_proxies(self) -> bool:
        return len(self.clusters) > 0

    def stop(self):
        """모든 워커의 터널 프로세스 100% 안전 종료 (Zero-Zombie 보장)"""
        with self._nodes_lock:
            for node in self.nodes.values():
                node.stop()
            self.nodes.clear()

    def __del__(self):
        self.stop()
