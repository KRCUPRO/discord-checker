<div align="center">

# 🛡️ Kebijakan Keamanan (Security Policy)

> **Panduan Keamanan D4UC, Perlindungan Kredensial, dan Pengungkapan Bertanggung Jawab**

<br />

| [KR 한국어](../ko/SECURITY.md) | [US English](../en/SECURITY.md) | [JP 日本語](../ja/SECURITY.md) | [CN 简体中文](../zh-CN/SECURITY.md) | [ES Español](../es/SECURITY.md) |
| :---: | :---: | :---: | :---: | :---: |
| [FR Français](../fr/SECURITY.md) | [DE Deutsch](../de/SECURITY.md) | [RU Русский](../ru/SECURITY.md) | [BR Português](../pt-BR/SECURITY.md) | [SA العربية](../ar/SECURITY.md) |

<p align="center"><sub>🌐 Also available: <a href="../hi/SECURITY.md">HI हिन्दी</a> • <a href="./SECURITY.md">ID Bahasa Indonesia</a></sub></p>

<br />

[![Last Updated: 19 Nov 2026](../../assets/badges/update_badge_id.svg)](./CHANGELOG.md)
[![Security Policy: Active](https://img.shields.io/badge/Security-Policy%20Active-brightgreen.svg)](https://github.com/KRCUPRO/discord-checker/security)

</div>

---

<a id="-daftar-isi"></a>
## 📑 Daftar Isi
1. [1. Perlindungan Kredensial & Kunci Privat](#-1-perlindungan-kredensial--kunci-privat)
1. [2. Isolasi Jaringan dan Keamanan Batas Kecepatan (Rate-Limit)](#-2-isolasi-jaringan-dan-keamanan-batas-kecepatan-rate-limit)
1. [3. Pelaporan Kerentanan Keamanan](#-3-pelaporan-kerentanan-keamanan)
1. [4. Riset Bertanggung Jawab & Etika](#-4-riset-bertanggung-jawab--etika)

---

<a id="-1-perlindungan-kredensial--kunci-privat"></a>
## 1. Perlindungan Kredensial & Kunci Privat

- **Jangan pernah melakukan commit file `config.yaml`, `.env`, `surfshark_credentials.json`, atau `*.conf` ke dalam Git.**
- Repositori ini dilengkapi dengan konfigurasi `.gitignore` yang ketat untuk mencegah terunggahnya kredensial lokal, database sesi (`*.db*`), hasil pemindaian (`available*.txt`, `taken*.txt`, `results/`), serta biner hasil kompilasi (`*.exe`, `*.apk`).
- Selalu salin konfigurasi awal dari templat yang disediakan: `config/.env.example`, `config/config.example.yaml`, dan `data/surfshark_credentials.example.json`.
- Tidak ada kredensial pribadi, kunci WireGuard, atau token akses yang disematkan secara langsung di dalam kode sumber.

[⬆️ Kembali ke Daftar Isi](#-daftar-isi)

---

<a id="-2-isolasi-jaringan-dan-keamanan-batas-kecepatan-rate-limit"></a>
## 2. Isolasi Jaringan dan Keamanan Batas Kecepatan (Rate-Limit)

- Seluruh permintaan HTTP memanfaatkan peniruan TLS siluman Chrome 131 (`curl_cffi`) yang dirutekan melalui terowongan terisolasi ruang pengguna (`wireproxy`).
- Pengaturan adaptor jaringan fisik, tabel perutean utama, dan DNS pada sistem operasi host tetap 100% utuh tanpa perubahan.
- Saat kode respons 429 terdeteksi, mesin segera menjalankan hot-swap atomik dalam kurun waktu kurang dari 0,3 detik untuk mengalihkan rute secara mulus.

[⬆️ Kembali ke Daftar Isi](#-daftar-isi)

---

<a id="-3-pelaporan-kerentanan-keamanan"></a>
## 3. Pelaporan Kerentanan Keamanan

- Jika Anda menemukan celah keamanan atau paparan kredensial secara tidak sengaja, mohon TIDAK membuka issue publik.
- Kirimkan laporan rahasia melalui GitHub **Private Security Advisory** atau hubungi pengelola proyek (`KRCUPRO`) secara langsung. Laporan valid akan ditangani dalam waktu 24 jam.

[⬆️ Kembali ke Daftar Isi](#-daftar-isi)

---

<a id="-4-riset-bertanggung-jawab--etika"></a>
## 4. Riset Bertanggung Jawab & Etika

- D4UC dirancang khusus untuk pembelajaran teknis mengenai TLS fingerprinting, orkestrasi proxy asinkron, dan arsitektur konkurensi tinggi.
- Dilarang keras menggunakan program ini untuk serangan penolakan layanan (DoS/DDoS) atau pelanggaran ketentuan layanan pihak ketiga.

[⬆️ Kembali ke Daftar Isi](#-daftar-isi)

