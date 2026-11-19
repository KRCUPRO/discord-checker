# deploy/scripts/generate_all_locales_suite.py
"""
D4UC Master 12-Locale 1:1 Complete Documentation Suite Generator.
Generates 96 fully localized, bidirectional-navigated documents in docs/locales/<lang>/
and synchronizes all master files with the standardized 5x2 language selector table.
"""
import sys
import shutil
from pathlib import Path

# Add current directory to path
script_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(script_dir))

from locale_data.common import LOCALES, LOCALE_MAP, generate_language_table
from locale_data.security import SECURITY_DATA
from locale_data.notice import NOTICE_DATA
from locale_data.license import OFFICIAL_LICENSE_TEXT, LICENSE_DATA
from locale_data.tasks import TASKS_DATA
from locale_data.changelog import CHANGELOG_DATA
from locale_data.architecture import ARCHITECTURE_DATA
from locale_data.guide import GUIDE_DATA
from locale_data.hub_readme import HUB_README_DATA

REPO_ROOT = script_dir.parent.parent


def sync_badges():
    """Ensure all badge alias files exist in docs/assets/badges/"""
    badge_dir = REPO_ROOT / "docs/assets/badges"
    badge_dir.mkdir(parents=True, exist_ok=True)
    
    aliases = [
        ("update_badge.svg", "update_badge_ko.svg"),
        ("update_badge_pt.svg", "update_badge_pt-BR.svg"),
        ("update_badge_zh.svg", "update_badge_zh-CN.svg"),
    ]
    for src_name, dst_name in aliases:
        src = badge_dir / src_name
        dst = badge_dir / dst_name
        if src.exists() and not dst.exists():
            shutil.copy2(src, dst)
            print(f"Created badge alias: {dst.name}")


def generate_security_doc(loc_code: str) -> str:
    loc = LOCALE_MAP[loc_code]
    data = SECURITY_DATA[loc_code]
    lang_table = generate_language_table("SECURITY.md", loc_code, "locale_subdir")
    badge_path = f"../../assets/badges/{loc['badge']}"

    toc_items = []
    sections_rendered = []
    for s in data["sections"]:
        toc_items.append(f"1. [{s['title']}](#{s['id']})")
        sec_block = (
            f'<a id="{s["id"]}"></a>\n'
            f'## {s["title"]}\n\n'
            f'{s["content"]}\n\n'
            f'{loc["return_top"]}\n'
        )
        sections_rendered.append(sec_block)

    toc_rendered = "\n".join(toc_items)
    body_rendered = "\n---\n\n".join(sections_rendered)

    doc = f"""<div align="center">

# {data["title"]}

> **{data["desc"]}**

<br />

{lang_table}

<br />

[![Last Updated: {loc["date_str"]}]({badge_path})](./CHANGELOG.md)
[![Security Policy: Active](https://img.shields.io/badge/Security-Policy%20Active-brightgreen.svg)](https://github.com/KRCUPRO/discord-checker/security)

</div>

---

<a id="{loc["toc_anchor"]}"></a>
## 📑 {loc["toc_title"]}
{toc_rendered}

---

{body_rendered}
"""
    return doc


def generate_notice_doc(loc_code: str) -> str:
    loc = LOCALE_MAP[loc_code]
    data = NOTICE_DATA[loc_code]
    lang_table = generate_language_table("NOTICE.md", loc_code, "locale_subdir")
    badge_path = f"../../assets/badges/{loc['badge']}"

    toc_items = []
    sections_rendered = []
    for p in data["packages"]:
        toc_items.append(f"1. [{p['name']} ({p['license']})](#{p['id']})")
        sec_block = (
            f'<a id="{p["id"]}"></a>\n'
            f'## {p["name"]}\n'
            f'> **License**: `{p["license"]}`\n\n'
            f'{p["desc"]}\n\n'
            f'{loc["return_top"]}\n'
        )
        sections_rendered.append(sec_block)

    toc_rendered = "\n".join(toc_items)
    body_rendered = "\n---\n\n".join(sections_rendered)

    doc = f"""<div align="center">

# {data["title"]}

> **{data["desc"]}**

<br />

{lang_table}

<br />

[![Last Updated: {loc["date_str"]}]({badge_path})](./CHANGELOG.md)
[![Third-Party Notices: Verified](https://img.shields.io/badge/Notices-Verified-blue.svg)](./NOTICE.md)

</div>

---

<a id="{loc["toc_anchor"]}"></a>
## 📑 {loc["toc_title"]}
{toc_rendered}

---

> {data["intro"]}

---

{body_rendered}
"""
    return doc


def generate_license_doc(loc_code: str) -> str:
    loc = LOCALE_MAP[loc_code]
    data = LICENSE_DATA[loc_code]
    lang_table = generate_language_table("LICENSE.md", loc_code, "locale_subdir")
    badge_path = f"../../assets/badges/{loc['badge']}"

    toc_items = [
        f"1. [{data['official_label']}](#-official-legal-text)",
        f"2. [{data['summary_title']}](#-legal-summary)"
    ]

    clauses_rendered = []
    for c_title, c_desc in data["clauses"]:
        clauses_rendered.append(f"### {c_title}\n{c_desc}\n")

    summary_block = "\n".join(clauses_rendered)

    doc = f"""<div align="center">

# {data["title"]}

> **{data["desc"]}**

<br />

{lang_table}

<br />

[![Last Updated: {loc["date_str"]}]({badge_path})](./CHANGELOG.md)
[![License: Proprietary](https://img.shields.io/badge/License-Proprietary-red.svg)](./LICENSE.md)

</div>

---

<a id="{loc["toc_anchor"]}"></a>
## 📑 {loc["toc_title"]}
{toc_items[0]}
{toc_items[1]}

---

<a id="-official-legal-text"></a>
## 📜 {data["official_label"]}

```text
{OFFICIAL_LICENSE_TEXT}
```

{loc["return_top"]}

---

<a id="-legal-summary"></a>
## ⚖️ {data["summary_title"]}

{summary_block}
{loc["return_top"]}
"""
    return doc


