# 🛡️ Security Policy

## Responsible Usage & Safety Best Practices

### 1. Credentials & Private Keys Protection
- **Never commit `config.yaml`, `.env`, or `credentials.json`** to public version control.
- This repository is pre-configured with a strict `.gitignore` to prevent accidental credential leakage.
- Always use `.env.example` and `config.example.yaml` as references when setting up your local environment.

### 2. Discord API Rate-Limiting & Safety
- D4UC uses `curl_cffi` to mimic genuine Chrome 131 browser TLS handshakes (JA3/JA4 fingerprints).
- When using proxies, ensure you use the integrated Surfshark 1:1 multi-tunnel engine or rotating proxies to distribute requests across distinct IPs.
- Respect Discord's service limits and avoid excessive concurrency without sufficient proxy distribution.

### 3. Reporting a Vulnerability
If you discover a security vulnerability or credential leak within this codebase, please open a private security advisory or contact the maintainer directly.
