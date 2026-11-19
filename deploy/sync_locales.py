# deploy/sync_locales.py
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOCALES_DIR = ROOT / "docs" / "locales"

TABLE = """| [KR 한국어](./ko.md) | [US English](../../README.md) | [JP 日本語](./ja.md) | [CN 简体中文](./zh-CN.md) | [ES Español](./es.md) |
| :---: | :---: | :---: | :---: | :---: |
| [FR Français](./fr.md) | [DE Deutsch](./de.md) | [RU Русский](./ru.md) | [BR Português](./pt-BR.md) | [SA العربية](./ar.md) |
| [HI हिन्दी](./hi.md) | [ID Bahasa Indonesia](./id.md) | | | |"""

BADGE = "[![최종 업데이트: 2026년 11월 19일](../assets/badges/update_badge.svg)](../../CHANGELOG.md)"

SECTION_EXCLUSION = {
    "ja": """
---

## 🚫 生成から除外されるユーザー名 (例: `ab..`, `a..1`)

Discord の公式ユーザー名ポリシーに基づき、以下の無効なユーザー名は候補生成時に 100% 事前除外されます：
1. **連続したドット (`..`) の禁止**:
   - `ab..` (末尾の連続ドット) ➔ **自動除外**
   - `a..1` (中間の連続ドット) ➔ **自動除外**
   - `..kr` (先頭の連続ドット) ➔ **自動除外**
2. **先頭および末尾の単一ドット (`.`) の禁止**: `.abc`, `abc.` ➔ **自動除外**
3. **使用可能文字**: 英小文字 (`a-z`), 数字 (`0-9`), アンダースコア (`_`), 単一ドット (`.`) のみ許可
4. **予約語除外**: `discord`, `clyde`, `system`, `everyone` などのシステム予約語は自動フィルタリング

> 全ての検証ロジックは `DiscordRuleValidator.is_valid()` によって厳密に管理され、84 種のテストを通過しています。

## 📞 お問い合わせ Discord : myuyayam

ご質問やサポートは Discord **`myuyayam`** までお問い合わせください。
""",
    "zh-CN": """
---

## 🚫 生成排除的用户名规则 (示例: `ab..`, `a..1`)

根据 Discord 官方用户名规范，以下格式在生成时将 100% 自动排除，绝不浪费网络请求：
1. **禁止连续句点 (`..`)**:
   - `ab..` (末尾连续句点) ➔ **自动排除**
   - `a..1` (中间连续句点) ➔ **自动排除**
   - `..kr` (起始连续句点) ➔ **自动排除**
2. **禁止前导或末尾单个句点 (`.`)**: `.abc`, `abc.` ➔ **自动排除**
3. **允许字符**: 仅限英文字母小写 (`a-z`), 数字 (`0-9`), 下划线 (`_`), 单句点 (`.`)
4. **系统保留词**: `discord`, `clyde`, `system`, `everyone` 自动过滤

> 所有验证规则均通过 `DiscordRuleValidator.is_valid()` 强制校验，通过 84 项单元测试。

## 📞 联系方式 Discord : myuyayam

如有功能建议或技术支持需求，请联系 Discord **`myuyayam`**。
""",
    "es": """
---

## 🚫 Nombres de Usuario Excluidos (Ejemplos: `ab..`, `a..1`)

De acuerdo con las reglas oficiales de nombres de usuario de Discord, los siguientes patrones quedan 100% excluidos antes del escaneo:
1. **Puntos consecutivos prohibidos (`..`)**:
   - `ab..` (Puntos consecutivos al final) ➔ **Excluido**
   - `a..1` (Puntos consecutivos en medio) ➔ **Excluido**
   - `..kr` (Puntos consecutivos al inicio) ➔ **Excluido**
2. **Prohibido punto único al inicio o final (`.`)**: `.abc`, `abc.` ➔ **Excluido**
3. **Caracteres válidos**: Solo minúsculas (`a-z`), dígitos (`0-9`), guion bajo (`_`) y punto simple (`.`).
4. **Palabras reservadas**: `discord`, `clyde`, `system`, `everyone` filtradas automáticamente.

## 📞 Contacto Discord : myuyayam

Para consultas o soporte técnico, contactar en Discord: **`myuyayam`**.
""",
    "de": """
---

## 🚫 Ausgeschlossene Benutzernamen (Beispiele: `ab..`, `a..1`)

Gemäß den offiziellen Discord-Richtlinien werden folgende ungültige Muster zu 100% vorab gefiltert:
1. **Aufeinanderfolgende Punkte verboten (`..`)**:
   - `ab..` (Am Ende) ➔ **Ausgeschlossen**
   - `a..1` (In der Mitte) ➔ **Ausgeschlossen**
   - `..kr` (Am Anfang) ➔ **Ausgeschlossen**
2. **Punkt am Anfang oder Ende verboten (`.`)**: `.abc`, `abc.` ➔ **Ausgeschlossen**
3. **Erlaubte Zeichen**: Nur Kleinbuchstaben (`a-z`), Ziffern (`0-9`), Unterstrich (`_`) und Einzelpunkt (`.`).
4. **Reservierte Begriffe**: `discord`, `clyde`, `system`, `everyone` werden automatisch blockiert.

## 📞 Discord Kontakt : myuyayam

Fragen und Support via Discord: **`myuyayam`**.
""",
    "fr": """
---

## 🚫 Noms d'utilisateur Exclus (Exemples: `ab..`, `a..1`)

Conformément aux règles d'identifiants de Discord, les motifs suivants sont exclus à 100% avant toute requête:
1. **Points consécutifs interdits (`..`)**:
   - `ab..` (Points consécutifs à la fin) ➔ **Exclu**
   - `a..1` (Points consécutifs au milieu) ➔ **Exclu**
   - `..kr` (Points consécutifs au début) ➔ **Exclu**
2. **Point en début ou fin interdit (`.`)**: `.abc`, `abc.` ➔ **Exclu**
3. **Caractères valides**: Uniquement minuscules (`a-z`), chiffres (`0-9`), souligné (`_`) et point unique (`.`).

## 📞 Contact Discord : myuyayam

Support et questions sur Discord : **`myuyayam`**.
""",
    "pt-BR": """
---

## 🚫 Nomes de Usuário Excluídos (Exemplos: `ab..`, `a..1`)

Seguindo as diretrizes oficiais do Discord, os seguintes formatos são 100% filtrados antes do envio:
1. **Pontos consecutivos proibidos (`..`)**:
   - `ab..` (Pontos consecutivos no final) ➔ **Excluído**
   - `a..1` (Pontos consecutivos no meio) ➔ **Excluído**
   - `..kr` (Pontos consecutivos no início) ➔ **Excluído**
2. **Ponto no início ou final proibido (`.`)**: `.abc`, `abc.` ➔ **Excluído**
3. **Caracteres válidos**: Apenas letras minúsculas (`a-z`), números (`0-9`), sublinhado (`_`) e ponto único (`.`).

## 📞 Contato Discord : myuyayam

Dúvidas e suporte via Discord: **`myuyayam`**.
""",
    "ru": """
---

## 🚫 Исключаемые имена пользователей (Примеры: `ab..`, `a..1`)

Согласно правилам Discord, следующие некорректные шаблоны исключаются на 100% до отправки сетевых запросов:
1. **Запрещены последовательные точки (`..`)**:
   - `ab..` (Точки на конце) ➔ **Исключено**
   - `a..1` (Точки в середине) ➔ **Исключено**
   - `..kr` (Точки в начале) ➔ **Исключено**
2. **Запрещена точка в начале или конце (`.`)**: `.abc`, `abc.` ➔ **Исключено**
3. **Разрешенные символы**: Строчные латинские (`a-z`), цифры (`0-9`), подчеркивание (`_`) и одиночная точка (`.`).

## 📞 Контакт в Discord : myuyayam

Техническая поддержка и связь: Discord **`myuyayam`**.
""",
    "hi": """
---

## 🚫 अमान्य उपयोगकर्ता नाम बहिष्करण नियम (उदाहरण: `ab..`, `a..1`)

Discord के नियमों के अनुसार निम्नलिखित अमान्य पैटर्न पूरी तरह बहिष्कृत हैं:
1. **लगातार बिंदु प्रतिबंधित (`..`)**:
   - `ab..` (अंत में लगातार बिंदु) ➔ **बहिष्कृत**
   - `a..1` (मध्य में लगातार बिंदु) ➔ **बहिष्कृत**
   - `..kr` (शुरुआत में लगातार बिंदु) ➔ **बहिष्कृत**
2. **आरंभ या अंत में बिंदु प्रतिबंधित (`.`)**: `.abc`, `abc.` ➔ **बहिष्कृत**

## 📞 संपर्क Discord : myuyayam

सहायता एवं पूछताछ के लिए Discord: **`myuyayam`**.
""",
    "ar": """
---

## 🚫 أسماء المستخدمين المستبعدة (أمثلة: `ab..` و `a..1`)

وفقاً لإرشادات ديسكورد الرسمية، يتم استبعاد الأنماط التالية بنسبة 100% قبل إرسال الطلب:
1. **النقاط المتتالية ممنوعة (`..`)**:
   - `ab..` (نقاط متتالية في النهاية) ➔ **مستبعد**
   - `a..1` (نقاط متتالية في الوسط) ➔ **مستبعد**
   - `..kr` (نقاط متتالية في البداية) ➔ **مستبعد**
2. **النقطة في البداية أو النهاية ممنوعة (`.`)**: `.abc` و `abc.` ➔ **مستبعد**

## 📞 للتواصل ديسكورد : myuyayam

للاستفسارات والدعم التقني عبر ديسكورد: **`myuyayam`**.
""",
    "id": """
---

## 🚫 Aturan Pengecualian Username (Contoh: `ab..`, `a..1`)

Sesuai panduan resmi Discord, pola username berikut 100% dikecualikan secara otomatis:
1. **Titik berurutan dilarang (`..`)**:
   - `ab..` (Titik berurutan di akhir) ➔ **Dikecualikan**
   - `a..1` (Titik berurutan di tengah) ➔ **Dikecualikan**
   - `..kr` (Titik berurutan di awal) ➔ **Dikecualikan**
2. **Titik di awal atau akhir dilarang (`.`)**: `.abc`, `abc.` ➔ **Dikecualikan**
3. **Karakter yang diizinkan**: Huruf kecil (`a-z`), angka (`0-9`), garis bawah (`_`), dan titik tunggal (`.`).

## 📞 Kontak Discord : myuyayam

Pertanyaan dan dukungan teknis melalui Discord: **`myuyayam`**.
"""
}

def sync_file(p: Path):
    if p.name == "ko.md":
        return # already perfected
    code = p.stem
    content = p.read_text(encoding="utf-8")

    # Replace <p align="center">... with Table
    content = re.sub(r'<p align="center">[\s\S]*?</p>', f"<br />\n\n{TABLE}\n\n<br />\n\n{BADGE}", content)
    
    # Replace v12.0.0 with v12.1.0
    content = content.replace("v12.0.0", "v12.1.0")

    # Append exclusion section if missing
    if "ab.." not in content and code in SECTION_EXCLUSION:
        content += SECTION_EXCLUSION[code]

    p.write_text(content, encoding="utf-8")
    print(f"Synced {p.name}")

def main():
    for f in LOCALES_DIR.glob("*.md"):
        sync_file(f)
    print("All locale docs synchronized!")

if __name__ == "__main__":
    main()
