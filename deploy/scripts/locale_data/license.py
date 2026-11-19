# deploy/scripts/locale_data/license.py
"""
1:1 Full Localization for LICENSE.md across all 12 locales.
"""

OFFICIAL_LICENSE_TEXT = """PROPRIETARY & CONFIDENTIAL SOFTWARE LICENSE

Copyright (c) 2026 KRCUPRO. All Rights Reserved.

IMPORTANT — READ CAREFULLY:
This software and associated documentation files (the "Software") are the proprietary
and confidential property of the Copyright Holder (KRCUPRO).

This repository is publicly visible on GitHub for evaluation, reference, and review.
However, NO LICENSE, express or implied, is granted to any person obtaining a copy of
this Software to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, or to create derivative works based upon the Software, without
the prior express written permission of the Copyright Holder.

1. RESTRICTIONS ON USE:
   - You may NOT copy, reproduce, or mirror this repository or any part of its source code.
   - You may NOT modify, adapt, translate, or create derivative works based upon the Software.
   - You may NOT redistribute, sublicense, rent, lease, or resell the Software or any portion thereof.
   - You may NOT deploy or use the Software in commercial production environments without an express commercial license.
   - You may NOT reverse engineer, decompile, or disassemble binary artifacts except as permitted by applicable law.

2. RESERVATION OF RIGHTS:
   The Copyright Holder (KRCUPRO) reserves all rights, title, and interest in and to the Software,
   including all copyright, trademark, patent, trade secret, and intellectual property rights therein.

3. THIRD-PARTY & UPSTREAM NOTICES:
   Any third-party open-source components, toolkits, or libraries incorporated or referenced herein
   strictly retain and preserve all original copyright notices and license terms as detailed in the NOTICE file.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
PURPOSE, AND NONINFRINGEMENT. IN NO EVENT SHALL THE COPYRIGHT HOLDER BE LIABLE FOR ANY CLAIM,
DAMAGES, OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF, OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE."""

