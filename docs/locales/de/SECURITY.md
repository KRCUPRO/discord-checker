<div align="center">

# 🛡️ Sicherheitsrichtlinie (Security Policy)

> **D4UC Sicherheitsrichtlinien, Schutz von Geheimnissen und koordinierte Offenlegung**

<br />

| [KR 한국어](../ko/SECURITY.md) | [US English](../en/SECURITY.md) | [JP 日本語](../ja/SECURITY.md) | [CN 简体中文](../zh-CN/SECURITY.md) | [ES Español](../es/SECURITY.md) |
| :---: | :---: | :---: | :---: | :---: |
| [FR Français](../fr/SECURITY.md) | [DE Deutsch](./SECURITY.md) | [RU Русский](../ru/SECURITY.md) | [BR Português](../pt-BR/SECURITY.md) | [SA العربية](../ar/SECURITY.md) |

<p align="center"><sub>🌐 Also available: <a href="../hi/SECURITY.md">HI हिन्दी</a> • <a href="../id/SECURITY.md">ID Bahasa Indonesia</a></sub></p>

<br />

[![Last Updated: 19. Nov 2026](../../assets/badges/update_badge_de.svg)](./CHANGELOG.md)
[![Security Policy: Active](https://img.shields.io/badge/Security-Policy%20Active-brightgreen.svg)](https://github.com/KRCUPRO/discord-checker/security)

</div>

---

<a id="-inhaltsverzeichnis"></a>
## 📑 Inhaltsverzeichnis
1. [1. Schutz von Zugangsdaten und privaten Schlüsseln](#-1-schutz-von-zugangsdaten-und-privaten-schlüsseln)
1. [2. Netzwerkisolation und Rate-Limit-Sicherheit](#-2-netzwerkisolation-und-rate-limit-sicherheit)
1. [3. Meldung von Sicherheitslücken](#-3-meldung-von-sicherheitslücken)
1. [4. Verantwortungsbewusste Forschung & Ethik](#-4-verantwortungsbewusste-forschung--ethik)

---

<a id="-1-schutz-von-zugangsdaten-und-privaten-schlüsseln"></a>
## 1. Schutz von Zugangsdaten und privaten Schlüsseln

- **Übertragen Sie `config.yaml`, `.env`, `surfshark_credentials.json` oder `*.conf` niemals in die Versionsverwaltung (Git).**
- Dieses Repository enthält eine gehärtete `.gitignore`-Datei, die lokale Anmeldedaten, Datenbanken (`*.db*`), Ergebnisdateien (`available*.txt`, `taken*.txt`, `results/`) und kompilierte Binärdateien (`*.exe`, `*.apk`) zuverlässig ausschließt.
- Nutzen Sie stets die Vorlagendateien: `config/.env.example`, `config/config.example.yaml` und `data/surfshark_credentials.example.json`.
- Im gesamten Quellcode und in der Dokumentation sind keinerlei private Schlüssel oder Passwörter fest einprogrammiert.

[⬆️ Zurück zum Inhaltsverzeichnis](#-inhaltsverzeichnis)

---

<a id="-2-netzwerkisolation-und-rate-limit-sicherheit"></a>
## 2. Netzwerkisolation und Rate-Limit-Sicherheit

- Alle HTTP-Anfragen nutzen Chrome 131 TLS-Tarnung über `curl_cffi`, geroutet durch isolierte User-Space-Tunnel (`wireproxy`).
- Netzwerkkarten, Routing-Tabellen und DNS-Konfigurationen des Host-Betriebssystems bleiben zu 100 % unverändert.
- Bei Erreichen eines HTTP 429 führt die Engine innerhalb von 0,3 Sekunden einen atomaren Hot-Swap zu einem alternativen Tunnel durch.

[⬆️ Zurück zum Inhaltsverzeichnis](#-inhaltsverzeichnis)

---

<a id="-3-meldung-von-sicherheitslücken"></a>
## 3. Meldung von Sicherheitslücken

- Falls Sie eine Schwachstelle oder versehentlich exponierte Schlüssel entdecken, eröffnen Sie bitte kein öffentliches Ticket.
- Erstellen Sie stattdessen einen vertraulichen Bericht über GitHub **Private Security Advisory** oder wenden Sie sich direkt an den Repository-Inhaber (`KRCUPRO`). Verifizierte Meldungen werden innerhalb von 24 Stunden behoben.

[⬆️ Zurück zum Inhaltsverzeichnis](#-inhaltsverzeichnis)

---

<a id="-4-verantwortungsbewusste-forschung--ethik"></a>
## 4. Verantwortungsbewusste Forschung & Ethik

- D4UC dient ausschließlich Bildungs- und Forschungszwecken in den Bereichen TLS-Fingerprinting, asynchrone Proxy-Pools und Hochleistungsnetzwerke.
- Angriffe zur Dienstverweigerung (DoS/DDoS) oder unautorisierte Aktivitäten sind ausdrücklich untersagt.

[⬆️ Zurück zum Inhaltsverzeichnis](#-inhaltsverzeichnis)

