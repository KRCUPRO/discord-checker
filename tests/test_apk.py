# tests/test_apk.py
"""
Unit and integration test for D4UC Android APK deliverable.
Validates APK existence, package badging, permissions, and cryptographic signatures.
"""

import os
import subprocess
from pathlib import Path
import pytest

REPO_ROOT = Path(__file__).parent.parent.resolve()
SDK_BUILD_TOOLS = Path(os.environ.get("ANDROID_BUILD_TOOLS", r"C:\Users\Administrator\AppData\Local\Android\Sdk\build-tools\35.0.0"))
AAPT = SDK_BUILD_TOOLS / "aapt.exe"
APKSIGNER = SDK_BUILD_TOOLS / "apksigner.bat"

APK_PATH = REPO_ROOT / "dist" / "DiscordUsernameChecker_v12.3.0.apk"
BIN_APK_PATH = REPO_ROOT / "bin" / "DiscordUsernameChecker_v12.3.0.apk"


def test_apk_files_exist():
    assert APK_PATH.exists(), f"APK missing at {APK_PATH}"
    assert BIN_APK_PATH.exists(), f"Bin APK missing at {BIN_APK_PATH}"
    assert APK_PATH.stat().st_size > 20 * 1024, "APK size too small"


def test_apk_aapt_badging():
    if not AAPT.exists():
        pytest.skip("aapt.exe not found on host")

    res = subprocess.run([str(AAPT), "dump", "badging", str(APK_PATH)], capture_output=True, text=True, encoding="utf-8", errors="replace")
    assert res.returncode == 0, f"aapt dump badging failed: {res.stderr}"
    
    stdout = res.stdout
    assert "package: name='com.krcupro.discordchecker'" in stdout
    assert "versionCode='1230'" in stdout
    assert "versionName='12.3.0'" in stdout
    assert "application-label:'D4UC Discord Checker'" in stdout
    assert "launchable-activity: name='com.krcupro.discordchecker.MainActivity'" in stdout
    assert "android.permission.INTERNET" in stdout
    assert "android.permission.ACCESS_NETWORK_STATE" in stdout
    assert "android.permission.WAKE_LOCK" in stdout


def test_apk_cryptographic_signatures():
    if not APKSIGNER.exists():
        pytest.skip("apksigner.bat not found on host")

    res = subprocess.run([str(APKSIGNER), "verify", "--verbose", str(APK_PATH)], capture_output=True, text=True, encoding="utf-8", errors="replace")
    assert res.returncode == 0, f"apksigner verify failed: {res.stderr}"
    
    stdout = res.stdout
    assert "Verified using v1 scheme (JAR signing): true" in stdout or "Verified using v2 scheme (APK Signature Scheme v2): true" in stdout
    assert "Number of signers: 1" in stdout