LICENSE_DATA = {
    "ko": {
        "title": "⚖️ 소프트웨어 독점 라이선스 (LICENSE)",
        "desc": "D4UC 독점 및 대외비 소프트웨어 라이선스 전문 및 한국어 법률 해설",
        "official_label": "공식 영문 라이선스 전문 (Official Legal Text)",
        "summary_title": "라이선스 핵심 조항 한국어 요약 안내",
        "clauses": [
            ("1. 사용 및 복제 제한", "저작권자(KRCUPRO)의 사전 서면 승인 없이 본 소프트웨어의 소스 코드 전체 또는 일부를 복제, 미러링, 배포, 재판매하거나 상업적 환경에 배포할 수 없습니다."),
            ("2. 지식재산권의 보유", "본 소프트웨어에 관한 저작권, 상표권, 특허권, 영업비밀 등 일체의 지식재산권은 저작권자에게 독점적으로 귀속됩니다."),
            ("3. 제3자 오픈소스의 보호", "프로젝트에 포함된 제3자 오픈소스 패키지는 고유한 라이선스(NOTICE 파일 참조)를 온전히 유지합니다."),
            ("4. 보증의 부인 및 면책", "본 소프트웨어는 어떠한 명시적·묵시적 보증 없이 '있는 그대로(AS IS)' 제공되며, 사용으로 인해 발생하는 일체의 손해에 대해 저작권자는 책임을 지지 않습니다.")
        ]
    },
    "en": {
        "title": "⚖️ Proprietary Software License (LICENSE)",
        "desc": "Official Proprietary & Confidential Software License Text and Legal Summary",
        "official_label": "Official Legal Text",
        "summary_title": "Core License Terms & Legal Summary",
        "clauses": [
            ("1. Restrictions on Use", "No copying, mirroring, modification, distribution, sublicensing, or commercial deployment is permitted without prior written consent from KRCUPRO."),
            ("2. Reservation of Rights", "All copyright, trademark, trade secret, and intellectual property rights are exclusively retained by KRCUPRO."),
            ("3. Third-Party Notices", "Open-source components retain their respective licenses as detailed in the NOTICE file."),
            ("4. Warranty Disclaimer & Liability", "The Software is provided 'AS IS' without warranty of any kind. The Copyright Holder is not liable for any damages arising from its use.")
        ]
    },
    "ja": {
        "title": "⚖️ 専有ソフトウェアライセンス (LICENSE)",
        "desc": "D4UC 専有および機密ソフトウェアライセンス全文ならびに日本語解説",
        "official_label": "公式英文ライセンス全文 (Official Legal Text)",
        "summary_title": "ライセンス重要条項の日本語解説",
        "clauses": [
            ("1. 使用および複製の制限", "著作権者（KRCUPRO）の事前の書面による許諾なく、本ソフトウェアのソースコードを複製、ミラーリング、再配布、商用運用することは禁止されています。"),
            ("2. 権利の留保", "本ソフトウェアに関する特許権、著作権、商標権、企業秘密等の知的財産権は、すべて著作権者に帰属します。"),
            ("3. サードパーティ製ライセンスの尊重", "組み込まれているオープンソースコンポーネントは、それぞれの元のライセンス条件を維持します（NOTICEファイル参照）。"),
            ("4. 保証の否認および免責", "本ソフトウェアは現状有姿（AS IS）で提供され、いかなる明示または黙示の保証も行われません。利用により生じたいかなる損害についても責任を負いません。")
        ]
    },
    "zh-CN": {
        "title": "⚖️ 专有软件许可协议 (LICENSE)",
        "desc": "D4UC 专有与保密软件许可协议原文及中文法律解读",
        "official_label": "官方英文法律文本 (Official Legal Text)",
        "summary_title": "许可协议核心条款中文解读",
        "clauses": [
            ("1. 使用与复制限制", "未经版权所有者（KRCUPRO）的事先书面许可，严禁复制、镜像、修改、分发、转授权或在商业生产环境中部署本软件的全部或任何部分代码。"),
            ("2. 权利保留", "与本软件相关的所有版权、商标权、专利权、商业秘密等知识产权均由版权所有者独家保留。"),
            ("3. 第三方开源组件保护", "项目中引用的第三方开源组件均严格保留其原有的开源许可协议（详见 NOTICE 文件）。"),
            ("4. 免责声明与有限责任", "本软件按“原样（AS IS）”提供，不包含任何明示或暗示的保证。对于因使用本软件引起的任何损失，版权所有者均不承担法律责任。")
        ]
    },
    "es": {
        "title": "⚖️ Licencia de Software Propietario (LICENSE)",
        "desc": "Texto oficial de la licencia confidencial y propietaria de D4UC y resumen legal en español",
        "official_label": "Texto Legal Oficial en Inglés",
        "summary_title": "Resumen de Cláusulas Principales",
        "clauses": [
            ("1. Restricciones de Uso", "Queda terminantemente prohibida la copia, reproducción, duplicación, distribución o explotación comercial sin autorización expresa y por escrito de KRCUPRO."),
            ("2. Reserva de Derechos", "Todos los derechos de propiedad intelectual, patentes, marcas y secretos comerciales son propiedad exclusiva de KRCUPRO."),
            ("3. Avisos de Terceros", "Las herramientas de código abierto incorporadas conservan íntegramente sus respectivas licencias (consulte NOTICE)."),
            ("4. Exclusión de Garantías", "El Software se distribuye 'TAL CUAL' (AS IS), sin garantías explícitas o implícitas de ningún tipo.")
        ]
    },
    "fr": {
        "title": "⚖️ Licence Logicielle Propriétaire (LICENSE)",
        "desc": "Texte officiel de la licence propriétaire et confidentielle D4UC et résumé juridique en français",
        "official_label": "Texte Juridique Officiel (Anglais)",
        "summary_title": "Résumé des Clauses Essentielles",
        "clauses": [
            ("1. Restrictions d'Utilisation", "Toute copie, reproduction, diffusion, modification ou exploitation commerciale sans l'accord écrit préalable de KRCUPRO est formellement interdite."),
            ("2. Réserve de Droits", "L'intégralité des droits d'auteur, brevets, marques et secrets d'affaires demeure la propriété exclusive de KRCUPRO."),
            ("3. Mentions Légales Tierces", "Les bibliothèques tierces intégrées conservent leurs licences respectives d'origine (se référer au fichier NOTICE)."),
            ("4. Exclusion de Garantie", "Le logiciel est fourni 'EN L'ÉTAT' (AS IS), sans garantie d'aucune sorte, expresse ou tacite.")
        ]
    },
    "de": {
        "title": "⚖️ Proprietäre Softwarelizenz (LICENSE)",
        "desc": "Offizieller Lizenztext der proprietären D4UC-Software und deutsche Rechtsübersicht",
        "official_label": "Offizieller Gesetzestext (Englisch)",
        "summary_title": "Zusammenfassung der Lizenzbestimmungen",
        "clauses": [
            ("1. Nutzungsbeschränkungen", "Jegliche Vervielfältigung, Spiegelung, Verbreitung, Unterlizenzierung oder kommerzielle Nutzung ohne vorherige schriftliche Zustimmung von KRCUPRO ist untersagt."),
            ("2. Rechtsvorbehalt", "Alle Urheberrechte, Marken, Patente und Betriebsgeheimnisse verbleiben ausschließlich beim Rechteinhaber (KRCUPRO)."),
            ("3. Drittanbieter-Hinweise", "Eingebundene Open-Source-Komponenten behalten ihre jeweiligen ursprünglichen Lizenzen bei (siehe NOTICE-Datei)."),
            ("4. Gewährleistungsausschluss", "Die Software wird ohne Mängelgewähr ('AS IS') zur Verfügung gestellt. Der Rechteinhaber haftet nicht für Schäden, die aus der Nutzung entstehen.")
        ]
    },
    "ru": {
        "title": "⚖️ Проприетарная лицензия на ПО (LICENSE)",
        "desc": "Официальный текст лицензии D4UC и юридическое резюме на русском языке",
        "official_label": "Официальный юридический текст (на английском языке)",
        "summary_title": "Краткое изложение ключевых условий лицензии",
        "clauses": [
            ("1. Ограничения на использование", "Запрещается копирование, зеркалирование, модификация, распространение или коммерческое использование исходного кода без письменного согласия KRCUPRO."),
            ("2. Сохранение прав", "Все исключительные права на программное обеспечение, товарные знаки и патенты принадлежат исключительно правообладателю (KRCUPRO)."),
            ("3. Уведомления третьих сторон", "Используемые компоненты с открытым исходным кодом сохраняют свои оригинальные лицензии (см. файл NOTICE)."),
            ("4. Отказ от гарантий", "Программное обеспечение предоставляется на условиях «КАК ЕСТЬ» (AS IS) без каких-либо явных или подразумеваемых гарантий.")
        ]
    },
    "pt-BR": {
        "title": "⚖️ Licença de Software Proprietário (LICENSE)",
        "desc": "Texto oficial da licença confidencial do D4UC e resumo legal em português",
        "official_label": "Texto Jurídico Oficial (Inglês)",
        "summary_title": "Resumo dos Termos Principais da Licença",
        "clauses": [
            ("1. Restrições de Uso", "É estritamente proibida a cópia, espelhamento, modificação, redistribuição ou uso comercial sem autorização prévia por escrito da KRCUPRO."),
            ("2. Reserva de Direitos", "Todos os direitos autorais, marcas registradas e propriedades intelectuais pertencem exclusivamente à KRCUPRO."),
            ("3. Avisos de Terceiros", "Bibliotecas de código aberto incorporadas preservam integralmente seus termos de licença originais (veja o arquivo NOTICE)."),
            ("4. Isenção de Garantias", "O Software é fornecido 'NO ESTADO EM QUE SE ENCONTRA' (AS IS), sem garantias de qualquer tipo expressas ou implícitas.")
        ]
    },
    "ar": {
        "title": "⚖️ رخصة البرمجيات الاحتكارية (LICENSE)",
        "desc": "النص الرسمي لرخصة برمجيات D4UC السرية والملكية الفكرية وملخص قانوني بالعربية",
        "official_label": "النص القانوني الرسمي باللغة الإنجليزية",
        "summary_title": "ملخص البنود والشروط الأساسية للترخيص",
        "clauses": [
            ("1. قيود الاستخدام", "يُحظر تماماً نسخ أو استنساخ أو تعديل أو توزيع أو تأجير أو استخدام هذا البرنامج في بيئات إنتاج تجارية دون إذن كتابي مسبق من KRCUPRO."),
            ("2. حفظ الحقوق", "تحتفظ KRCUPRO بكافة حقوق النشر والعلامات التجارية وبراءات الاختراع والملكية الفكرية الخاصة بهذا البرنامج."),
            ("3. إشعارات الجهات الخارجية", "تحتفظ مكونات المصادر المفتوحة المضمنة بتراخيصها الأصلية دون أي مساس (راجع ملف NOTICE)."),
            ("4. إخلاء المسؤولية", "يتم توفير البرنامج 'كما هو' (AS IS) دون أي ضمانات صريحة أو ضمنية من أي نوع، وتخلي الجهة المالكة مسؤوليتها عن أي أضرار ناتجة عن الاستخدام.")
        ]
    },
    "hi": {
        "title": "⚖️ मालिकाना सॉफ़्टवेयर लाइसेंस (LICENSE)",
        "desc": "D4UC मालिकाना और गोपनीय सॉफ़्टवेयर लाइसेंस का आधिकारिक पाठ और कानूनी सारांश",
        "official_label": "आधिकारिक कानूनी पाठ (अंग्रेजी)",
        "summary_title": "लाइसेंस की मुख्य शर्तों का सारांश",
        "clauses": [
            ("1. उपयोग पर प्रतिबंध", "KRCUPRO की पूर्व लिखित सहमति के बिना इस सॉफ़्टवेयर की प्रतिलिपि बनाना, मिरर करना, संशोधित करना या व्यावसायिक उपयोग करना सख्त वर्जित है।"),
            ("2. अधिकारों का आरक्षण", "इस सॉफ़्टवेयर से जुड़े सभी कॉपीराइट, ट्रेडमार्क, पेटेंट और बौद्धिक संपदा अधिकार पूरी तरह से KRCUPRO के पास सुरक्षित हैं।"),
            ("3. तृतीय-पक्ष नोटिस", "शामिल किए गए सभी ओपन-सोर्स घटक अपने मूल लाइसेंस को पूर्ण रूप से बनाए रखते हैं (NOTICE फ़ाइल देखें)।"),
            ("4. वारंटी का अस्वीकरण", "यह सॉफ़्टवेयर 'जैसा है' (AS IS) बिना किसी वारंटी के प्रदान किया जाता है। इसके उपयोग से होने वाले किसी भी नुकसान के लिए कॉपीराइट धारक उत्तरदायी नहीं होगा।")
        ]
    },
    "id": {
        "title": "⚖️ Lisensi Perangkat Lunak Kepemilikan (LICENSE)",
        "desc": "Teks resmi lisensi perangkat lunak eksklusif D4UC dan ringkasan hukum dalam Bahasa Indonesia",
        "official_label": "Teks Hukum Resmi (Bahasa Inggris)",
        "summary_title": "Ringkasan Ketentuan Hukum Utama Lisensi",
        "clauses": [
            ("1. Pembatasan Penggunaan", "Dilarang keras menyalin, mereplikasi, memodifikasi, mendistribusikan ulang, atau menggunakan perangkat lunak ini untuk kepentingan komersial tanpa izin tertulis dari KRCUPRO."),
            ("2. Hak Cipta & Kekayaan Intelektual", "Seluruh hak cipta, merek dagang, paten, dan rahasia dagang sepenuhnya menjadi hak eksklusif KRCUPRO."),
            ("3. Pemberitahuan Pihak Ketiga", "Seluruh komponen sumber terbuka pihak ketiga yang disematkan tetap tunduk pada ketentuan lisensi aslinya masing-masing (lihat berkas NOTICE)."),
            ("4. Pelepasan Tanggung Jawab (Disclaimer)", "Perangkat lunak ini disediakan 'SEBAGAIMANA ADANYA' (AS IS) tanpa jaminan apa pun, baik tersurat maupun tersirat.")
        ]
    }
}
