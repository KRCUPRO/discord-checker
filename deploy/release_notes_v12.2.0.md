# ⚡ D4UC (`discord-checker`) v12.2.0

## 📱 What's New in v12.2.0

### 1. Mobile Touch-Optimized Responsive Web GUI & PWA Engine (`src/ui/web/`, `src/web_gui.py`)
- **Remote Mobile Control**: Host locally, on a VPS, or inside Docker/Termux and control everything from any smartphone browser (iPhone Safari, Android Chrome) at `http://<host>:5000`.
- **Native PWA (Add to Home Screen)**: Full-screen standalone web application experience with custom app icons (`icon-192.png`, `icon-512.png`, `favicon.svg`) and offline asset caching via `sw.js`.
- **Touch-Friendly Controls**:
  - Full proxy configuration (Surfshark isolated key pool, custom proxy files, Thordata dynamic proxies).
  - Target generator control: 8 generation modes (Hybrid, Permutation, Dictionary, Pattern, Numeric, Custom Mask, Combinatorial, Recheck), length selection (3–6), sharding keys, prefix/suffix/dot rules.
  - Concurrency slider (1–50 workers) with real-time hot-scaling without restart.
  - Real-time rolling RPS speed curve on pure HTML5 Canvas (zero external chart dependencies).
  - 1-tap clipboard copy for available usernames with toast alert.
  - Multi-format instant export: `.txt`, `.csv`, `.json`.
  - Big touch-friendly Start, Stop, and Restart buttons.

### 2. Standalone Windows Web Executable (`DiscordUsernameCheckerV2_Web.exe`)
- Embedded HTTP web server and bundled PWA assets into a single zero-dependency Windows executable.
- Launches the web engine and automatically displays the local network URL (`http://<PC_IP>:5000`) for 1-tap mobile pairing.

### 3. 1:1 Full Localization for ALL 11 Locale Documents (`docs/locales/*.md`)
- Exhaustive, native professional translations across all 18 major sections for:
  - 🇰🇷 Korean (`docs/locales/ko.md`)
  - 🇺🇸 US English (`README.md`)
  - 🇯🇵 Japanese (`docs/locales/ja.md`)
  - 🇨🇳 Simplified Chinese (`docs/locales/zh-CN.md`)
  - 🇪🇸 Spanish (`docs/locales/es.md`)
  - 🇫🇷 French (`docs/locales/fr.md`)
  - 🇩🇪 German (`docs/locales/de.md`)
  - 🇷🇺 Russian (`docs/locales/ru.md`)
  - 🇧🇷 Portuguese (`docs/locales/pt-BR.md`)
  - 🇸🇦 Arabic (`docs/locales/ar.md`)
  - 🇮🇳 Hindi (`docs/locales/hi.md`)
  - 🇮🇩 Indonesian (`docs/locales/id.md`)

### 4. 1:1 Localized SVG Update Date Badges (`docs/assets/badges/`)
- Vector SVG update badges for all 12 supported languages reflecting November 19, 2026.

### 5. High-Resolution Mobile Media Assets
- Added smartphone preview screenshot (`docs/assets/mobile_web_main.png`) and animated touch demo GIF (`docs/assets/mobile_web_demo.gif`).

---

## 📦 Attached Binaries
- `DiscordUsernameCheckerV2_Web.exe`: Mobile Web GUI & PWA HTTP Engine (Windows 64-bit)
- `DiscordUsernameCheckerV2_KO.exe`: Korean Desktop GUI (CustomTkinter)
- `DiscordUsernameCheckerV2_EN.exe`: English Desktop GUI (CustomTkinter)
- `DiscordUsernameCheckerV2_CLI.exe`: Headless CLI Terminal Dashboard (Rich)