def generate_tasks_doc(loc_code: str) -> str:
    loc = LOCALE_MAP[loc_code]
    data = TASKS_DATA[loc_code]
    lang_table = generate_language_table("TASKS.md", loc_code, "locale_subdir")
    badge_path = f"../../assets/badges/{loc['badge']}"

    toc_items = [
        f"1. [{data['sec1_title']}](#{data['sec1_id']})",
        f"2. [{data['sec2_title']}](#{data['sec2_id']})",
        f"3. [{data['sec3_title']}](#{data['sec3_id']})",
    ]

    ms_rows = []
    for ver, title, desc, status in data["milestones"]:
        ms_rows.append(f"| **{ver}** | {title} | {desc} | {status} |")
    ms_table = data["milestones_header"] + "\n" + "\n".join(ms_rows)

    sec2_content = "\n".join([f"- {it}" for it in data["sec2_items"]])
    sec3_content = "\n".join([f"- {it}" for it in data["sec3_items"]])

    doc = f"""<div align="center">

# {data["title"]}

> **{data["desc"]}**

<br />

{lang_table}

<br />

[![Last Updated: {loc["date_str"]}]({badge_path})](./CHANGELOG.md)
[![Status: Production Stable](https://img.shields.io/badge/Status-Production%20Stable-brightgreen.svg)](./TASKS.md)

</div>

---

<a id="{loc["toc_anchor"]}"></a>
## 📑 {loc["toc_title"]}
{chr(10).join(toc_items)}

---

<a id="{data['sec1_id']}"></a>
## 🎯 {data["sec1_title"]}

{ms_table}

{loc["return_top"]}

---

<a id="{data['sec2_id']}"></a>
## 📦 {data["sec2_title"]}

{sec2_content}

{loc["return_top"]}

---

<a id="{data['sec3_id']}"></a>
## 🛡️ {data["sec3_title"]}

{sec3_content}

{loc["return_top"]}
"""
    return doc


def generate_changelog_doc(loc_code: str) -> str:
    loc = LOCALE_MAP[loc_code]
    data = CHANGELOG_DATA[loc_code]
    lang_table = generate_language_table("CHANGELOG.md", loc_code, "locale_subdir")
    badge_path = f"../../assets/badges/{loc['badge']}"

    toc_items = []
    versions_rendered = []
    for v in data["versions"]:
        slug = f"-{v['ver'].replace('.', '')}-{v['date']}"
        toc_items.append(f"1. [[{v['ver']}] — {v['date']}](#{slug})")
        
        v_lines = [
            f'<a id="{slug}"></a>',
            f'## [{v["ver"]}] — {v["date"]}\n',
            "### Added"
        ]
        for a in v["added"]:
            v_lines.append(f"- {a}")
        
        if "changed" in v and v["changed"]:
            v_lines.append("\n### Changed")
            for c in v["changed"]:
                v_lines.append(f"- {c}")
        
        v_lines.append(f"\n{loc['return_top']}\n")
        versions_rendered.append("\n".join(v_lines))

    toc_rendered = "\n".join(toc_items)
    body_rendered = "\n---\n\n".join(versions_rendered)

    doc = f"""<div align="center">

# {data["title"]}

> **{data["desc"]}**

<br />

{lang_table}

<br />

[![Last Updated: {loc["date_str"]}]({badge_path})](./CHANGELOG.md)
[![Latest Release](https://img.shields.io/badge/Release-v12.5.0-blue.svg)](https://github.com/KRCUPRO/discord-checker/releases)

</div>

---

<a id="{loc["toc_anchor"]}"></a>
## 📑 {loc["toc_title"]}
{toc_rendered}

---

> {data["intro"]}

---

{body_rendered}
"""
    return doc


