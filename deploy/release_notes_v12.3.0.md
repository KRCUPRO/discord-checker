# ⚡ D4UC (`discord-checker`) v12.3.0

## 🌐 What's New in v12.3.0: Free Public Proxy Scraper, Live Validator & Android APK

### 1. Free Public Proxy Scraper & Live Multi-Threaded Validator (`src/proxy/free_proxy.py`)
- **100% Zero-Cost Operation**: Enables high-concurrency Discord username checking without requiring paid VPN subscriptions or commercial proxy purchases.
- **Automated Open-Source Proxy Aggregation**:
  - Automatically fetches continually updated proxy candidate lists across 14+ reliable GitHub repositories and Hugging Face public datasets (`TheSpeedX/PROXY-List`, `monosans/proxy-list`, `hookzof/socks5_list`, `roosterkid/openproxylist`, `ShiftyTR/Proxy-List`, `mertguvencli/http-proxy-list`, Hugging Face raw dataset mirrors).
  - Multi-protocol support across HTTP, HTTPS, SOCKS4, and SOCKS5 free proxies with automatic deduplication.
- **Live Asynchronous Verification Gate**:
  - Validates candidate proxies concurrently against real Discord API endpoints (`https://discord.com/api/v9/unique-username/username-attempt-unauthed`) and Cloudflare edge traces.
  - Automatically discards dead nodes, high-latency proxies exceeding 3,500ms, and 403 Cloudflare WAF-blocked addresses.
- **Smart Rotation & Auto-Refresh**:
  - Prioritizes lowest-latency active nodes in round-robin fashion.
  - Applies 15-second cooldown isolation upon receiving 429 rate limit responses, hot-swapping immediately to the next ready node.
  - Periodic background auto-refresher replenishes the pool dynamically.
  - Local JSON caching (`data/free_proxies_verified.json`) enables instant cold restarts without latency penalties.

### 2. Android Smartphone Native Package (`.apk`) Support
- **1-Tap Direct Install**: Deploy and run D4UC directly on any Android smartphone (Galaxy, Pixel, Xiaomi, etc.).
- **High-Performance WebView Architecture**:
  - Bundles the responsive, touch-friendly, 12-language Discord-Dark Web GUI offline into `assets/www/index.html`.
  - `@JavascriptInterface` (`AndroidBridge`): native Android clipboard copy, native toast notifications, wake lock toggle (`WAKE_LOCK`), and server connection URL selector (connect to PC/server IP or local host).
  - Permissions in `AndroidManifest.xml`: `android.permission.INTERNET`, `android.permission.ACCESS_NETWORK_STATE`, `android.permission.WAKE_LOCK`.
  - Launcher icons: `res/mipmap-*/ic_launcher.png` generated from Discord Blurple assets.
- **Reproducible Direct Build Engine**: `deploy/build_apk.py` compiles, converts to `classes.dex`, zipaligns, and signs with v1/v2/v3 signatures.

### 3. Desktop GUI Free Proxy Integration (`src/gui.py`)
- Added `🌐 무료 프록시 자동 수집 (Free Public)` option in the proxy mode selector.
- Added live `[🔄 무료 프록시 수집 & 검증]` / `[🔄 Scrape & Verify Free Proxies]` button with real-time active proxy count badge.
- Automatic pre-flight verification when scan begins with an empty pool.

### 4. Mobile Touch Web GUI & PWA REST APIs (`src/web_gui.py`, `src/ui/web/index.html`)
- Added `Free Public` option in proxy provider selection.
- 1-tap `🔄 무료 프록시 수집 & 검증` button with live status polling.
- Mobile & remote server connection configuration card with native AndroidBridge integration and Wake Lock toggle.
- New REST API endpoints:
  - `POST /api/proxy/scrape`: Triggers asynchronous background scraping & validation.
  - `GET /api/proxy/free_status`: Returns live telemetry: total scraped, verified active count, average latency, and top working proxies.

### 5. Headless CLI Free Proxy Mode (`src/run.py`)
- Support for `--proxy free` (or `-p free`).
- Automatically scrapes, validates, and initializes the verified proxy pool before launching asynchronous workers.

### 6. Documentation & 11 Locale Documents
- Comprehensive documentation across `README.md` and all 11 locale documents in `docs/locales/` (`ko.md`, `ja.md`, `zh-CN.md`, `es.md`, `fr.md`, `de.md`, `ru.md`, `pt-BR.md`, `ar.md`, `hi.md`, `id.md`).
- Added unit tests in `tests/test_free_proxy.py`, `tests/test_apk.py`, and updated `tests/test_deliverables_verification.py`.

---

## 📦 Attached Binaries
- `DiscordUsernameChecker_v12.3.0.apk`: Android Smartphone 1-Tap Package (Signed v1/v2/v3) [NEW]
- `DiscordUsernameCheckerV2_Web.exe`: Mobile Web GUI & PWA HTTP Server (Windows 64-bit)
- `DiscordUsernameCheckerV2_KO.exe`: Korean Desktop GUI (CustomTkinter)
- `DiscordUsernameCheckerV2_EN.exe`: English Desktop GUI (CustomTkinter)
- `DiscordUsernameCheckerV2_CLI.exe`: Headless CLI Dashboard (Rich)
