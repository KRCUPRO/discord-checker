<div align="center">

# 📋 Index des Tâches et Backlog de Développement D4UC (TASKS.md)

> **Historique des jalons par version, état des livrables du système et gestion du backlog**

<br />

| [KR 한국어](../ko/TASKS.md) | [US English](../en/TASKS.md) | [JP 日本語](../ja/TASKS.md) | [CN 简体中文](../zh-CN/TASKS.md) | [ES Español](../es/TASKS.md) |
| :---: | :---: | :---: | :---: | :---: |
| [FR Français](./TASKS.md) | [DE Deutsch](../de/TASKS.md) | [RU Русский](../ru/TASKS.md) | [BR Português](../pt-BR/TASKS.md) | [SA العربية](../ar/TASKS.md) |

<p align="center"><sub>🌐 Also available: <a href="../hi/TASKS.md">HI हिन्दी</a> • <a href="../id/TASKS.md">ID Bahasa Indonesia</a></sub></p>

<br />

[![Last Updated: 19 nov 2026](../../assets/badges/update_badge_fr.svg)](./CHANGELOG.md)
[![Status: Production Stable](https://img.shields.io/badge/Status-Production%20Stable-brightgreen.svg)](./TASKS.md)

</div>

---

<a id="-table-des-matières"></a>
## 📑 Table des Matières
1. [1. Historique des Jalons Achevés (Completed Milestones)](#-1-historique-des-jalons-achevés-completed-milestones)
2. [2. État des Actifs du Système](#-2-état-des-actifs-du-système)
3. [3. Assurance Qualité et Invariants d'Architecture](#-3-assurance-qualité-et-invariants-darchitecture)

---

<a id="-1-historique-des-jalons-achevés-completed-milestones"></a>
## 🎯 1. Historique des Jalons Achevés (Completed Milestones)

| Version | Jalon | Réalisations Clés & Avancées Techniques | Statut |
| :---: | :--- | :--- | :---: |
| **v1~v3** | Cœur Asynchrone & Architecture SQLite | Furtivité TLS Chrome 131 via `curl_cffi`, persistance SQLite et fichiers miroirs txt | ✅ Terminé |
| **v4~v5** | 8 Moteurs de Génération de Noms | Permutation, Hybride, Dictionnaire, Motif, Numérique, Masque, Combinatoire, Revérification | ✅ Terminé |
| **v6~v7** | Pool Multi-Tunnels 1:1 Surfshark | Wireproxy en espace utilisateur, jusqu'à 50 workers simultanés, 142 nœuds mondiaux | ✅ Terminé |
| **v8** | Hot-Swap Atomique Sans Interruption | Bascule en 0,3s d'un tunnel ciblé par un 429 vers un nouveau pays sans bloquer les autres | ✅ Terminé |
| **v9** | Sharding Multi-Fenêtres & Sync BD | Découpage mathématique (`2_1`, `2_2`), synchronisation SQLite WAL en temps réel | ✅ Terminé |
| **v10** | GUI/UX et Amélioration des Débits | Bandeau d'accueil, infobulles complètes, file d'attente debounced de 30ms (60 FPS) | ✅ Terminé |
| **v11** | Termux Mobile & Déploiement Docker | Script 1-clic pour Android `proot-distro debian`, Dockerfile Multi-Arch ARM64/AMD64 | ✅ Terminé |
| **v12.0** | Livraison Multiplateforme Finale | 4 exécutables Windows EXE autonomes, scripts macOS/Linux, règles de sécurité strictes | ✅ Terminé |
| **v12.1** | Publication Sécurisée Zéro Fuite | `.gitignore` renforcé, modèles de configuration, suppression définitive des secrets en dur | ✅ Terminé |
| **v12.2** | Web GUI Tactile & PWA Mobile | Interface Web responsive, PWA avec Service Worker, alertes Webhook en 0,1s | ✅ Terminé |
| **v12.3** | Proxys Publics Gratuits & APK | Collecte depuis 18 sources et validation Cloudflare, APK Android autonome signé | ✅ Terminé |
| **v12.4** | Navigation Bidirectionnelle & Guides | Tables des matières interactives avec retour au sommaire, 13 manuels dédiés par OS | ✅ Terminé |
| **v12.5** | Suite Complète 12 Langues & Nettoyage | Traduction 1:1 de 8 documents en 12 langues, arborescence racine allégée et UX bonifiée | ✅ Terminé |

[⬆️ Retour au Sommaire](#-table-des-matières)

---

<a id="-2-état-des-actifs-du-système"></a>
## 📦 2. État des Actifs du Système

- **Exécution Desktop**: `python src/gui_ko.py` / `python src/gui_en.py` / `python src/run.py` / 4 EXE autonomes (`dist/`)
- **Web GUI Mobile & APK**: Interface tactile port 5000 / cache PWA / `DiscordUsernameChecker_v12.3.0.apk`
- **Conteneurs Docker**: `deploy/Dockerfile` (Multi-Arch), `deploy/docker-compose.yml` (profil 2-shard)
- **Suite Documentaire 12 Langues**: `README.md` et `docs/locales/<lang>/` (alignement 1:1 pour les 12 langues)

[⬆️ Retour au Sommaire](#-table-des-matières)

---

<a id="-3-assurance-qualité-et-invariants-darchitecture"></a>
## 🛡️ 3. Assurance Qualité et Invariants d'Architecture

- **Invariant Zéro Fuite**: Interdiction permanente de tout commit contenant des clés WireGuard ou des identifiants réels.
- **Vérification Mécanique à 100%**: 103 tests unitaires et 13 validations de livrables doivent réussir avec le code de sortie 0.
- **Garantie de Navigation Bidirectionnelle**: Aucun lien rompu parmi l'ensemble des ancres et liens de retour.

[⬆️ Retour au Sommaire](#-table-des-matières)