def generate_architecture_doc(loc_code: str) -> str:
    loc = LOCALE_MAP[loc_code]
    data = ARCHITECTURE_DATA[loc_code]
    lang_table = generate_language_table("ARCHITECTURE_MAP.md", loc_code, "locale_subdir")
    badge_path = f"../../assets/badges/{loc['badge']}"

    toc_items = [
        f"1. [{data['sec1_title']}](#{data['sec1_id']})",
        f"2. [{data['sec2_title']}](#{data['sec2_id']})",
        f"3. [{data['sec3_title']}](#{data['sec3_id']})",
        f"4. [{data['sec4_title']}](#{data['sec4_id']})",
        f"5. [{data['sec5_title']}](#{data['sec5_id']})"
    ]

    principles_rendered = "\n".join([f"- {p}" for p in data["principles"]])

    layers_rendered = []
    for l_name, l_desc in data["layers"]:
        layers_rendered.append(f"### {l_name}\n{l_desc}\n")
    layers_block = "\n".join(layers_rendered)

    doc = f"""<div align="center">

# {data["title"]}

> **{data["desc"]}**

<br />

{lang_table}

<br />

[![Last Updated: {loc["date_str"]}]({badge_path})](./CHANGELOG.md)
[![Architecture: Lossless Multi-Tier](https://img.shields.io/badge/Architecture-Lossless%20Multi--Tier-purple.svg)](./ARCHITECTURE_MAP.md)

</div>

---

<a id="{loc["toc_anchor"]}"></a>
## 📑 {loc["toc_title"]}
{chr(10).join(toc_items)}

---

## 💎 {data["principles_title"]}
{principles_rendered}

---

<a id="{data['sec1_id']}"></a>
## 🏛️ {data["sec1_title"]}

```mermaid
graph TD
    subgraph Layer 1: Presentation ["1. Presentation Layer (UI / CLI)"]
        GUI_KO["src/gui_ko.py (Korean GUI)"]
        GUI_EN["src/gui_en.py (English GUI)"]
        GUI_WEB["src/web_gui.py (Mobile Touch Web GUI / PWA)"]
        CLI["src/run.py (Headless CLI + Rich Dashboard)"]
    end

    subgraph Layer 2: Orchestration ["2. Orchestration & Worker Loop"]
        ORCH["Orchestrator / Async Worker Loop"]
        METRICS["DashboardMetrics (RPS, Available, Taken, 429)"]
        SHARD["Sharding Coordinator (2_1, 2_2, 3_1...)"]
    end

    subgraph Layer 3: Network & Stealth ["3. Network & TLS Stealth"]
        CLIENT["DiscordApiClient (curl_cffi AsyncSession)"]
        TLS["Chrome 131 TLS JA3/JA4 Fingerprint"]
        HEADERS["Browser Headers (sec-ch-ua, Referer, Accept)"]
    end

    subgraph Layer 4: Proxy Infrastructure ["4. Proxy Infrastructure & Multi-Tunnel"]
        UPM["UnifiedProxyManager"]
        SURF["SurfsharkProxyProvider (1:1 Multi-Tunnel)"]
        FREE["FreeProxyProvider (18 Open-Source Pools)"]
        WIRE["Wireproxy Process Daemon (User-Space Netstack)"]
        COOLDOWN["429 Cooldown Queue & 0.3s Atomic Hot-Swap Engine"]
    end

    subgraph Layer 5: Candidate Generator ["5. Candidate Username Generator Engine"]
        GEN_FACT["create_generator() Factory"]
        HYBRID["HybridGenerator"]
        PERM["PermutationGenerator (Sharded Math Engine)"]
        DICT["DictionaryGenerator"]
        MASK["CustomMaskGenerator"]
        OTHER_GEN["Pattern / Numeric / Combinatorial / Recheck"]
    end

    subgraph Layer 6: Storage & Notify ["6. Persistent Storage & Notifications"]
        STORAGE["StorageManager (Async Queue Worker)"]
        SQLITE["SQLite WAL (d4uc_results.db, busy_timeout=5s)"]
        MIRROR["Legacy Mirror (available.txt, taken.txt)"]
        WEBHOOK["DiscordWebhookNotifier (0.1s Dispatch)"]
    end

    GUI_KO & GUI_EN & GUI_WEB & CLI --> ORCH
    ORCH --> GEN_FACT
    GEN_FACT --> HYBRID & PERM & DICT & MASK & OTHER_GEN
    ORCH --> CLIENT
    CLIENT --> TLS & HEADERS
    ORCH --> UPM
    UPM --> SURF & FREE & WIRE & COOLDOWN
    ORCH --> STORAGE
    STORAGE --> SQLITE & MIRROR & WEBHOOK
```

{layers_block}

{loc["return_top"]}

---

<a id="{data['sec2_id']}"></a>
## 🔄 {data["sec2_title"]}

```text
[Candidate Generator] ──(Next Batch)──> [Orchestrator Worker Pool]
                                                    │
                                            (Lease Isolated SOCKS5)
                                                    ▼
                                        [Unified Proxy Manager]
                                                    │
                                          (Chrome 131 TLS Impersonation)
                                                    ▼
                                        [Discord API Endpoint]
                                                    │
                                         (Response Dispatch)
                        ┌───────────────────────────┴───────────────────────────┐
                        ▼                                                       ▼
               HTTP 200 / Taken                                         HTTP 429 Rate Limit
                        │                                                       │
        ┌───────────────┴───────────────┐                             (0.3s Atomic Hot-Swap)
        ▼                               ▼                                       ▼
 [SQLite WAL Storage]       [Discord Webhook Push]                  [Rotate to Fresh Country]
```

{loc["return_top"]}

---

<a id="{data['sec3_id']}"></a>
## ⚡ {data["sec3_title"]}

- **Non-blocking Concurrency**: All network I/O operations are scheduled on Python's native `asyncio` event loop.
- **429 Atomic Hot-Swap**: When an isolated worker hits Discord's 429 rate limit, its specific Wireproxy local port is seamlessly reassigned to an available server node in under 0.3s without affecting concurrent workers.
- **Zero Lock Deadlock**: SQLite WAL journal mode coupled with Python-level queueing completely eliminates `database is locked` operational exceptions.

{loc["return_top"]}

---

<a id="{data['sec4_id']}"></a>
## 💾 {data["sec4_title"]}

- **Primary Database**: `data/d4uc_results.db` configured with `PRAGMA journal_mode = WAL` and `PRAGMA synchronous = NORMAL`.
- **Text File Mirroring**: For maximum legacy compatibility, all newly verified rare handles are concurrently appended to `available.txt` and `checked_history.txt`.

{loc["return_top"]}

---

<a id="{data['sec5_id']}"></a>
## 🛡️ {data["sec5_title"]}

- **Zero-Leak Policy**: All local credentials, WireGuard configuration files, and secrets are strictly excluded from version control.
- **User-Space Network Isolation**: All proxy traffic is terminated in user space (`wireproxy`), preventing interference with system-wide DNS or routing tables.

{loc["return_top"]}
"""
    return doc


