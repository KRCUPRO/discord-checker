# build_exe.py
import os
import sys
import subprocess
import shutil
from pathlib import Path

def build():
    root = Path(__file__).resolve().parent.parent
    os.chdir(root)

    # 1. Ensure bin/wireproxy.exe exists
    bin_wireproxy = root / "bin" / "wireproxy.exe"
    if not bin_wireproxy.exists():
        which_wp = shutil.which("wireproxy.exe") or shutil.which("wireproxy")
        candidates = [Path.home() / "go" / "bin" / "wireproxy.exe"]
        if which_wp:
            candidates.insert(0, Path(which_wp))
        for src_wireproxy in candidates:
            if src_wireproxy.exists():
                bin_wireproxy.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src_wireproxy, bin_wireproxy)
                print(f"Copied wireproxy.exe to {bin_wireproxy}")
                break

    # 2. PyInstaller command
    data_flags = [
        "--add-data", f"src{os.pathsep}src",
        "--add-data", f"data{os.pathsep}data",
        "--add-data", f"config/config.example.yaml{os.pathsep}config",
    ]
    if (root / "config.yaml").exists():
        data_flags.extend(["--add-data", f"config.yaml{os.pathsep}."])

    binary_flags = []
    if bin_wireproxy.exists():
        binary_flags.extend(["--add-binary", f"bin/wireproxy.exe{os.pathsep}bin"])

    pyinstaller_args = [
        sys.executable,
        "-m", "PyInstaller",
        "--noconfirm",
        "--clean",
        "--name", "DiscordUsernameCheckerV2",
        "--windowed",
        "--onefile",
        # CustomTkinter & curl_cffi collections
        "--collect-all", "customtkinter",
        "--collect-all", "curl_cffi",
        *data_flags,
        *binary_flags,
        # Hidden imports
        "--hidden-import", "yaml",
        "--hidden-import", "sqlite3",
        "--hidden-import", "asyncio",
        "--hidden-import", "curl_cffi",
        "--hidden-import", "customtkinter",
        # Entrypoint
        "src/gui.py"
    ]

    print("Executing PyInstaller command...")
    res = subprocess.run(pyinstaller_args)
    if res.returncode != 0:
        print(f"PyInstaller build failed with code {res.returncode}")
        sys.exit(res.returncode)

    dist_exe = root / "dist" / "DiscordUsernameCheckerV2.exe"
    if dist_exe.exists():
        size_mb = dist_exe.stat().st_size / (1024 * 1024)
        print(f"Build succeeded! Standalone executable created: {dist_exe} ({size_mb:.2f} MB)")

        # Create KO and EN editions
        ko_exe = root / "dist" / "DiscordUsernameCheckerV2_KO.exe"
        en_exe = root / "dist" / "DiscordUsernameCheckerV2_EN.exe"
        shutil.copy2(dist_exe, ko_exe)
        shutil.copy2(dist_exe, en_exe)
        print(f"Created Korean Edition: {ko_exe}")
        print(f"Created English Edition: {en_exe}")

        # Optional deployment target via environment variable
        deploy_dir = os.environ.get("D4UC_DEPLOY_DIR", "").strip()
        if deploy_dir:
            ws_root = Path(deploy_dir)
            ws_root.mkdir(parents=True, exist_ok=True)
            ws_bin = ws_root / "bin"
            ws_bin.mkdir(parents=True, exist_ok=True)
            if bin_wireproxy.exists():
                try:
                    shutil.copy2(bin_wireproxy, ws_bin / "wireproxy.exe")
                except Exception:
                    pass

            for src, dst in [(ko_exe, ws_root / "DiscordUsernameCheckerV2_KO.exe"), (en_exe, ws_root / "DiscordUsernameCheckerV2_EN.exe"), (dist_exe, ws_root / "DiscordUsernameCheckerV2.exe")]:
                try:
                    shutil.copy2(src, dst)
                except Exception as e:
                    print(f"Warning: Could not overwrite {dst.name} (app may be open): {e}")
            print(f"Deployed standalone executables and bin/wireproxy.exe to {ws_root}")
    else:
        print("Build completed, but output executable was not found.")

if __name__ == "__main__":
    build()
