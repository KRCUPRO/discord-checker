# src/utils/paths.py
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Optional

def get_app_dir() -> Path:
    """
    Returns the persistent application directory where the executable or script is installed.
    - If running as a PyInstaller frozen exe: directory containing sys.executable.
    - If running as normal Python: root directory of the repository.
    """
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent.resolve()
    return Path(__file__).resolve().parent.parent.parent

def get_bundle_dir() -> Path:
    """
    Returns the bundled resources directory (_MEIPASS) during PyInstaller execution,
    or falls back to get_app_dir().
    """
    if hasattr(sys, "_MEIPASS"):
        return Path(getattr(sys, "_MEIPASS")).resolve()
    return get_app_dir()

def resolve_resource(relative_path: str) -> Path:
    """
    Resolves a read-only or default resource path.
    1. If already absolute, return directly
    2. Checks if file exists in get_app_dir() / relative_path (user modified/local)
    3. Checks if file exists in get_bundle_dir() / relative_path (bundled with exe)
    4. Falls back to get_app_dir() / relative_path
    """
    p = Path(relative_path)
    if p.is_absolute():
        return p
    local = get_app_dir() / relative_path
    if local.exists():
        return local
    bundled = get_bundle_dir() / relative_path
    if bundled.exists():
        return bundled
    return local

def resolve_output_path(relative_path: str) -> Path:
    """
    Resolves a writable output path (DB, logs, output text files)
    always located in get_app_dir() unless already an absolute path.
    """
    p = Path(relative_path)
    if p.is_absolute():
        p.parent.mkdir(parents=True, exist_ok=True)
        return p
    p = get_app_dir() / relative_path
    p.parent.mkdir(parents=True, exist_ok=True)
    return p

_FIREWALL_CHECKED = False

def ensure_wireproxy_firewall_rule(bin_path: Path):
    """
    Ensures Windows Defender Firewall rules (Inbound & Outbound, Allow, Loopback/Any)
    exist for wireproxy.exe so Windows NEVER prompts the user with security dialogs.
    No-op on Linux / macOS / Docker / Termux.
    """
    if sys.platform != "win32":
        return

    global _FIREWALL_CHECKED
    if _FIREWALL_CHECKED:
        return
    _FIREWALL_CHECKED = True

    try:
        bin_str = str(bin_path.resolve())
        # Use a stable hash/name based on path
        rule_name = "D4UC_Wireproxy_Tunnel"
        ps_script = (
            f'$p = "{bin_str}"; '
            f'if (-not (Get-NetFirewallRule -DisplayName "{rule_name}" -ErrorAction SilentlyContinue)) {{ '
            f'  New-NetFirewallRule -DisplayName "{rule_name}" -Direction Inbound -Program $p -Action Allow -Profile Any | Out-Null; '
            f'  New-NetFirewallRule -DisplayName "{rule_name} Out" -Direction Outbound -Program $p -Action Allow -Profile Any | Out-Null '
            f'}}'
        )
        creationflags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
        subprocess.run(
            ["powershell", "-NoProfile", "-NonInteractive", "-Command", ps_script],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=creationflags,
            timeout=5
        )
    except Exception:
        pass

def _make_executable_if_posix(p: Path):
    """Linux/POSIX 환경에서 바이너리에 실행 권한(chmod +x) 자동 부여"""
    if sys.platform != "win32" and p.exists():
        try:
            import stat
            st = p.stat()
            p.chmod(st.st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)
        except Exception:
            pass

def find_wireproxy_bin() -> Path:
    """
    Finds or extracts wireproxy binary to a fixed, persistent location.
    - Windows: wireproxy.exe with automatic Windows Defender Firewall whitelist
    - Linux / Termux / Docker: wireproxy with auto-detection from system PATH or bin/
    """
    is_windows = sys.platform == "win32"
    bin_name = "wireproxy.exe" if is_windows else "wireproxy"

    # 1. Check system PATH first on Linux / Docker / Termux
    which_bin = shutil.which(bin_name) or (shutil.which("wireproxy") if not is_windows else None)
    if which_bin:
        p = Path(which_bin).resolve()
        if p.is_file():
            _make_executable_if_posix(p)
            return p

    persistent_dir = get_app_dir() / "bin"
    persistent_bin = persistent_dir / bin_name

    if persistent_bin.is_file():
        if is_windows:
            ensure_wireproxy_firewall_rule(persistent_bin)
        else:
            _make_executable_if_posix(persistent_bin)
        return persistent_bin.resolve()

    # If missing in persistent_dir, search candidate sources and copy to persistent_dir
    sources = [
        get_bundle_dir() / "bin" / bin_name,
        get_bundle_dir() / bin_name,
        Path(f"bin/{bin_name}").resolve(),
        Path(f"/usr/local/bin/{bin_name}"),
        Path(f"/usr/bin/{bin_name}"),
        Path.cwd() / "bin" / bin_name,
        Path.home() / "go" / "bin" / bin_name,
    ]

    for s in sources:
        if s and s.is_file():
            try:
                persistent_dir.mkdir(parents=True, exist_ok=True)
                shutil.copy2(str(s), str(persistent_bin))
                if is_windows:
                    ensure_wireproxy_firewall_rule(persistent_bin)
                else:
                    _make_executable_if_posix(persistent_bin)
                return persistent_bin.resolve()
            except Exception:
                if is_windows:
                    ensure_wireproxy_firewall_rule(s)
                else:
                    _make_executable_if_posix(s)
                return s.resolve()

    return persistent_bin.resolve()