def generate_guide_doc(loc_code: str) -> str:
    loc = LOCALE_MAP[loc_code]
    data = GUIDE_DATA[loc_code]
    lang_table = generate_language_table("GUIDE.md", loc_code, "locale_subdir")
    badge_path = f"../../assets/badges/{loc['badge']}"

    toc_items = [
        f"1. [{data['sec1_title']}](#{data['sec1_id']})",
        f"2. [{data['sec2_title']}](#{data['sec2_id']})",
        f"3. [{data['sec3_title']}](#{data['sec3_id']})",
        f"4. [{data['sec4_title']}](#{data['sec4_id']})",
        f"5. [{data['sec5_title']}](#{data['sec5_id']})",
        f"6. [{data['sec6_title']}](#{data['sec6_id']})",
        f"7. [{data['sec7_title']}](#{data['sec7_id']})",
        f"8. [{data['sec8_title']}](#{data['sec8_id']})",
        f"9. [{data['sec9_title']}](#{data['sec9_id']})"
    ]

    doc = f"""<div align="center">

# {data["title"]}

> **{data["desc"]}**

<br />

{lang_table}

<br />

[![Last Updated: {loc["date_str"]}]({badge_path})](./CHANGELOG.md)
[![Guide Version](https://img.shields.io/badge/Guide-v12.5.0-blue.svg)](./GUIDE.md)

</div>

---

<a id="{loc["toc_anchor"]}"></a>
## 📑 {loc["toc_title"]}
{chr(10).join(toc_items)}

---

<a id="{data['sec1_id']}"></a>
## 1. {data["sec1_title"]}

- **Engine Target Endpoint**: `https://discord.com/api/v9/unique-username/username-attempt-unauthed`
- **Core Technological Invariants**:
  1. <a id="fnref-1"></a><a id="fnref1"></a>**Chrome 131 TLS JA3/JA4 Stealth Impersonation** (`curl_cffi`)[^1].
  2. <a id="fnref-2"></a><a id="fnref2"></a>**Surfshark 1:1 Isolated Multi-Tunnel Pool** (`wireproxy`)[^2].
  3. **0.3s Atomic 429 Hot-Swap**: Uninterrupted continuous scanning across alternate global countries.
  4. **Free Public Proxy Scraper & Live Multi-Threaded Validator** (`src/proxy/free_proxy.py`).
  5. **SQLite WAL Concurrency**: Multi-process safe state synchronization without database locks.

{loc["return_top"]}

---

<a id="{data['sec2_id']}"></a>
## 2. {data["sec2_title"]}

- 🪟 [Windows Guide (WINDOWS_GUIDE.md)](../../guides/WINDOWS_GUIDE.md): 4 Standalone EXEs, Windows Firewall, Task Scheduler 24/7.
- 🍏 [macOS Guide (MACOS_GUIDE.md)](../../guides/MACOS_GUIDE.md): Apple Silicon M1-M4 & Intel, Homebrew, `launchd` automation.
- 🐧 [Linux Guide (LINUX_GUIDE.md)](../../guides/LINUX_GUIDE.md): Ubuntu, Debian, systemd service, tmux/screen background execution.
- 🤖 [Android Guide (ANDROID_GUIDE.md)](../../guides/ANDROID_GUIDE.md): 1-Tap native APK, Wake Lock management, Termux PRoot.
- 📱 [iOS Guide (IOS_GUIDE.md)](../../guides/IOS_GUIDE.md): Safari PWA Home Screen App, 0.1s Discord Webhook push notifications.
- 🐳 [Docker Guide (DOCKER_GUIDE.md)](../../guides/DOCKER_GUIDE.md): Multi-Arch Docker Compose 2-shard acceleration.
- 🍓 [Raspberry Pi Guide (RASPBERRY_PI_GUIDE.md)](../../guides/RASPBERRY_PI_GUIDE.md): 3W low-power homelab 24/7 setup.
- 🧭 [Guides Hub (docs/guides/README.md)](../../guides/README.md) & [Docs Hub (docs/README.md)](../../README.md)

{loc["return_top"]}

---

<a id="{data['sec3_id']}"></a>
## 3. {data["sec3_title"]}

### A. Desktop GUI (Windows & macOS)
```bash
python src/gui_ko.py   # Korean GUI
python src/gui_en.py   # English GUI
```

### B. Mobile Touch Web GUI & PWA
```bash
python src/web_gui.py --port 5000
# Open http://<LOCAL_IP>:5000 on mobile browser or tap 'Add to Home Screen'
```

### C. Android 1-Tap Standalone APK
- Install `dist/DiscordUsernameChecker_v12.3.0.apk` directly on Android 8.0+.

### D. Headless Rich CLI (Linux / Server)
```bash
python src/run.py --mode hybrid --length 4 --workers 10 --proxy free
```

### E. Multi-Arch Docker Compose
```bash
docker compose -f deploy/docker-compose.yml up -d
```

{loc["return_top"]}

---

<a id="{data['sec4_id']}"></a>
## 4. {data["sec4_title"]}

1. **Hybrid**: Combines dictionary bases, consonant-vowel combinations, and alphanumeric affixes.
2. **Permutation**: Pure combinatorial math engine (`[a-z0-9_.]^N`).
3. **Dictionary**: Real word frequency dictionary matching.
4. **Pattern**: Custom regex pattern matching (`a*b?`, `kr_*`).
5. **Numeric**: Consecutive and rare numerical combinations (`0001`~`9999`).
6. **Custom Mask**: Precise position-by-position character masking.
7. **Combinatorial**: User-defined prefix + base + suffix combinations.
8. **Recheck**: Scans previously verified or taken database history.

{loc["return_top"]}

---

<a id="{data['sec5_id']}"></a>
## 5. {data["sec5_title"]}

- **Surfshark WireGuard Multi-Tunnel**: Maps 142 global server clusters to local ports `127.0.0.1:1081~1085`.
- **Free Public Proxy Scraper**: Aggregates from 18 verified open-source endpoints with Cloudflare trace pre-validation.
- **Tor & User Proxies**: SOCKS5 and HTTP proxy list rotation support.

{loc["return_top"]}

---

<a id="{data['sec6_id']}"></a>
## 6. {data["sec6_title"]}

Execute 2 to 4 parallel sharded instances with zero key collisions:
```bash
# Window 1 (Shard 1/2)
python src/run.py --mode permutation --shard 2_1 --length 4

# Window 2 (Shard 2/2)
python src/run.py --mode permutation --shard 2_2 --length 4
```

{loc["return_top"]}

---

<a id="{data['sec7_id']}"></a>
## 7. {data["sec7_title"]}

- Never commit `config.yaml`, `.env`, or `surfshark_credentials.json`.
- All credentials must be passed via environment variables or template files.
- Refer to [SECURITY.md](./SECURITY.md) for vulnerability reporting.

{loc["return_top"]}

---

<a id="{data['sec8_id']}"></a>
## 8. {data["sec8_title"]}

```text
src/
├── network/    # DiscordApiClient & Chrome 131 TLS handshake
├── proxy/      # UnifiedProxyManager, Surfshark, FreeProxyProvider
├── generator/  # 8 candidate generation algorithms
├── storage/    # SQLite WAL database & text mirrors
└── ui/         # Desktop CustomTkinter & Mobile Web GUI
```

{loc["return_top"]}

---

<a id="{data['sec9_id']}"></a>
## 9. {data["sec9_title"]}

[^1]: <a id="fn-1"></a><a id="fn1"></a>{data["fn1"]} [↩️ {loc["return_ref"]}](#fnref-1)
[^2]: <a id="fn-2"></a><a id="fn2"></a>{data["fn2"]} [↩️ {loc["return_ref"]}](#fnref-2)

{loc["return_top"]}
"""
    return doc


