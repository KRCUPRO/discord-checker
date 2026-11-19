<div align="center">

# 🛡️ Politique de Sécurité (Security Policy)

> **Directives de sécurité D4UC, protection des secrets et divulgation responsable**

<br />

| [KR 한국어](../ko/SECURITY.md) | [US English](../en/SECURITY.md) | [JP 日本語](../ja/SECURITY.md) | [CN 简体中文](../zh-CN/SECURITY.md) | [ES Español](../es/SECURITY.md) |
| :---: | :---: | :---: | :---: | :---: |
| [FR Français](./SECURITY.md) | [DE Deutsch](../de/SECURITY.md) | [RU Русский](../ru/SECURITY.md) | [BR Português](../pt-BR/SECURITY.md) | [SA العربية](../ar/SECURITY.md) |

<p align="center"><sub>🌐 Also available: <a href="../hi/SECURITY.md">HI हिन्दी</a> • <a href="../id/SECURITY.md">ID Bahasa Indonesia</a></sub></p>

<br />

[![Last Updated: 19 nov 2026](../../assets/badges/update_badge_fr.svg)](./CHANGELOG.md)
[![Security Policy: Active](https://img.shields.io/badge/Security-Policy%20Active-brightgreen.svg)](https://github.com/KRCUPRO/discord-checker/security)

</div>

---

<a id="-table-des-matières"></a>
## 📑 Table des Matières
1. [1. Protection des Identifiants et des Clés Privées](#-1-protection-des-identifiants-et-des-clés-privées)
1. [2. Isolation Réseau et Maîtrise du Rate-Limiting](#-2-isolation-réseau-et-maîtrise-du-rate-limiting)
1. [3. Signalement d'une Vulnérabilité](#-3-signalement-dune-vulnérabilité)
1. [4. Démarche Éthique et Recherche Responsable](#-4-démarche-éthique-et-recherche-responsable)

---

<a id="-1-protection-des-identifiants-et-des-clés-privées"></a>
## 1. Protection des Identifiants et des Clés Privées

- **Ne committez jamais `config.yaml`, `.env`, `surfshark_credentials.json` ou `*.conf` dans le dépôt Git.**
- Ce dépôt intègre un fichier `.gitignore` renforcé interdisant les identifiants locaux, bases de données de session (`*.db*`), fichiers de résultats (`available*.txt`, `taken*.txt`, `results/`) et binaires (`*.exe`, `*.apk`).
- Utilisez systématiquement les fichiers modèles fournis : `config/.env.example`, `config/config.example.yaml` et `data/surfshark_credentials.example.json`.
- Aucun secret, jeton d'authentification ou clé WireGuard n'est codé en dur dans le code source ou la documentation.

[⬆️ Retour au Sommaire](#-table-des-matières)

---

<a id="-2-isolation-réseau-et-maîtrise-du-rate-limiting"></a>
## 2. Isolation Réseau et Maîtrise du Rate-Limiting

- L'intégralité des requêtes HTTP exploite l'empreinte TLS furtive Chrome 131 (`curl_cffi`) acheminée via des tunnels en espace utilisateur (`wireproxy`).
- Les cartes réseau, la table de routage principale et les paramètres DNS de votre machine hôte restent totalement préservés.
- Dès détection d'un statut 429, un basculement atomique immédiat s'effectue en moins de 0,3 s sans interrompre les autres flux de travail.

[⬆️ Retour au Sommaire](#-table-des-matières)

---

<a id="-3-signalement-dune-vulnérabilité"></a>
## 3. Signalement d'une Vulnérabilité

- En cas de découverte d'une faille de sécurité ou d'une fuite de données, n'ouvrez pas d'issue publique.
- Transmettez un rapport confidentiel via l'outil **Private Security Advisory** de GitHub ou joignez directement l'auteur (`KRCUPRO`). Une correction sera déployée sous 24h.

[⬆️ Retour au Sommaire](#-table-des-matières)

---

<a id="-4-démarche-éthique-et-recherche-responsable"></a>
## 4. Démarche Éthique et Recherche Responsable

- D4UC est conçu à des fins d'apprentissage technique et de recherche sur les protocoles TLS, la gestion asynchrone de proxies et les architectures concurrentes.
- Toute utilisation abusive, attaque par déni de service (DDoS) ou contournement illicite est rigoureusement interdite.

[⬆️ Retour au Sommaire](#-table-des-matières)

