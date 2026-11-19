# deploy/build_exe.py
"""
Automated PyInstaller build script for D4UC v12.1.0 standalone Windows executables:
1. DiscordUsernameCheckerV2_KO.exe (Korean GUI, windowed)
2. DiscordUsernameCheckerV2_EN.exe (English GUI, windowed)
3. DiscordUsernameCheckerV2_CLI.exe (Headless CLI, console mode)
"""
import os
import sys
import subprocess
import shutil
from pathlib import Path

def build():
    root = Path(__file__).resolve().parent.parent
    os.chdir(root)
    dist_dir = root / "dist"
    dist_dir.mkdir(parents=True, exist_ok=True)

    # 1. Ensure bin/wireproxy.exe exists
    bin_wireproxy = root / "bin" / "wireproxy.exe"
    if not bin_wireproxy.exists():
        parent_wp = root.parent / "bin" / "wireproxy.exe"
        if parent_wp.exists():
            bin_wireproxy.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(parent_wp, bin_wireproxy)
            print(f"Copied wireproxy.exe to {bin_wireproxy}")

    # Shared flags
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

    shared_hidden = [
        "--hidden-import", "yaml",
        "--hidden-import", "sqlite3",
        "--hidden-import", "asyncio",
        "--hidden-import", "curl_cffi",
        "--hidden-import", "customtkinter",
        "--hidden-import", "rich",
        "--hidden-import", "pydantic",
    ]

    targets = [
        {
            "name": "DiscordUsernameCheckerV2_Web",
            "entry": "src/web_gui.py",
            "windowed": False,
        },
        {
            "name": "DiscordUsernameCheckerV2_KO",
            "entry": "src/gui_ko.py",
            "windowed": True,
        },
        {
            "name": "DiscordUsernameCheckerV2_EN",
            "entry": "src/gui_en.py",
            "windowed": True,
        },
        {
            "name": "DiscordUsernameCheckerV2_CLI",
            "entry": "src/run.py",
            "windowed": False,
        },
    ]

    selected_target = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("-") else None
    if selected_target:
        targets = [t for t in targets if t["name"] == selected_target or selected_target in t["name"]]

    for target in targets:
        name = target["name"]
        entry = target["entry"]
        is_windowed = target["windowed"]
        out_exe = dist_dir / f"{name}.exe"
        
        print(f"\n========================================================")
        print(f"🔨 Building {name}.exe (Entry: {entry}, Windowed: {is_windowed})")
        print(f"========================================================")

        cmd = [
            sys.executable,
            "-m", "PyInstaller",
            "--noconfirm",
            "--clean",
            "--name", name,
            "--onefile",
            *data_flags,
            *binary_flags,
            "--collect-all", "curl_cffi",
        ]
        if is_windowed:
            cmd.extend(["--windowed", "--collect-all", "customtkinter"])
        else:
            cmd.extend(["--collect-all", "rich"])

        cmd.extend(shared_hidden)
        cmd.append(entry)

        res = subprocess.run(cmd)
        if res.returncode != 0:
            print(f"❌ PyInstaller build failed for {name} with code {res.returncode}")
            sys.exit(res.returncode)

        if out_exe.exists():
            size_mb = out_exe.stat().st_size / (1024 * 1024)
            print(f"✅ Successfully compiled: {out_exe} ({size_mb:.2f} MB)")
            # Mirror to bin/ directory
            bin_dir = root / "bin"
            bin_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy2(out_exe, bin_dir / out_exe.name)
            print(f"   Mirrored to {bin_dir / out_exe.name}")
        else:
            print(f"❌ Target executable {out_exe} not found after build!")
            sys.exit(1)

    print("\n🎉 Windows Standalone Executables Successfully Built in dist/ and bin/!")
    for t in targets:
        p = dist_dir / f"{t['name']}.exe"
        if p.exists():
            print(f"  • {p.name} ({p.stat().st_size / (1024*1024):.2f} MB)")

if __name__ == "__main__":
    build()