def generate_hub_readme_doc(loc_code: str) -> str:
    loc = LOCALE_MAP[loc_code]
    data = HUB_README_DATA[loc_code]
    lang_table = generate_language_table("README.md", loc_code, "locale_subdir")
    badge_path = f"../../assets/badges/{loc['badge']}"

    toc_items = [
        f"1. [{data['sec1_title']}](#{data['sec1_id']})",
        f"2. [{data['sec2_title']}](#{data['sec2_id']})",
        f"3. [{data['sec3_title']}](#{data['sec3_id']})",
        f"4. [{data['sec4_title']}](#{data['sec4_id']})",
        f"5. [{data['sec5_title']}](#{data['sec5_id']})",
        f"6. [{data['sec6_title']}](#{data['sec6_id']})"
    ]

    doc = f"""<div align="center">

# {data["title"]}

> **{data["desc"]}**

<br />

{lang_table}

<br />

[![Last Updated: {loc["date_str"]}]({badge_path})](./CHANGELOG.md)
[![Docs Hub](https://img.shields.io/badge/Docs-Hub%20Active-brightgreen.svg)](./README.md)

</div>

---

<a id="{loc["toc_anchor"]}"></a>
## 📑 {loc["toc_title"]}
{chr(10).join(toc_items)}

---

<a id="{data['sec1_id']}"></a>
## 📂 {data["sec1_title"]}

```text
docs/
├── README.md                  # Central Documentation Hub Index
├── GUIDE.md                   # D4UC Master Project Guide
├── ARCHITECTURE_MAP.md        # Full Architecture Map & Flowcharts
├── TASKS.md                   # Task Backlog & Milestone History
├── guides/                    # 13 Dedicated OS & Platform Manuals
│   ├── WINDOWS_GUIDE.md       # Windows 10/11 & Standalone EXEs
│   ├── MACOS_GUIDE.md         # Apple Silicon & Homebrew
│   ├── LINUX_GUIDE.md         # Ubuntu/Debian systemd Daemon
│   ├── ANDROID_GUIDE.md       # 1-Tap Standalone APK
│   ├── IOS_GUIDE.md           # Safari PWA Full-Screen App
│   ├── DOCKER_GUIDE.md        # Multi-Arch Docker Compose
│   └── RASPBERRY_PI_GUIDE.md  # 3W Low-Power Homelab
├── specs/                     # Core Engine Technical Specs
└── locales/                   # 12-Language 1:1 Complete Translations
```

{loc["return_top"]}

---

<a id="{data['sec2_id']}"></a>
## 🖥️ {data["sec2_title"]}

- 🪟 [Windows (WINDOWS_GUIDE.md)](../../guides/WINDOWS_GUIDE.md)
- 🍏 [macOS (MACOS_GUIDE.md)](../../guides/MACOS_GUIDE.md)
- 🐧 [Linux (LINUX_GUIDE.md)](../../guides/LINUX_GUIDE.md)
- 🤖 [Android (ANDROID_GUIDE.md)](../../guides/ANDROID_GUIDE.md)
- 📱 [iOS (IOS_GUIDE.md)](../../guides/IOS_GUIDE.md)
- 🐳 [Docker (DOCKER_GUIDE.md)](../../guides/DOCKER_GUIDE.md)
- 🍓 [Raspberry Pi (RASPBERRY_PI_GUIDE.md)](../../guides/RASPBERRY_PI_GUIDE.md)

{loc["return_top"]}

---

<a id="{data['sec3_id']}"></a>
## 🌐 {data["sec3_title"]}

- 🇰🇷 [한국어 (ko)](../ko/README.md) • 🇺🇸 [US English (en)](../en/README.md) • 🇯🇵 [日本語 (ja)](../ja/README.md)
- 🇨🇳 [简体中文 (zh-CN)](../zh-CN/README.md) • 🇪🇸 [Español (es)](../es/README.md) • 🇫🇷 [Français (fr)](../fr/README.md)
- 🇩🇪 [Deutsch (de)](../de/README.md) • 🇷🇺 [Русский (ru)](../ru/README.md) • 🇧🇷 [Português (pt-BR)](../pt-BR/README.md)
- 🇸🇦 [العربية (ar)](../ar/README.md) • 🇮🇳 [हिन्दी (hi)](../hi/README.md) • 🇮🇩 [Bahasa Indonesia (id)](../id/README.md)

{loc["return_top"]}

---

<a id="{data['sec4_id']}"></a>
## ⚙️ {data["sec4_title"]}

1. [01 Network Core Engine](../../specs/01_NETWORK_CORE_ENGINE.md)
2. [02 Proxy Infrastructure](../../specs/02_PROXY_INFRASTRUCTURE.md)
3. [03 Nickname Generation Algorithms](../../specs/03_NICKNAME_GENERATION_ALGORITHMS.md)
4. [04 Monitoring, Storage & Webhook](../../specs/04_MONITORING_STORAGE_WEBHOOK.md)
5. [05 Surfshark Integration](../../specs/05_SURFSHARK_INTEGRATION.md)

{loc["return_top"]}

---

<a id="{data['sec5_id']}"></a>
## 📋 {data["sec5_title"]}

- [CHANGELOG.md](./CHANGELOG.md) — Release notes and changelog history
- [TASKS.md](./TASKS.md) — Development task index and milestones
- [LICENSE.md](./LICENSE.md) — Proprietary software license
- [NOTICE.md](./NOTICE.md) — Third-party open-source attributions
- [SECURITY.md](./SECURITY.md) — Security policy and vulnerability disclosure

{loc["return_top"]}

---

<a id="{data['sec6_id']}"></a>
## 📝 {data["sec6_title"]}

<a id="fn-1"></a><a id="fn1"></a>[^1]: {data["fn1"]}

{loc["return_top"]}
"""
    return doc


