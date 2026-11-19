<div align="center">

# 📋 Índice de Tarefas e Backlog de Desenvolvimento D4UC (TASKS.md)

> **Histórico de marcos por versão, ativos do sistema e gerenciamento de tarefas**

<br />

| [KR 한국어](../ko/TASKS.md) | [US English](../en/TASKS.md) | [JP 日本語](../ja/TASKS.md) | [CN 简体中文](../zh-CN/TASKS.md) | [ES Español](../es/TASKS.md) |
| :---: | :---: | :---: | :---: | :---: |
| [FR Français](../fr/TASKS.md) | [DE Deutsch](../de/TASKS.md) | [RU Русский](../ru/TASKS.md) | [BR Português](./TASKS.md) | [SA العربية](../ar/TASKS.md) |

<p align="center"><sub>🌐 Also available: <a href="../hi/TASKS.md">HI हिन्दी</a> • <a href="../id/TASKS.md">ID Bahasa Indonesia</a></sub></p>

<br />

[![Last Updated: 19 nov 2026](../../assets/badges/update_badge_pt.svg)](./CHANGELOG.md)
[![Status: Production Stable](https://img.shields.io/badge/Status-Production%20Stable-brightgreen.svg)](./TASKS.md)

</div>

---

<a id="-índice"></a>
## 📑 Índice
1. [1. Marcos Concluídos (Completed Milestones)](#-1-marcos-concluídos-completed-milestones)
2. [2. Ativos Atuais do Sistema](#-2-ativos-atuais-do-sistema)
3. [3. Garantia de Qualidade e Invariantes](#-3-garantia-de-qualidade-e-invariantes)

---

<a id="-1-marcos-concluídos-completed-milestones"></a>
## 🎯 1. Marcos Concluídos (Completed Milestones)

| Versão | Título do Marco | Principais Conquistas & Inovações Técnicas | Status |
| :---: | :--- | :--- | :---: |
| **v1~v3** | Núcleo Assíncrono & SQLite | Disfarce TLS Chrome 131 via `curl_cffi`, persistência em SQLite e espelhamento txt | ✅ Concluído |
| **v4~v5** | 8 Motores de Geração de Nomes | Permutação, Híbrido, Dicionário, Padrão, Numérico, Máscara, Combinatório, Rechecagem | ✅ Concluído |
| **v6~v7** | Pool Multitúnel 1:1 Surfshark | Wireproxy em espaço de usuário, até 50 workers concorrentes, 142 clusters globais | ✅ Concluído |
| **v8** | Hot-Swap Atômico sem Interrupção | Troca imediata de túnel em 0,3s ao detectar 429 sem interromper os demais workers | ✅ Concluído |
| **v9** | Sharding Multi-Janelas & Sincronização | Divisão matemática de intervalos (`2_1`, `2_2`), sincronização em tempo real via SQLite WAL | ✅ Concluído |
| **v10** | GUI/UX & Alta Performance | Banner explicativo, dicas em todos os botões, fila com debounce de 30ms para 60 FPS estáveis | ✅ Concluído |
| **v11** | Termux Móvel & Docker | Script automatizado para Android `proot-distro debian`, Dockerfile Multi-Arch ARM64/AMD64 | ✅ Concluído |
| **v12.0** | Lançamento Multiplataforma | 4 executáveis independentes para Windows, scripts para macOS/Linux, regras de segurança | ✅ Concluído |
| **v12.1** | Publicação Segura no GitHub | `.gitignore` reforçado, modelos de configuração, ausência de senhas no código-fonte | ✅ Concluído |
| **v12.2** | Web GUI Touch & PWA Móvel | Interface Web responsiva, PWA com Service Worker, notificações Webhook em 0,1s | ✅ Concluído |
| **v12.3** | Proxies Gratuitos & APK Android | Coleta de 18 fontes públicas com validação Cloudflare, APK nativo assinado | ✅ Concluído |
| **v12.4** | Navegação Bidirecional & Guias | Sumários interativos com links de retorno, 13 manuais completos por sistema operacional | ✅ Concluído |
| **v12.5** | Suíte Completa em 12 Idiomas & Limpeza | Tradução 1:1 de 8 documentos em 12 idiomas, reorganização da raiz e polimento de UX | ✅ Concluído |

[⬆️ Voltar ao Topo do Índice](#-índice)

---

<a id="-2-ativos-atuais-do-sistema"></a>
## 📦 2. Ativos Atuais do Sistema

- **Execução Desktop**: `python src/gui_ko.py` / `python src/gui_en.py` / `python src/run.py` / 4 EXEs independentes (`dist/`)
- **Web GUI Móvel & APK**: Interface de toque na porta 5000 / cache PWA / `DiscordUsernameChecker_v12.3.0.apk`
- **Pilhas Docker**: `deploy/Dockerfile` (Multi-Arch), `deploy/docker-compose.yml` (perfil 2-shard)
- **Suíte de Documentação em 12 Idiomas**: `README.md` e `docs/locales/<lang>/` (1:1 nos 12 idiomas)

[⬆️ Voltar ao Topo do Índice](#-índice)

---

<a id="-3-garantia-de-qualidade-e-invariantes"></a>
## 🛡️ 3. Garantia de Qualidade e Invariantes

- **Invariante de Zero Vazamentos**: Chaves WireGuard reais e senhas terminantemente bloqueadas no Git.
- **100% de Verificação Mecânica**: Todos os 103 testes unitários e 13 verificações com código de saída 0.
- **Navegação Bidirecional Íntegra**: Todos os links de sumário e retorno ao topo funcionando perfeitamente.

[⬆️ Voltar ao Topo do Índice](#-índice)
