<div align="center">

# 🛡️ Política de Seguridad (Security Policy)

> **Directrices de Seguridad de D4UC, Protección de Secretos y Divulgación Responsable**

<br />

| [KR 한국어](../ko/SECURITY.md) | [US English](../en/SECURITY.md) | [JP 日本語](../ja/SECURITY.md) | [CN 简体中文](../zh-CN/SECURITY.md) | [ES Español](./SECURITY.md) |
| :---: | :---: | :---: | :---: | :---: |
| [FR Français](../fr/SECURITY.md) | [DE Deutsch](../de/SECURITY.md) | [RU Русский](../ru/SECURITY.md) | [BR Português](../pt-BR/SECURITY.md) | [SA العربية](../ar/SECURITY.md) |

<p align="center"><sub>🌐 Also available: <a href="../hi/SECURITY.md">HI हिन्दी</a> • <a href="../id/SECURITY.md">ID Bahasa Indonesia</a></sub></p>

<br />

[![Last Updated: 19 nov 2026](../../assets/badges/update_badge_es.svg)](./CHANGELOG.md)
[![Security Policy: Active](https://img.shields.io/badge/Security-Policy%20Active-brightgreen.svg)](https://github.com/KRCUPRO/discord-checker/security)

</div>

---

<a id="-tabla-de-contenidos"></a>
## 📑 Tabla de Contenidos
1. [1. Protección de Credenciales y Claves Privadas](#-1-protección-de-credenciales-y-claves-privadas)
1. [2. Aislamiento de Red y Seguridad ante Límites de Tasa](#-2-aislamiento-de-red-y-seguridad-ante-límites-de-tasa)
1. [3. Notificación de Incidentes de Seguridad](#-3-notificación-de-incidentes-de-seguridad)
1. [4. Investigación Responsable y Ética](#-4-investigación-responsable-y-ética)

---

<a id="-1-protección-de-credenciales-y-claves-privadas"></a>
## 1. Protección de Credenciales y Claves Privadas

- **Nunca subas `config.yaml`, `.env`, `surfshark_credentials.json` o `*.conf` al control de versiones (Git).**
- Este repositorio incluye un `.gitignore` blindado para bloquear credenciales locales, bases de datos en tiempo de ejecución (`*.db*`), resultados de escaneo (`available*.txt`, `taken*.txt`, `results/`) y binarios compilados (`*.exe`, `*.apk`).
- Comienza siempre duplicando las plantillas oficiales: `config/.env.example`, `config/config.example.yaml` y `data/surfshark_credentials.example.json`.
- Ninguna clave privada, token personal ni credencial propietaria está incrustada en el código fuente o documentación.

[⬆️ Volver al Índice](#-tabla-de-contenidos)

---

<a id="-2-aislamiento-de-red-y-seguridad-ante-límites-de-tasa"></a>
## 2. Aislamiento de Red y Seguridad ante Límites de Tasa

- Todas las peticiones HTTP implementan suplantación TLS sigilosa Chrome 131 mediante `curl_cffi`, enrutadas a través de túneles aislados en espacio de usuario (`wireproxy`).
- Las interfaces de red del sistema operativo anfitrión, tablas de enrutamiento y servidores DNS no sufren ninguna alteración.
- Al detectar un código 429, el motor ejecuta un reemplazo atómico en caliente en menos de 0.3 segundos, distribuyendo la carga de manera segura.

[⬆️ Volver al Índice](#-tabla-de-contenidos)

---

<a id="-3-notificación-de-incidentes-de-seguridad"></a>
## 3. Notificación de Incidentes de Seguridad

- Si detectas una vulnerabilidad o exposición accidental de credenciales, por favor NO abras una incidencia pública.
- Emplea la herramienta **Private Security Advisory** de GitHub o contacta al propietario del repositorio (`KRCUPRO`). Los reportes verificados reciben un parche en menos de 24 horas.

[⬆️ Volver al Índice](#-tabla-de-contenidos)

---

<a id="-4-investigación-responsable-y-ética"></a>
## 4. Investigación Responsable y Ética

- D4UC ha sido desarrollado exclusivamente con fines educativos para el estudio de huellas TLS, orquestación asíncrona de proxies y arquitectura distribuida.
- Queda terminantemente prohibido el uso para ataques DoS/DDoS o vulneración de términos de servicio de terceros.

[⬆️ Volver al Índice](#-tabla-de-contenidos)