def generate_main_readme_in_locale(loc_code: str) -> str:
    """Generate docs/locales/<lang>/README.md using existing flat file docs/locales/<lang>.md or root README.md"""
    if loc_code == "en":
        src_path = REPO_ROOT / "README.md"
    else:
        src_path = REPO_ROOT / f"docs/locales/{loc_code}.md"

    if not src_path.exists():
        print(f"Warning: source path {src_path} does not exist.")
        return ""

    content = src_path.read_text(encoding="utf-8")

    # Use placeholder to prevent double-replacement of assets, guides, and specs
    # Target from docs/locales/<lang>/README.md:
    # docs/assets/ -> ../../assets/
    # docs/guides/ -> ../../guides/
    # docs/specs/  -> ../../specs/
    for prefix in ["docs/assets/", "../assets/"]:
        content = content.replace(prefix, "___PLACEHOLDER_ASSETS___")
    for prefix in ["docs/guides/", "../guides/"]:
        content = content.replace(prefix, "___PLACEHOLDER_GUIDES___")
    for prefix in ["docs/specs/", "../specs/"]:
        content = content.replace(prefix, "___PLACEHOLDER_SPECS___")

    content = content.replace("___PLACEHOLDER_ASSETS___", "../../assets/")
    content = content.replace("___PLACEHOLDER_GUIDES___", "../../guides/")
    content = content.replace("___PLACEHOLDER_SPECS___", "../../specs/")
    
    # Root files: CHANGELOG.md, LICENSE, NOTICE, SECURITY.md
    content = content.replace("](CHANGELOG.md)", "](./CHANGELOG.md)")
    content = content.replace("](../../CHANGELOG.md)", "](./CHANGELOG.md)")
    content = content.replace("](LICENSE)", "](./LICENSE.md)")
    content = content.replace("](../../LICENSE)", "](./LICENSE.md)")
    content = content.replace("](NOTICE)", "](./NOTICE.md)")
    content = content.replace("](../../NOTICE)", "](./NOTICE.md)")
    content = content.replace("](SECURITY.md)", "](./SECURITY.md)")
    content = content.replace("](../../SECURITY.md)", "](./SECURITY.md)")
    
    # Replace language table at top
    lang_table = generate_language_table("README.md", loc_code, "locale_subdir")
    
    table_pattern_start = content.find("| [KR")
    if table_pattern_start != -1:
        table_pattern_end = content.find("\n\n[![", table_pattern_start)
        if table_pattern_end != -1:
            content = content[:table_pattern_start] + lang_table + content[table_pattern_end:]

    return content


