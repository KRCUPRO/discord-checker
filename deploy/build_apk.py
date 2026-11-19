#!/usr/bin/env python3
"""
deploy/build_apk.py - High-Performance Reproducible Android APK Builder for D4UC
Compiles com.krcupro.discordchecker (D4UC Discord Checker) into an installable release APK.
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

# Paths
REPO_ROOT = Path(__file__).parent.parent.resolve()
DEPLOY_DIR = REPO_ROOT / "deploy"
ANDROID_DIR = DEPLOY_DIR / "android"
RES_DIR = ANDROID_DIR / "res"
SRC_DIR = ANDROID_DIR / "src"
ASSETS_DIR = ANDROID_DIR / "assets"
BUILD_DIR = ANDROID_DIR / "build"
GEN_DIR = BUILD_DIR / "gen"
CLASSES_DIR = BUILD_DIR / "classes"
DEX_DIR = BUILD_DIR / "dex"
DIST_DIR = REPO_ROOT / "dist"
BIN_DIR = REPO_ROOT / "bin"

# Tools discovery
SDK_ROOT = Path(os.environ.get("ANDROID_HOME", r"C:\Users\Administrator\AppData\Local\Android\Sdk"))
BUILD_TOOLS_DIR = Path(os.environ.get("ANDROID_BUILD_TOOLS", str(SDK_ROOT / "build-tools" / "35.0.0")))
PLATFORMS_DIR = SDK_ROOT / "platforms" / "android-35"
ANDROID_JAR = PLATFORMS_DIR / "android.jar"

AAPT = BUILD_TOOLS_DIR / "aapt.exe"
D8 = BUILD_TOOLS_DIR / "d8.bat"
ZIPALIGN = BUILD_TOOLS_DIR / "zipalign.exe"
APKSIGNER = BUILD_TOOLS_DIR / "apksigner.bat"
JAVAC = shutil.which("javac") or "javac"
KEYTOOL = shutil.which("keytool") or "keytool"

KEYSTORE_PATH = DEPLOY_DIR / "d4uc_release.keystore"
KEYSTORE_PASS = "d4uc123456"
KEYSTORE_ALIAS = "d4uc"

APK_VERSION = "v12.3.0"
OUTPUT_APK_NAME = f"DiscordUsernameChecker_{APK_VERSION}.apk"
FINAL_DIST_APK = DIST_DIR / OUTPUT_APK_NAME
FINAL_BIN_APK = BIN_DIR / OUTPUT_APK_NAME


def run_cmd(cmd, cwd=None):
    return subprocess.run(
        cmd,
        cwd=cwd,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace"
    )


def check_prerequisites():
    print("🔍 [1/8] Checking Android SDK & Java Compiler Prerequisites...")
    assert AAPT.exists(), f"Missing aapt at {AAPT}"
    assert D8.exists(), f"Missing d8 at {D8}"
    assert ZIPALIGN.exists(), f"Missing zipalign at {ZIPALIGN}"
    assert APKSIGNER.exists(), f"Missing apksigner at {APKSIGNER}"
    assert ANDROID_JAR.exists(), f"Missing android.jar at {ANDROID_JAR}"
    
    # Check javac
    res = run_cmd([JAVAC, "-version"])
    assert res.returncode == 0, f"javac failed: {res.stderr}"
    print(f"   • Java Compiler: {res.stdout.strip() or res.stderr.strip()}")
    print(f"   • Android Build-Tools 35.0.0: OK")
    print(f"   • Android Platform 35 jar: OK")


def generate_launcher_icons():
    print("🎨 [2/8] Generating Android Mipmap Icons from Blurple Assets...")
    from PIL import Image

    src_icon = REPO_ROOT / "src" / "ui" / "web" / "icons" / "icon-512.png"
    assert src_icon.exists(), f"Missing source icon: {src_icon}"
    img = Image.open(src_icon).convert("RGBA")

    densities = {
        "mipmap-mdpi": 48,
        "mipmap-hdpi": 72,
        "mipmap-xhdpi": 96,
        "mipmap-xxhdpi": 144,
        "mipmap-xxxhdpi": 192,
    }

    for folder, size in densities.items():
        out_dir = RES_DIR / folder
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / "ic_launcher.png"
        resized = img.resize((size, size), Image.Resampling.LANCZOS)
        resized.save(out_path, format="PNG")
        print(f"   • Created {folder}/ic_launcher.png ({size}x{size})")


def validate_js_syntax(file_path: Path):
    with open(file_path, "r", encoding="utf-8") as f:
        html = f.read()
    import re
    scripts = re.findall(r"<script(?:\s+[^>]*)?>([\s\S]*?)</script>", html, re.IGNORECASE)
    assert len(scripts) > 0, f"No scripts found in {file_path}"
    
    node_path = shutil.which("node")
    if node_path:
        for idx, script in enumerate(scripts):
            res = subprocess.run([node_path, "-e", "new Function(process.argv[1])", script], capture_output=True, text=True)
            if res.returncode != 0:
                raise SyntaxError(f"JavaScript syntax error in {file_path} (script #{idx}):\n{res.stderr}")


def sync_assets():
    print("📦 [3/8] Synchronizing Web GUI & PWA Assets into assets/www/...")
    target_www = ASSETS_DIR / "www"
    if target_www.exists():
        shutil.rmtree(target_www)
    target_www.mkdir(parents=True, exist_ok=True)

    src_web = REPO_ROOT / "src" / "ui" / "web"
    index_html = src_web / "index.html"
    assert index_html.exists(), f"Missing index.html at {index_html}"
    validate_js_syntax(index_html)
    print("   • Validated Web GUI JavaScript syntax: PASSED")

    for item in src_web.iterdir():
        dest = target_www / item.name
        if item.is_dir():
            shutil.copytree(item, dest)
        else:
            shutil.copy2(item, dest)
    print(f"   • Synchronized {len(list(target_www.glob('**/*')))} assets into {target_www}")


def compile_resources_and_java():
    print("⚙️ [4/8] Generating R.java and Compiling Native Android Java Sources...")
    # Clean build dirs
    for d in (GEN_DIR, CLASSES_DIR, DEX_DIR):
        if d.exists():
            shutil.rmtree(d)
        d.mkdir(parents=True, exist_ok=True)

    manifest_xml = ANDROID_DIR / "AndroidManifest.xml"

    # 1. AAPT package -m -J gen
    aapt_cmd = [
        str(AAPT), "package", "-f", "-m",
        "-J", str(GEN_DIR),
        "-M", str(manifest_xml),
        "-S", str(RES_DIR),
        "-I", str(ANDROID_JAR)
    ]
    res = run_cmd(aapt_cmd)
    if res.returncode != 0:
        raise RuntimeError(f"aapt failed to generate R.java:\n{res.stderr}\n{res.stdout}")
    print("   • R.java generated successfully")

    # 2. Gather Java files
    java_files = [str(p) for p in SRC_DIR.glob("**/*.java")] + [str(p) for p in GEN_DIR.glob("**/*.java")]
    assert len(java_files) > 0, "No Java files found!"

    # 3. Compile with javac
    javac_cmd = [
        JAVAC,
        "-encoding", "UTF-8",
        "-source", "8",
        "-target", "8",
        "-d", str(CLASSES_DIR),
        "-cp", str(ANDROID_JAR),
    ] + java_files

    res = run_cmd(javac_cmd)
    if res.returncode != 0:
        raise RuntimeError(f"javac compilation failed:\n{res.stderr}\n{res.stdout}")
    print(f"   • Compiled {len(java_files)} Java classes to {CLASSES_DIR}")


def build_dex():
    print("🔨 [5/8] Converting Compiled Class Files into classes.dex via D8...")
    class_files = [str(p) for p in CLASSES_DIR.glob("**/*.class")]
    assert len(class_files) > 0, "No compiled class files found!"

    d8_cmd = [
        str(D8),
        "--min-api", "21",
        "--output", str(DEX_DIR),
    ] + class_files

    res = run_cmd(d8_cmd)
    if res.returncode != 0:
        raise RuntimeError(f"d8 conversion failed:\n{res.stderr}\n{res.stdout}")

    dex_file = DEX_DIR / "classes.dex"
    assert dex_file.exists(), f"classes.dex was not generated in {DEX_DIR}"
    print(f"   • Generated {dex_file.name} ({dex_file.stat().st_size / 1024:.1f} KB)")


def package_and_align_apk():
    print("📦 [6/8] Packaging Assets & Resources, Aligning APK with zipalign...")
    manifest_xml = ANDROID_DIR / "AndroidManifest.xml"
    unaligned_apk = BUILD_DIR / "unaligned.apk"
    if unaligned_apk.exists():
        unaligned_apk.unlink()

    # 1. Package initial APK with aapt
    aapt_pkg_cmd = [
        str(AAPT), "package", "-f",
        "-M", str(manifest_xml),
        "-S", str(RES_DIR),
        "-A", str(ASSETS_DIR),
        "-I", str(ANDROID_JAR),
        "-F", str(unaligned_apk)
    ]
    res = run_cmd(aapt_pkg_cmd)
    if res.returncode != 0:
        raise RuntimeError(f"aapt packaging failed:\n{res.stderr}\n{res.stdout}")

    # 2. Add classes.dex into unaligned.apk
    # aapt add must be run from DEX_DIR so classes.dex is stored at the root of the apk
    res = run_cmd([str(AAPT), "add", str(unaligned_apk), "classes.dex"], cwd=str(DEX_DIR))
    if res.returncode != 0:
        raise RuntimeError(f"aapt add classes.dex failed:\n{res.stderr}\n{res.stdout}")
    print(f"   • Unaligned APK created ({unaligned_apk.stat().st_size / 1024:.1f} KB)")

    # 3. Zipalign
    aligned_apk = BUILD_DIR / "aligned.apk"
    if aligned_apk.exists():
        aligned_apk.unlink()

    zipalign_cmd = [str(ZIPALIGN), "-f", "-p", "4", str(unaligned_apk), str(aligned_apk)]
    res = run_cmd(zipalign_cmd)
    if res.returncode != 0:
        raise RuntimeError(f"zipalign failed:\n{res.stderr}\n{res.stdout}")
    print(f"   • 4-byte ZipAligned APK created ({aligned_apk.stat().st_size / 1024:.1f} KB)")
    return aligned_apk


def sign_apk(aligned_apk: Path):
    print("🔐 [7/8] Signing Release APK with apksigner (v1/v2/v3 Schemes)...")
    # 1. Ensure keystore exists
    if not KEYSTORE_PATH.exists():
        print("   • Generating reproducible release keystore...")
        keytool_cmd = [
            KEYTOOL,
            "-genkeypair", "-v",
            "-keystore", str(KEYSTORE_PATH),
            "-storepass", KEYSTORE_PASS,
            "-keypass", KEYSTORE_PASS,
            "-alias", KEYSTORE_ALIAS,
            "-keyalg", "RSA",
            "-keysize", "2048",
            "-validity", "10000",
            "-dname", "CN=D4UC, OU=KRCUPRO, O=KRCUPRO, L=Seoul, ST=Seoul, C=KR"
        ]
        res = run_cmd(keytool_cmd)
        if res.returncode != 0:
            raise RuntimeError(f"keytool failed:\n{res.stderr}\n{res.stdout}")

    DIST_DIR.mkdir(parents=True, exist_ok=True)
    BIN_DIR.mkdir(parents=True, exist_ok=True)

    if FINAL_DIST_APK.exists():
        FINAL_DIST_APK.unlink()

    # 2. Run apksigner
    sign_cmd = [
        str(APKSIGNER), "sign",
        "--ks", str(KEYSTORE_PATH),
        "--ks-key-alias", KEYSTORE_ALIAS,
        "--ks-pass", f"pass:{KEYSTORE_PASS}",
        "--key-pass", f"pass:{KEYSTORE_PASS}",
        "--out", str(FINAL_DIST_APK),
        str(aligned_apk)
    ]
    res = run_cmd(sign_cmd)
    if res.returncode != 0:
        raise RuntimeError(f"apksigner failed:\n{res.stderr}\n{res.stdout}")

    # Copy to bin/
    shutil.copy2(FINAL_DIST_APK, FINAL_BIN_APK)
    print(f"   ✅ Release APK signed and saved to:\n      • {FINAL_DIST_APK}\n      • {FINAL_BIN_APK}")


def verify_apk():
    print("🔬 [8/8] Verifying APK Signature and Metadata...")
    # 1. apksigner verify
    res = run_cmd([str(APKSIGNER), "verify", "--verbose", str(FINAL_DIST_APK)])
    if res.returncode != 0:
        raise RuntimeError(f"apksigner verify failed:\n{res.stderr}\n{res.stdout}")
    print("   • apksigner verify: PASSED (Valid v1/v2/v3 signatures)")

    # 2. aapt dump badging
    res = run_cmd([str(AAPT), "dump", "badging", str(FINAL_DIST_APK)])
    if res.returncode != 0:
        raise RuntimeError(f"aapt dump badging failed:\n{res.stderr}\n{res.stdout}")
    assert "com.krcupro.discordchecker" in res.stdout
    assert "D4UC Discord Checker" in res.stdout
    print("   • aapt dump badging: Verified package and label successfully!")
    print(f"\n🎉 Successfully Built Installable Android Package:\n   📁 {FINAL_DIST_APK} ({FINAL_DIST_APK.stat().st_size / (1024*1024):.2f} MB)")


def main():
    print("=" * 70)
    print("🚀 D4UC Discord Checker Android APK Builder (deploy/build_apk.py)")
    print("=" * 70)
    check_prerequisites()
    generate_launcher_icons()
    sync_assets()
    compile_resources_and_java()
    build_dex()
    aligned_apk = package_and_align_apk()
    sign_apk(aligned_apk)
    verify_apk()
    print("=" * 70)


if __name__ == "__main__":
    main()
