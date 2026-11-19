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


def test_apk_bundled_web_assets_integrity():
    """Validates that assets/www/index.html bundled inside the APK is syntactically sound."""
    import zipfile
    import shutil
    import re

    assert APK_PATH.exists()
    with zipfile.ZipFile(APK_PATH, "r") as zf:
        namelist = zf.namelist()
        assert "assets/www/index.html" in namelist, "assets/www/index.html missing inside APK!"
        assert "classes.dex" in namelist, "classes.dex missing inside APK!"
        assert "AndroidManifest.xml" in namelist, "AndroidManifest.xml missing inside APK!"
        
        index_content = zf.read("assets/www/index.html").decode("utf-8")
        assert "D4UC Mobile Web" in index_content
        assert "AndroidBridge" in index_content

        # Node syntax check on all scripts inside the APK's index.html
        node_bin = shutil.which("node")
        if node_bin:
            scripts = re.findall(r"<script(?:\s+[^>]*)?>([\s\S]*?)</script>", index_content, re.IGNORECASE)
            assert len(scripts) > 0
            for idx, script in enumerate(scripts):
                res = subprocess.run([node_bin, "-e", "new Function(require('fs').readFileSync(0, 'utf-8'))"], input=script, capture_output=True, text=True, encoding="utf-8")
                assert res.returncode == 0, f"Script block {idx} inside bundled APK has syntax error:\n{res.stderr}"