def update_master_files():
    """Synchronize the 8 master files with the updated 5x2 language selector table and Quick Jump bar."""
    print("Updating 8 master files...")
    
    # 1. Root README.md
    readme_path = REPO_ROOT / "README.md"
    readme_content = readme_path.read_text(encoding="utf-8")
    readme_table = generate_language_table("README.md", "en", "repo_root")
    
    # Add Quick Jump bar right below shields
    quick_jump = """
<p align="center">
  <b>Quick Jump:</b>
  <a href="#-interface-previews">Previews</a> •
  <a href="#-key-capabilities">Features</a> •
  <a href="#-system-requirements-dependencies">Requirements</a> •
  <a href="#-installation-execution">Quick Start</a> •
  <a href="#-mobile-web-gui-pwa-remote-control-guide">Mobile PWA</a> •
  <a href="docs/ARCHITECTURE_MAP.md">Architecture</a> •
  <a href="docs/guides/README.md">OS Guides</a> •
  <a href="LICENSE">License</a>
</p>
"""
    # Replace table
    t_start = readme_content.find("| [KR")
    if t_start != -1:
        t_end = readme_content.find("\n\n[![", t_start)
        if t_end != -1:
            readme_content = readme_content[:t_start] + readme_table + "\n" + quick_jump + readme_content[t_end:]
            readme_path.write_text(readme_content, encoding="utf-8")
            print("Updated root README.md")

    # 2. Master CHANGELOG.md
    cl_path = REPO_ROOT / "CHANGELOG.md"
    cl_content = cl_path.read_text(encoding="utf-8")
    cl_table = generate_language_table("CHANGELOG.md", "en", "repo_root")
    
    v125_entry = """## [v12.5.0] — 2026-11-19

### Added
- **12-Language 1:1 Complete Documentation Suite (`docs/locales/<lang>/`)**:
  - Full 1:1 professional localization for all 8 core documents across 12 languages (Korean, English, Japanese, Simplified Chinese, Spanish, French, German, Russian, Portuguese, Arabic, Hindi, Indonesian).
  - Clean modular hierarchy: `docs/locales/<lang>/` housing `README.md`, `ARCHITECTURE_MAP.md`, `GUIDE.md`, `TASKS.md`, `CHANGELOG.md`, `LICENSE.md`, `NOTICE.md`, `SECURITY.md`.
- **GitHub Repository Root Streamlining & Modular Reorganization**:
  - Moved internal maintenance scripts to `deploy/scripts/` and test configuration to `tests/pytest.ini`.
  - Removed duplicate root scripts, reducing root clutter to 6 directories and 8 essential files so README and preview media render prominently above the fold on GitHub.
- **Above-the-Fold Quick Jump Navigation Bar**:
  - Instant one-touch navigation bar below badge strip (`[ Previews | Features | Requirements | Quick Start | Mobile PWA | Architecture | OS Guides | License ]`).
"""
    if "## [v12.5.0]" not in cl_content:
        # Prepend v12.5.0 before [v12.4.0]
        pos = cl_content.find("## [v12.4.0]")
        if pos != -1:
            cl_content = cl_content[:pos] + v125_entry + "\n" + cl_content[pos:]
    
    # Ensure language table at top
    if "| [KR" not in cl_content:
        header_end = cl_content.find("\n\n## [")
        if header_end != -1:
            cl_content = cl_content[:header_end] + "\n\n" + cl_table + cl_content[header_end:]
    else:
        ct_start = cl_content.find("| [KR")
        ct_end = cl_content.find("\n\n## [", ct_start)
        if ct_end != -1:
            cl_content = cl_content[:ct_start] + cl_table + cl_content[ct_end:]
    cl_path.write_text(cl_content, encoding="utf-8")
    print("Updated root CHANGELOG.md")

    # 3. Master docs/GUIDE.md
    guide_path = REPO_ROOT / "docs/GUIDE.md"
    guide_content = guide_path.read_text(encoding="utf-8")
    guide_table = generate_language_table("GUIDE.md", "ko", "docs_root")
    gt_start = guide_content.find("| [KR")
    if gt_start != -1:
        gt_end = guide_content.find("\n\n---", gt_start)
        if gt_end != -1:
            guide_content = guide_content[:gt_start] + guide_table + guide_content[gt_end:]
    else:
        # Insert after title block
        sep_pos = guide_content.find("\n\n---")
        if sep_pos != -1:
            guide_content = guide_content[:sep_pos] + "\n\n" + guide_table + guide_content[sep_pos:]
    guide_path.write_text(guide_content, encoding="utf-8")
    print("Updated docs/GUIDE.md")

    # 4. Master docs/ARCHITECTURE_MAP.md
    arch_path = REPO_ROOT / "docs/ARCHITECTURE_MAP.md"
    arch_content = arch_path.read_text(encoding="utf-8")
    arch_table = generate_language_table("ARCHITECTURE_MAP.md", "ko", "docs_root")
    at_start = arch_content.find("| [KR")
    if at_start != -1:
        at_end = arch_content.find("\n\n---", at_start)
        if at_end != -1:
            arch_content = arch_content[:at_start] + arch_table + arch_content[at_end:]
    else:
        sep_pos = arch_content.find("\n\n---")
        if sep_pos != -1:
            arch_content = arch_content[:sep_pos] + "\n\n" + arch_table + arch_content[sep_pos:]
    arch_path.write_text(arch_content, encoding="utf-8")
    print("Updated docs/ARCHITECTURE_MAP.md")

    # 5. Master docs/TASKS.md
    tasks_path = REPO_ROOT / "docs/TASKS.md"
    tasks_content = tasks_path.read_text(encoding="utf-8")
    tasks_table = generate_language_table("TASKS.md", "ko", "docs_root")
    tt_start = tasks_content.find("| [KR")
    if tt_start != -1:
        tt_end = tasks_content.find("\n\n---", tt_start)
        if tt_end != -1:
            tasks_content = tasks_content[:tt_start] + tasks_table + tasks_content[tt_end:]
    else:
        sep_pos = tasks_content.find("\n\n---")
        if sep_pos != -1:
            tasks_content = tasks_content[:sep_pos] + "\n\n" + tasks_table + tasks_content[sep_pos:]
    tasks_path.write_text(tasks_content, encoding="utf-8")
    print("Updated docs/TASKS.md")

    # 6. Master docs/README.md
    hub_path = REPO_ROOT / "docs/README.md"
    hub_content = hub_path.read_text(encoding="utf-8")
    hub_table = generate_language_table("README.md", "ko", "docs_root")
    ht_start = hub_content.find("| [KR")
    if ht_start != -1:
        ht_end = hub_content.find("\n\n---", ht_start)
        if ht_end != -1:
            hub_content = hub_content[:ht_start] + hub_table + hub_content[ht_end:]
    else:
        sep_pos = hub_content.find("\n\n---")
        if sep_pos != -1:
            hub_content = hub_content[:sep_pos] + "\n\n" + hub_table + hub_content[sep_pos:]
    hub_path.write_text(hub_content, encoding="utf-8")
    print("Updated docs/README.md")

    # 7. Master SECURITY.md
    sec_path = REPO_ROOT / "SECURITY.md"
    sec_content = sec_path.read_text(encoding="utf-8")
    sec_table = generate_language_table("SECURITY.md", "en", "repo_root")
    st_start = sec_content.find("| [KR")
    if st_start != -1:
        st_end = sec_content.find("\n\n##", st_start)
        if st_end != -1:
            sec_content = sec_content[:st_start] + sec_table + sec_content[st_end:]
    else:
        sep_pos = sec_content.find("\n\n##")
        if sep_pos != -1:
            sec_content = sec_content[:sep_pos] + "\n\n" + sec_table + sec_content[sep_pos:]
    sec_path.write_text(sec_content, encoding="utf-8")
    print("Updated SECURITY.md")

    # 8. Master NOTICE
    notice_path = REPO_ROOT / "NOTICE"
    notice_content = notice_path.read_text(encoding="utf-8")
    notice_table = generate_language_table("NOTICE", "en", "repo_root")
    nt_start = notice_content.find("| [KR")
    if nt_start != -1:
        nt_end = notice_content.find("\n\n1.", nt_start)
        if nt_end != -1:
            notice_content = notice_content[:nt_start] + notice_table + notice_content[nt_end:]
    else:
        sep_pos = notice_content.find("\n\n1.")
        if sep_pos != -1:
            notice_content = notice_content[:sep_pos] + "\n\n" + notice_table + notice_content[sep_pos:]
    notice_path.write_text(notice_content, encoding="utf-8")
    print("Updated NOTICE")

    # 9. Master LICENSE
    license_path = REPO_ROOT / "LICENSE"
    license_content = license_path.read_text(encoding="utf-8")
    license_table = generate_language_table("LICENSE", "en", "repo_root")
    lt_start = license_content.find("| [KR")
    if lt_start != -1:
        lt_end = license_content.find("\n\nCopyright", lt_start)
        if lt_end != -1:
            license_content = license_content[:lt_start] + license_table + license_content[lt_end:]
    else:
        sep_pos = license_content.find("\n\nCopyright")
        if sep_pos != -1:
            license_content = license_content[:sep_pos] + "\n\n" + license_table + license_content[sep_pos:]
    license_path.write_text(license_content, encoding="utf-8")
    print("Updated LICENSE")


