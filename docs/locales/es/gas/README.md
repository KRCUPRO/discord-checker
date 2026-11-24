<div align="center">

# ⚡ D4UC Google Apps Script (GAS) Verificador 24/7 sin Servidor

> **¡Sin necesidad de mantener tu PC, teléfono o Colab encendido!** Se ejecuta en Google Cloud las 24 horas, los 365 días del año mediante activadores programados.

<br />

| [KR 한국어](../ko/gas/README.md) | [US English](../en/gas/README.md) | [JP 日本語](../ja/gas/README.md) | [CN 简体中文](../zh-CN/gas/README.md) | [ES Español](../es/gas/README.md) |
| :---: | :---: | :---: | :---: | :---: |
| [FR Français](../fr/gas/README.md) | [DE Deutsch](../de/gas/README.md) | [RU Русский](../ru/gas/README.md) | [BR Português](../pt-BR/gas/README.md) | [SA العربية](../ar/gas/README.md) |

<p align="center"><sub>🌐 Also available: <a href="../hi/gas/README.md">HI हिन्दी</a> • <a href="../id/gas/README.md">ID Bahasa Indonesia</a></sub></p>

---


</div>

## 🚀 Guía de Inicio Rápido de 1 Minuto

### Paso 1: Crear proyecto de Google Apps Script
1. Abre [Google Apps Script](https://script.google.com/).
2. Haz clic en **[+ Nuevo proyecto]** y nombra `D4UC 24/7 Checker`.

---

### Paso 2: Copiar código y configurar
1. Pega [`gas/D4UC_Checker.js`](https://github.com/KRCUPRO/discord-checker/blob/main/gas/D4UC_Checker.js) en `Code.gs`.
2. Configura `CONFIG` y guarda.

---

### Paso 3: Inicializar ejecución 24/7
1. Selecciona **`initD4UCChecker`** y haz clic en **[Ejecutar]**.
2. Otorga los permisos requeridos.

---

## 📊 Comprobación de Resultados
Guardado en Google Drive, Google Sheets y alertas en Discord Webhook.

---

## 🌐 Aceleración con Múltiples Cuentas (100k~240k Diarias)
Usa [`gas/D4UC_MultiAccount_Worker.js`](https://github.com/KRCUPRO/discord-checker/blob/main/gas/D4UC_MultiAccount_Worker.js) en cuentas secundarias con `WORKER_ID` (0..N-1) y el mismo Discord Webhook.

---

## 🛑 Detener el Verificador
Ejecuta **`stopD4UCChecker`** para eliminar todos los activadores.