def generate_all():
    print("🚀 Starting D4UC 12-Locale Documentation Suite Generation...")
    sync_badges()

    total_generated = 0
    locales_dir = REPO_ROOT / "docs/locales"
    locales_dir.mkdir(parents=True, exist_ok=True)

    for loc in LOCALES:
        code = loc["code"]
        target_dir = locales_dir / code
        target_dir.mkdir(parents=True, exist_ok=True)
        print(f"\n📁 Processing Locale: [{code}] {loc['name']} ({target_dir})")

        # 1. README.md
        readme_md = generate_main_readme_in_locale(code)
        if readme_md:
            (target_dir / "README.md").write_text(readme_md, encoding="utf-8")
            total_generated += 1

        # 2. ARCHITECTURE_MAP.md
        arch_md = generate_architecture_doc(code)
        (target_dir / "ARCHITECTURE_MAP.md").write_text(arch_md, encoding="utf-8")
        total_generated += 1

        # 3. GUIDE.md
        guide_md = generate_guide_doc(code)
        (target_dir / "GUIDE.md").write_text(guide_md, encoding="utf-8")
        total_generated += 1

        # 4. TASKS.md
        tasks_md = generate_tasks_doc(code)
        (target_dir / "TASKS.md").write_text(tasks_md, encoding="utf-8")
        total_generated += 1

        # 5. CHANGELOG.md
        cl_md = generate_changelog_doc(code)
        (target_dir / "CHANGELOG.md").write_text(cl_md, encoding="utf-8")
        total_generated += 1

        # 6. LICENSE.md
        lic_md = generate_license_doc(code)
        (target_dir / "LICENSE.md").write_text(lic_md, encoding="utf-8")
        total_generated += 1

        # 7. NOTICE.md
        notice_md = generate_notice_doc(code)
        (target_dir / "NOTICE.md").write_text(notice_md, encoding="utf-8")
        total_generated += 1

        # 8. SECURITY.md
        sec_md = generate_security_doc(code)
        (target_dir / "SECURITY.md").write_text(sec_md, encoding="utf-8")
        total_generated += 1

        print(f"   ✅ Generated all 8 docs for [{code}]")

    # Update master files
    update_master_files()

    print(f"\n🎉 Successfully generated {total_generated} localized documents across 12 locales!")


if __name__ == "__main__":
    generate_all()
