# src/ui/i18n.py
from typing import Dict, Any

STRINGS: Dict[str, Dict[str, str]] = {
    "ko": {
        # App Header
        "app_title": "⚡ D4UC 체커 V2",
        "app_subtitle": "Discord 고속 스텔스 사용자명 검사기",
        "lang_switch": "🌐 Language: 한국어",
        "help_btn": "📖 도움말 / 사용법",
        "btn_settings": "⚙️ 프록시 / 계정 설정",
        "btn_settings_tooltip": "Surfshark WireGuard 키, 계정 자격 증명, 프록시 포트 및 안정화 웜업 지연 시간을 직접 수정합니다.",

        # Quick Guide Banner (Onboarding)
        "guide_banner_title": "💡 프로그램 목적 및 3단계 빠른 사용 순서 (Quick Guide)",
        "guide_banner_hide": "접기 ▲",
        "guide_banner_show": "사용법 펼치기 ▼",
        "guide_banner_content": "• [목적] Discord 희귀 고유 닉네임(3~6자)을 Chrome131 TLS 스텔스 위장과 유저스페이스 격리 프록시로 안전하게 탐색하고 선점합니다.\n• [1단계] 모드 & 글자수 선택: 창을 2~4개 띄워 2~4배 가속하려면 '전수순열(Permutation)'의 다중 창 분할을 선택하세요.\n• [2단계] 프록시 & 워커 수 확인: Surfshark 격리 터널 권장 (워커 3~5개 권장, 각 워커마다 전용 해외 IP 배정).\n• [3단계] '검사 시작' 클릭: 발견 즉시 아래 표에 실시간 기록되며, 'Discord 가입 창 열기' 버튼으로 즉시 선점하세요!",

        # Sidebar Controls
        "target_mode": "탐색 모드",
        "target_mode_tooltip": "생성할 사용자명 알고리즘을 선택합니다.\n• Hybrid: 사전 단어, 대칭 패턴, 숫자, 커스텀 마스크를 고르게 섞어 고가치 닉네임 탐색\n• Custom Mask: 앞 글자, 뒤 글자, 중간 점(.)을 직접 지정하여 정밀 탐색\n• Dictionary: 영어 단어 및 발음하기 쉬운 CVCV 음절 조합\n• Pattern: AAAA, ABAB, 12345 등 대칭/반복 패턴\n• Numeric: 0~9 순수 숫자 및 연속/대칭 숫자닉 (00000~99999)\n• Permutation: 지정된 문자셋의 모든 가능한 순열 전수조사\n• Random: 무작위 영숫자 조합",
        
        "length_title": "글자수 (Length)",
        "length_tooltip": "탐색할 닉네임의 길이(3~6자)를 지정합니다.\n• 3자: 극도로 희귀하며 선점 가치가 가장 높음\n• 4자: 전통적인 D4U 체커 표준 길이\n• 5~6자: 실제 단어 및 의미 있는 닉네임 발견 확률 높음",

        # Custom Pattern & Dynamic Mode Controls
        "custom_pattern_title": "🎯 커스텀 패턴 세부 설정",
        "mode_title_hybrid": "⚡ 하이브리드 복합 탐색 설정",
        "mode_badge_hybrid": "● 스마트 복합 분산",
        "mode_desc_hybrid": "사전(40%) + 패턴(30%) + 숫자(20%) + 무작위(10%)를 결합하여 고가치 닉네임을 효율적으로 탐색합니다.",

        "mode_title_custom": "🎯 커스텀 패턴 세부 설정",
        "mode_badge_custom": "● 마스크/패턴 필터",
        "mode_desc_custom": "앞/뒤 글자, 중간 점, 마스크를 지정하여 원하는 조건의 닉네임만 정밀 탐색합니다.",

        "mode_title_dict": "📖 사전 및 발음형 음절 설정",
        "mode_badge_dict": "● 발음형 음절/사전",
        "mode_desc_dict": "CVCV(자음+모음) 발음 가능한 자연스러운 단어 및 실제 영문 사전 어휘 기반으로 탐색합니다.",

        "mode_title_pattern": "✨ 대칭 및 패턴 세부 설정",
        "mode_badge_pattern": "● 시각적 대칭/반복",
        "mode_desc_pattern": "ABBA(대칭), AABB(더블), ABAB(교차), AAAB(트리플) 등 시각적 패턴을 탐색합니다.",

        "mode_title_numeric": "🔢 숫자 닉네임 세부 설정",
        "mode_badge_numeric": "● 0~9 순수 숫자 전용",
        "mode_desc_numeric": "순수 아라비아 숫자(0~9)로만 구성된 초희귀 레어 숫자 닉네임을 집중 탐색합니다.",

        "mode_title_perm": "🔤 순차 전수순열 설정",
        "mode_badge_perm": "● 100% 누락 없는 전수 검사",
        "mode_desc_perm": "a~z, 0~9 문자셋 순열을 순차적으로 탐색하여 단 1개의 닉네임도 빠짐없이 전수 조사합니다.",

        "mode_title_comb": "🔐 영숫자 전수조사 (비번형 조합 0~z)",
        "mode_badge_comb": "● 0~9 + a~z 진법 순차 전수",
        "mode_desc_comb": "0~9와 a~z를 결합한 전수조사 조합 엔진입니다. 오름차순(0000 ➔ zzzz) 또는 내림차순(zzzz ➔ 0000)으로 단 하나의 닉네임도 빠짐없이 순차 탐색합니다.",
        "comb_direction_label": "탐색 순서 (Direction):",
        "comb_direction_asc": "오름차순 (0000 ➔ zzzz)",
        "comb_direction_desc": "내림차순 (zzzz ➔ 0000)",
        "comb_direction_tooltip": "조합 탐색 방향을 설정합니다.\n• 오름차순: 0000부터 시작하여 0001, ..., 000a, ..., zzzz 순서로 전진 탐색\n• 내림차순: zzzz부터 시작하여 zzzy, ..., 0000 순서로 후진 탐색",
        "comb_charset_label": "문자셋 우선순위:",
        "comb_charset_num_first": "숫자 우선 (0-9 ➔ a-z)",
        "comb_charset_alpha_first": "영문 우선 (a-z ➔ 0-9)",
        "comb_charset_tooltip": "진법 인덱싱 시 어떤 문자를 앞 순위로 둘지 결정합니다.\n• 숫자 우선: 0~9 뒤에 a~z 배치 (00, 01, ..., 09, 0a, ..., zz)\n• 영문 우선: a~z 뒤에 0~9 배치 (aa, ab, ..., az, a0, ..., 99)",

        "mode_title_random": "🎲 무작위 난수 설정",
        "mode_badge_random": "● 영숫자 고속 난수",
        "mode_desc_random": "a~z, 0~9 문자셋 기반의 최대 엔트로피 고속 난수 닉네임을 생성합니다.",

        "prefix_label": "앞 글자 (Prefix):",
        "prefix_placeholder": "예: kr, 7, vip, 또는 비워둠",
        "prefix_tooltip": "닉네임 맨 앞에 올 고정 문자열을 지정합니다 (예: 'kr', '7', 'vip').",
        "suffix_label": "뒤 글자 (Suffix):",
        "suffix_placeholder": "예: 99, x, kr, 또는 비워둠",
        "suffix_tooltip": "닉네임 맨 뒤에 올 고정 문자열을 지정합니다 (예: '99', 'x', 'kr').",
        "middle_dot_label": "중간 dot (.) 여부:",
        "middle_dot_none": "점 미포함 (None)",
        "middle_dot_opt": "점 허용/선택 (Optional)",
        "middle_dot_req": "중간 점 필수 1개 (Required)",
        "middle_dot_tooltip": "Discord 규정 준수 중간 점(.) 옵션입니다.\n• Discord 규칙: 시작/끝 점 불가, 연속 점(..) 불가\n• '필수 1개' 선택 시 a.bc, ab.cd 등 중간에 점 1개가 반드시 포함됩니다.",
        "custom_mask_label": "직접 마스크 입력 (선택):",
        "custom_mask_placeholder": "예: ??.?? 또는 kr?.?? 또는 a.???",
        "custom_mask_tooltip": "직접 패턴 마스크를 지정합니다.\n• ? = 영숫자 [a-z0-9]\n• @ = 영문자 [a-z]\n• # = 숫자 [0-9]\n• . = 점\n• 일반 문자 = 고정 문자 (예: kr?.??, ??.ab)",

        "proxy_title": "프록시 인프라",
        "proxy_tooltip": "Discord API 호출에 사용할 네트워크 프록시 엔진을 선택합니다.\n• Surfshark: 유저스페이스 wireproxy 터널(127.0.0.1:1081). 호스트 PC 인터넷에 일체 영향 없음\n• 무료 프록시: GitHub/HuggingFace 공개 프록시 목록 자동 수집 및 실시간 Discord 연결성 검증\n• File Pool: proxies.txt 파일에 기재된 프록시 목록 사용\n• ThorData: 상용 로테이팅 프록시 연동\n• Direct: 프록시 없이 현재 PC 공인 IP로 직접 검사",
        "proxy_opt_free": "🌐 무료 프록시 자동 수집 (Free Public)",
        "btn_scrape_free": "🔄 무료 프록시 수집 & 검증",
        "free_proxy_badge_zero": "가용: 0개 검증됨",

        "country_title": "선호 국가 (Surfshark)",
        "country_tooltip": "Surfshark 경유 시 우선적으로 연결할 국가 클러스터를 지정합니다.\n• 한국/일본/싱가포르: 아시아 권역으로 지연시간(Latency)이 가장 낮음\n• 미국/유럽: 대규모 IP 풀을 활용할 때 적합\n• 전세계 142개: 레이트리밋 발생 시 모든 글로벌 노드로 무한 순환",

        "concurrency_title": "동시 비동기 워커 수",
        "concurrency_tooltip": "동시에 검사를 수행할 비동기(asyncio) 워커 개수입니다 (1~50개).\n• 1~8개 (안정): 429 쿨다운 빈도가 가장 낮고 안정적\n• 9~20개 (고속): 초당 5~15회 고속 검사 (권장)\n• 21~50개 (터보): 초고속 병렬 검사 (Surfshark 글로벌 IP 순환과 결합 시 최고 효율)",

        "webhook_title": "Discord Webhook 알림 URL",
        "webhook_placeholder": "https://discord.com/api/webhooks/...",
        "webhook_tooltip": "희귀 닉네임이 발견되었을 때 실시간 임베드 알림을 수신할 Discord 채널의 웹훅 URL을 입력합니다.\n• 비워두면 웹훅 알림을 보내지 않고 로컬 화면 및 DB에만 저장됩니다.",

        "btn_start": "🚀 검사 시작 (Start)",
        "btn_stop": "⏹️ 검사 중지 (Stop)",
        "btn_toggle_tooltip": "비동기 검사 루프를 시작하거나 안전하게 중지합니다.\n• 시작 시 프록시 사전 실사 검증 및 웜업 지연을 거쳐 안전하게 가동됩니다.\n• 중지 시 현재 진행 중인 요청을 안전하게 마무리하고 리소스를 정상 해제합니다.",

        # Top Bar
        "status_idle": "● 대기 중 (IDLE)",
        "status_running": "● 실시간 검사 중 (RUNNING)",
        "status_stopping": "● 안전 종료 중 (STOPPING...)",
        "proxy_badge": "🛡️ Surfshark 다중 터널 풀",

        # KPI Cards
        "kpi_total": "총 검사수",
        "kpi_rps": "RPS (속도)",
        "kpi_avail": "✅ 사용 가능",
        "kpi_taken": "❌ 사용 중",
        "kpi_429": "⚠️ 429 쿨다운",
        "kpi_skipped": "⏩ 건너뜀",

        # Skip Toggle
        "chk_skip_already": "이미 검사된 닉네임 자동 건너뛰기",
        "chk_skip_already_tooltip": "DB 및 텍스트 파일(available.txt, taken.txt)에 저장된 과거 검사 닉네임을 중복 없이 100% 자동 건너뜁니다.",
        "custom_box_badge_active": "● 활성 (패턴 모드)",
        "custom_box_badge_inactive": "○ 대기 (기본 모드)",
        "btn_custom_reset": "초기화",
        "btn_custom_reset_tooltip": "커스텀 패턴 입력을 모두 비우고 기본 모드로 복원합니다.",
        "preview_title": "💡 실시간 생성 미리보기 (Preview)",
        "custom_preview_idle": "패턴 미지정: 상단 탐색 모드로 동작합니다.",
        "custom_preview_paused": "⚠️ 상단에서 다른 모드가 선택되어 대기 중입니다.",
        "auto_save_indicator": "💾 실시간 자동 저장 (.txt / .csv / .json): {count}개",
        "btn_open_folder": "📂 저장 폴더 열기",
        "btn_open_folder_tooltip": "실시간 자동 저장된 파일(available_usernames.txt, csv, json)이 위치한 폴더를 윈도우 탐색기로 엽니다.",
        "btn_load_history": "📂 이전 발견/파일 불러오기",
        "btn_load_history_tooltip": "기존에 발견해 둔 닉네임 목록이나 외부 .txt, .csv, .json 파일을 불러와 화면에 복원하고 재확인 큐에 등록합니다.",
        "recheck_title": "🔄 기존 닉네임 전용 재확인(Re-check) 설정",
        "recheck_badge": "● 재확인 모드",
        "recheck_range_label": "분할 검사 범위 (청크/나눠서 작업):",
        "recheck_range_all": "전체 닉네임 재확인 (All)",
        "recheck_range_1_50": "1 ~ 50번 닉네임 (Part 1)",
        "recheck_range_51_100": "51 ~ 100번 닉네임 (Part 2)",
        "recheck_range_101_200": "101 ~ 200번 닉네임 (Part 3)",
        "recheck_range_custom": "선택한 항목만 재확인",
        "recheck_completed_msg": "재확인 검사 완료: 총 {total}개 중 유효 {valid}개, 사용 중(TAKEN) {taken}개",

        # Discovered Table
        "table_title": "🎉 발견된 사용 가능 닉네임 (LIVE)",
        "btn_open_reg": "Discord 가입 창 열기",
        "btn_open_reg_tooltip": "기본 웹 브라우저로 Discord 공식 회원가입 페이지(https://discord.com/register)를 즉시 엽니다.\n발견된 희귀 닉네임을 빠르게 계정에 등록할 때 사용하세요.",
        "btn_export_avail": "💾 결과 내보내기 (Export)",
        "btn_export_tooltip": "발견된 희귀 닉네임 목록을 .txt, .csv, .json 외부 파일로 저장합니다.",
        "col_time": "발견 시각",
        "col_username": "사용자명 (Username)",
        "col_pattern": "패턴 유형",
        "col_latency": "지연 시간",
        "col_server": "경유 서버 (Surfshark)",

        # Context Menu
        "ctx_recheck_selected": "🔄 선택한 닉네임 지금 바로 재확인",
        "ctx_recheck_all": "🔄 전체 목록 지금 바로 재확인",
        "ctx_copy_username": "📋 선택한 닉네임 복사",
        "ctx_copy_all": "📋 전체 닉네임 목록 복사",
        "ctx_export_file": "💾 외부 파일로 저장...",
        "ctx_open_discord": "🚀 Discord 회원가입 페이지 열기",
        "no_usernames_to_export": "내보낼 사용 가능한 닉네임이 아직 없습니다.",
        "export_success_msg": "닉네임 {count}개가 성공적으로 저장되었습니다:\n{path}",

        # Search & Filter Bar
        "search_placeholder": "🔍 닉네임 검색 (예: vip, .kr, 777, a*b)...",
        "search_tooltip": "발견된 닉네임 목록에서 실시간으로 검색합니다.\n• 부분 일치 (예: vip, kr)\n• 와일드카드 지원 (예: vip*, *kr, a*b, ??.vip)\n• 점(.) 포함 검색 지원",
        "btn_clear_search_tooltip": "검색어를 지우고 전체 목록을 표시합니다.",
        "btn_reset_filters_tooltip": "모든 검색 필터(글자수, 유형, 정렬)를 기본값으로 초기화합니다.",
        "filter_len_all": "글자수: 전체",
        "filter_len_3": "3글자",
        "filter_len_4": "4글자",
        "filter_len_5": "5글자",
        "filter_len_6p": "6글자+",
        "filter_len_tooltip": "특정 글자수의 닉네임만 필터링합니다.",
        "filter_type_all": "유형: 전체",
        "filter_type_dict": "사전/단어",
        "filter_type_patt": "대칭/패턴",
        "filter_type_num": "순수 숫자닉",
        "filter_type_dot": "점(.) 포함",
        "filter_type_comb": "조합(0~z)",
        "filter_type_custom": "커스텀 마스크",
        "filter_type_tooltip": "특정 생성 알고리즘 또는 패턴 유형만 필터링합니다.",
        "filter_sort_latest": "정렬: 최신순",
        "filter_sort_alpha_asc": "닉네임 (A-Z)",
        "filter_sort_alpha_desc": "닉네임 (Z-A)",
        "filter_sort_latency_fast": "지연시간 (빠른순)",
        "filter_sort_tooltip": "테이블 항목의 정렬 순서를 변경합니다.",
        "export_filter_dialog_title": "내보내기 범위 선택",
        "export_filter_dialog_msg": "현재 필터가 적용되어 있습니다.\n\n표시 항목: {filtered}개 / 전체 항목: {total}개\n\n[예 (Yes)]: 현재 필터링된 {filtered}개만 내보내기\n[아니오 (No)]: 전체 {total}개 모두 내보내기",

        # Status Bar & Progress
        "status_bar_idle": "대기 상태: 설정을 확인한 후 [검사 시작] 버튼을 누르세요.",
        "status_bar_running": "스텔스 검사 가동 중 | 워커: {workers}개 활성 | 가동 시간: {elapsed}",
        "status_bar_stopping": "검사 루프를 중지하고 리소스를 안전하게 정리하고 있습니다...",

        # Log Console & Filters
        "log_title": "실시간 실행 및 이벤트 로그",
        "log_filter_worker": "워커별 상세",
        "log_filter_worker_tooltip": "각 워커가 검사하는 개별 닉네임과 결과(성공/사용중/지연시간)를 실시간 출력합니다.",
        "log_filter_success": "발견/성공",
        "log_filter_success_tooltip": "발견된 희귀 닉네임 알림을 표시합니다.",
        "log_filter_proxy": "429 & IP회전",
        "log_filter_proxy_tooltip": "Discord 429 쿨다운 및 Surfshark IP 자동 순환 상태를 표시합니다.",
        "log_filter_system": "시스템/오류",
        "log_filter_system_tooltip": "프로그램 초기화, DB 저장, 경고 및 에러를 표시합니다.",
        "log_worker_select": "워커 선택:",
        "all_workers": "전체 워커",
        "btn_clear_log": "🗑️ 로그 지우기",
        "btn_clear_log_tooltip": "현재 화면에 표시된 모든 로그 텍스트를 초기화합니다.",
        "btn_save_log": "💾 로그 저장 (.log)",
        "btn_save_log_tooltip": "지금까지의 전체 실행 로그를 로컬 텍스트 파일(.log)로 저장합니다.",
        "btn_collapse_log": "🔽 로그창 접기",
        "btn_expand_log": "🔼 로그창 펼치기",
        "btn_toggle_log_tooltip": "로그 콘솔 영역을 접어 닉네임 테이블을 넓게 보거나 다시 펼칩니다.",
        "log_saved_msg": "로그 파일이 성공적으로 저장되었습니다:\n{path}",

        # Settings Modal
        "settings_modal_title": "⚙️ 프록시 인프라 & Surfshark 계정 설정",
        "sett_wg_key": "WireGuard 개인키 (단일 또는 줄바꿈/쉼표 구분으로 다중 계정 등록):",
        "sett_wg_key_tooltip": "2개 이상의 계정 키를 줄바꿈이나 쉼표로 등록하면 워커들에 계정이 균등하게 분산 배정(Round-Robin)되어 처리량과 레이트리밋 한도가 대폭 증가합니다.",
        "sett_wg_key_count": "현재 등록된 Surfshark 계정 키: {count}개",
        "sett_btn_open_surfshark": "🌐 새 격리 브라우저로 서프샤크 키 발급창 열기 (다중 계정 로그인)",
        "sett_btn_open_surfshark_tooltip": "새로운 독립 브라우저 프로필을 화면에 즉시 팝업하여 두 번째 계정 로그인 및 WireGuard 수동 키 발급 페이지로 이동합니다.",
        "sett_ovpn_user": "Surfshark OpenVPN 사용자명 (Username):",
        "sett_ovpn_pass": "Surfshark OpenVPN 비밀번호 (Password):",
        "sett_http_port": "로컬 HTTP 프록시 포트 (기본 1081):",
        "sett_socks5_port": "로컬 SOCKS5 프록시 포트 (기본 1080):",
        "sett_warmup_delay": "터널 실사 검증 후 웜업 지연 시간 (초/sec, 기본 1.0초):",
        "sett_warmup_tooltip": "프록시 공인 IP 검증이 완료된 후 워커를 투입하기 전 대기할 지연 시간입니다. 호스트 IP 노출 위험을 0%로 완벽 차단합니다.",
        "sett_btn_save": "💾 설정 저장 및 즉시 적용",
        "sett_btn_reset": "🔄 기본값 복원",
        "sett_btn_cancel": "닫기 (Cancel)",
        "sett_saved_msg": "프록시 및 계정 설정이 성공적으로 저장 및 적용되었습니다.",

        # Sharding & Multi-Window
        "perm_shard_title": "다중 창 분할(샤딩)",
        "perm_shard_tooltip": "여러 프로그램을 동시에 띄워 전수검사할 때 창 1에는 '1번 창', 창 2에는 '2번 창'을 설정하면 닉네임이 단 1개도 겹치지 않고 2배~4배 속도로 분할 완료합니다.",
        "perm_custom_range_title": "직접 글자 범위 지정",
        "perm_custom_range_tooltip": "검사할 첫 글자의 시작(Start)과 끝(End) 범위를 직접 지정합니다. (예: a ~ c, 0 ~ 9)",
        "perm_start_char_tooltip": "검사를 시작할 첫 글자 (a-z, 0-9, _)",
        "perm_end_char_tooltip": "검사를 종료할 마지막 첫 글자 (a-z, 0-9, _)",

        # Help Modal
        "help_modal_title": "📖 Discord 체커 V2 사용 방법 및 기능 가이드",
        "help_modal_content": """
[ 프로그램 개요 및 목적 ]
본 프로그램은 Discord 고유 사용자명(Unique Username) 체계에서 3~6글자의 희귀한 닉네임(사전 단어, 대칭 패턴, 앞/뒤 글자 지정, 중간 점 레어닉 등)을 탐색하고 선점할 수 있도록 제작된 고속 스텔스 검사기입니다.
최신 Chrome 브라우저의 TLS 핑거프린트(JA3/JA4)를 위장하여 Cloudflare 및 Discord WAF 차단을 방지하며, 유저스페이스 wireproxy 터널을 통해 호스트 PC의 일반 인터넷 통신에 일체 영향 없이 안전하게 동작합니다.

[ 🚀 다중 창 분할(샤딩) 2배~4배 초고속 가속 가이드 ]
본 프로그램은 여러 개의 창을 동시에 띄워 전수검사를 병렬로 분할 실행할 수 있습니다.
SQLite WAL 데이터베이스와 실시간 연동되어 여러 창이 동시에 돌아도 닉네임 중복 검사 0%, 발견 즉시 모든 창에 실시간 동기화됩니다!

1. [창 2개로 2배 빠르게 돌리기]:
   - 1번 창: 모드를 '전수순열 (Permutation)' 선택 -> 다중 창 분할에서 '2분할 - [1번 창: a ~ m]' 선택 후 [검사 시작]
   - 2번 창: 프로그램을 한 번 더 실행 -> '2분할 - [2번 창: n ~ _]' 선택 후 [검사 시작]
   - 효과: 1번 창은 a~m 시작 닉네임을, 2번 창은 n~_ 시작 닉네임을 전담하므로 단 1개도 겹치지 않고 정확히 2배 속도로 완료됩니다!

2. [창 3개로 3배 빠르게 돌리기]:
   - 1번 창: '3분할 - [1번 창: a ~ i]'
   - 2번 창: '3분할 - [2번 창: j ~ r]'
   - 3번 창: '3분할 - [3번 창: s ~ _]'

3. [창 4개로 4배 빠르게 돌리기]:
   - 1번 창: '4분할 - [1번 창: a ~ g]'
   - 2번 창: '4분할 - [2번 창: h ~ n]'
   - 3번 창: '4분할 - [3번 창: o ~ u]'
   - 4번 창: '4분할 - [4번 창: v ~ _]'

4. [직접 글자 범위 지정]:
   - 특정 글자로 시작하는 닉네임만 집중 탐색하고 싶을 때(예: 숫자 0~9로 시작하는 닉네임), 시작 글자와 끝 글자를 직접 지정할 수 있습니다.

[ 💡 초보자 3단계 초고속 시작 가이드 ]
1단계: [모드 선택]
   - 원하는 탐색 방식(사전 단어, 대칭 패턴, 커스텀 마스크, 전수순열 등)과 글자수(3~6자)를 선택합니다.
2단계: [인프라 확인]
   - 'Surfshark (격리 프록시)'를 권장합니다. 다른 PC 작업창에 VPN 영향 없이 오직 체커만 안전하게 우회됩니다.
   - 동시 워커 수는 3~5개를 권장합니다. (워커별로 서로 다른 국가 IP가 1:1 자동 배정됩니다)
3단계: [검사 시작 & 선점]
   - '검사 시작' 버튼을 누르면 프록시 실사 검증 후 실시간 프로그레스 바가 동작하며 안전하게 검사가 진행됩니다.
   - 사용 가능한 희귀 닉네임이 발견되면 중앙 테이블에 즉시 표시되며, 상단 'Discord 가입 창 열기' 버튼을 눌러 즉시 선점하세요!

[ 🛠️ 주요 편의 기능 ]
1. [실시간 로그 제어]:
   - [🗑️ 로그 지우기]: 로그 화면을 깨끗이 비웁니다.
   - [💾 로그 파일 저장]: 현재까지의 실행 로그를 .txt/.log 파일로 저장합니다.
   - [▣ 로그창 접기/펼치기]: 로그 창을 접어 발견된 닉네임 표를 넓게 보거나 다시 펼칠 수 있습니다.
2. [결과 외부 내보내기 (Export)]:
   - 발견된 사용 가능 닉네임 테이블 상단의 '💾 결과 내보내기' 버튼을 통해 .txt, .csv, .json 형식으로 손쉽게 파일 저장할 수 있습니다.
3. [Windows 방화벽 무경고 자동 등록]:
   - wireproxy.exe 바이너리가 고정된 로컬 경로에 상주하며 Windows Defender Firewall에 영구 허용 규칙으로 자동 등록되어 방화벽 경고창이 뜨지 않습니다.
""",
        "help_close": "닫기 (Close)"
    },

    "en": {
        # App Header
        "app_title": "⚡ D4UC Checker V2",
        "app_subtitle": "Discord Fast Stealth Username Checker",
        "lang_switch": "🌐 Language: English",
        "help_btn": "📖 Help / User Guide",
        "btn_settings": "⚙️ Proxy / Account Settings",
        "btn_settings_tooltip": "Configure Surfshark WireGuard keys, account credentials, proxy ports, and warm-up delay.",

        # Quick Guide Banner (Onboarding)
        "guide_banner_title": "💡 Program Purpose & 3-Step Quick Guide",
        "guide_banner_hide": "Hide ▲",
        "guide_banner_show": "Expand Guide ▼",
        "guide_banner_content": "• [Purpose] Fast stealth checker for 3-to-6 char Discord Unique Usernames using Chrome131 TLS and userspace isolated proxies.\n• [Step 1] Select Mode & Length: For 2x~4x multi-window speedup, select 'Permutation' and choose a window shard.\n• [Step 2] Verify Proxy & Workers: Surfshark isolated tunnel is recommended (3~5 workers with 1:1 dedicated country IPs).\n• [Step 3] Click 'Start Checking': Available usernames pop up in real-time. Click 'Open Discord Registration' to claim immediately!",

        # Sidebar Controls
        "target_mode": "Target Mode",
        "target_mode_tooltip": "Select username generation algorithm:\n• Hybrid: Balanced mix of dictionary words, patterns, digits & custom masks\n• Custom Mask: Target specific prefix, suffix, and middle dot (.) arrangements\n• Dictionary: Curated English words & pronounceable CVCV syllables\n• Pattern: Symmetrical & repeating patterns (AAAA, ABAB, 12345)\n• Numeric: Pure 0-9 digits and numeric patterns (00000-99999)\n• Permutation: Exhaustive combinatorial permutation\n• Random: Pure random alphanumeric strings",

        "length_title": "Length",
        "length_tooltip": "Set target username length (3-6 chars):\n• 3 chars: Ultra rare & highest value\n• 4 chars: Traditional D4U checker standard\n• 5-6 chars: High chance of real words & readable names",

        # Custom Pattern & Dynamic Mode Controls
        "custom_pattern_title": "🎯 Custom Pattern Settings",
        "mode_title_hybrid": "⚡ Hybrid Composite Mode",
        "mode_badge_hybrid": "● Smart Composite",
        "mode_desc_hybrid": "Combines Dictionary (40%), Pattern (30%), Numeric (20%), and Random (10%) for optimal efficiency.",

        "mode_title_custom": "🎯 Custom Pattern Settings",
        "mode_badge_custom": "● Custom Mask Active",
        "mode_desc_custom": "Filter and target usernames by specifying prefix, suffix, middle dot, or direct wildcard masks.",

        "mode_title_dict": "📖 Dictionary & Phonetics Mode",
        "mode_badge_dict": "● Pronounceable / Words",
        "mode_desc_dict": "Generates natural CVCV pronounceable syllables and genuine English dictionary words.",

        "mode_title_pattern": "✨ Pattern & Symmetry Mode",
        "mode_badge_pattern": "● Symmetry & Repetition",
        "mode_desc_pattern": "Searches for visually rare patterns: ABBA (symmetry), AABB (doubles), ABAB (alternating), and AAAB.",

        "mode_title_numeric": "🔢 Pure Numeric Mode (0-9)",
        "mode_badge_numeric": "● 0-9 Digits Only",
        "mode_desc_numeric": "Exclusively targets ultra-rare pure Arabic numeral usernames (0000-99999).",

        "mode_title_perm": "🔤 Sequential Permutation Mode",
        "mode_badge_perm": "● 100% Exhaustive Scan",
        "mode_desc_perm": "Sequentially checks all combinations of a-z and 0-9 to ensure zero missed usernames.",

        "mode_title_comb": "🔐 Alphanumeric Combinatorial (0-z Brute-force)",
        "mode_badge_comb": "● 0-9 & a-z Base-36 Scan",
        "mode_desc_comb": "Exhaustive combinatorial generator combining digits (0-9) and letters (a-z). Sequentially sweeps all combinations in Ascending (0000 ➔ zzzz) or Descending (zzzz ➔ 0000) order.",
        "comb_direction_label": "Scan Direction:",
        "comb_direction_asc": "Ascending (0000 ➔ zzzz)",
        "comb_direction_desc": "Descending (zzzz ➔ 0000)",
        "comb_direction_tooltip": "Search direction for combinations:\n• Ascending: Starts from 0000 forward to zzzz (0000, 0001, ..., 000a, ..., zzzz)\n• Descending: Starts from zzzz backward to 0000 (zzzz, zzzy, ..., 0000)",
        "comb_charset_label": "Charset Priority:",
        "comb_charset_num_first": "Digits First (0-9 ➔ a-z)",
        "comb_charset_alpha_first": "Letters First (a-z ➔ 0-9)",
        "comb_charset_tooltip": "Character order for radix conversion:\n• Digits First: 0-9 followed by a-z (00..09, 0a..zz)\n• Letters First: a-z followed by 0-9 (aa..az, a0..99)",

        "mode_title_random": "🎲 High-Entropy Random Mode",
        "mode_badge_random": "● Pure Alphanumeric",
        "mode_desc_random": "Generates high-speed, maximum-entropy pseudo-random alphanumeric usernames.",

        "prefix_label": "Prefix:",
        "prefix_placeholder": "e.g. kr, 7, vip, or leave empty",
        "prefix_tooltip": "Fixed string at the beginning of the username (e.g. 'kr', '7', 'vip').",
        "suffix_label": "Suffix:",
        "suffix_placeholder": "e.g. 99, x, kr, or leave empty",
        "suffix_tooltip": "Fixed string at the end of the username (e.g. '99', 'x', 'kr').",
        "middle_dot_label": "Middle Dot (.) Option:",
        "middle_dot_none": "No Dot (None)",
        "middle_dot_opt": "Optional Dot",
        "middle_dot_req": "Required Middle Dot (1 Dot)",
        "middle_dot_tooltip": "Discord username rules for dot (.):\n• No leading/trailing dot, no consecutive dots (..)\n• When 'Required' is selected, a single dot is guaranteed strictly between characters (e.g. a.bc, ab.cd).",
        "custom_mask_label": "Direct Mask (Optional):",
        "custom_mask_placeholder": "e.g. ??.?? or kr?.?? or a.???",
        "custom_mask_tooltip": "Custom mask pattern:\n• ? = alphanumeric [a-z0-9]\n• @ = letters [a-z]\n• # = digits [0-9]\n• . = dot\n• Other characters = fixed literals (e.g. kr?.??, ??.ab)",

        "proxy_title": "Proxy Infrastructure",
        "proxy_tooltip": "Select network proxy infrastructure for Discord API requests:\n• Surfshark: Userspace wireproxy tunnel (127.0.0.1:1081). 0% host impact\n• Free Public: Auto-scrape GitHub & HuggingFace public proxy lists and verify live Discord connectivity\n• File Pool: Load proxies from proxies.txt\n• ThorData: Commercial rotating proxy provider\n• Direct: Direct connection using your current public IP",
        "proxy_opt_free": "🌐 Free Public Proxies (Auto Scrape)",
        "btn_scrape_free": "🔄 Scrape & Verify Free Proxies",
        "free_proxy_badge_zero": "Active: 0 Verified",

        "country_title": "Preferred Country (Surfshark)",
        "country_tooltip": "Preferred country clusters for Surfshark WireGuard:\n• KR/JP/SG: Lowest latency for Asian region\n• US/EU: Large IP pools\n• All 142: Infinite global rotation on rate limits",

        "concurrency_title": "Concurrent Workers",
        "concurrency_tooltip": "Number of concurrent asyncio workers (1~50):\n• 1~8 Workers (Safe): Lowest 429 rate limit risk, most stable\n• 9~20 Workers (Fast): 5~15 RPS high-speed checking (Recommended)\n• 21~50 Workers (Turbo): Ultra-high parallel throughput (Peak performance with Surfshark IP rotation)",

        "webhook_title": "Discord Webhook Alert URL",
        "webhook_placeholder": "https://discord.com/api/webhooks/...",
        "webhook_tooltip": "Discord Channel Webhook URL to receive instant alerts when an available username is discovered.\n• Leave empty to disable webhook notifications.",

        "btn_start": "🚀 Start Checking",
        "btn_stop": "⏹️ Stop Checking",
        "btn_toggle_tooltip": "Start or gracefully stop the asynchronous checking loop.\n• Start runs pre-flight proxy IP verification & warm-up delay before workers fire.\n• Stop safely finishes inflight checks and releases resources.",

        # Top Bar
        "status_idle": "● IDLE",
        "status_running": "● RUNNING (Stealth)",
        "status_stopping": "● STOPPING...",
        "proxy_badge": "🛡️ Surfshark Multi-Tunnel Pool",

        # KPI Cards
        "kpi_total": "Total Checked",
        "kpi_rps": "RPS (Speed)",
        "kpi_avail": "✅ Available",
        "kpi_taken": "❌ Taken",
        "kpi_429": "⚠️ 429 Cooldown",
        "kpi_skipped": "⏩ Skipped",

        # Skip Toggle
        "chk_skip_already": "Skip Already Checked Usernames",
        "chk_skip_already_tooltip": "Automatically skip usernames recorded in database or text files (available.txt, taken.txt).",
        "custom_box_badge_active": "● Active (Pattern Mode)",
        "custom_box_badge_inactive": "○ Idle (Default Mode)",
        "btn_custom_reset": "Reset",
        "btn_custom_reset_tooltip": "Clear all custom pattern inputs and restore default mode.",
        "preview_title": "💡 Live Preview & Template",
        "custom_preview_idle": "No pattern set: Default search mode active.",
        "custom_preview_paused": "⚠️ Another mode selected above; custom pattern paused.",
        "auto_save_indicator": "💾 Live Auto-Save (.txt / .csv / .json): {count}",
        "btn_open_folder": "📂 Open Results Folder",
        "btn_open_folder_tooltip": "Open the directory containing auto-saved files (available_usernames.txt, csv, json) in Windows Explorer.",
        "btn_load_history": "📂 Import / Restore History",
        "btn_load_history_tooltip": "Load previously discovered usernames or external .txt/.csv/.json files into the LIVE table and re-check queue.",
        "recheck_title": "🔄 Re-check Discovered Usernames Settings",
        "recheck_badge": "● Re-check Mode",
        "recheck_range_label": "Batch Split Range (Chunk Work):",
        "recheck_range_all": "All Usernames (All)",
        "recheck_range_1_50": "Usernames 1 ~ 50 (Part 1)",
        "recheck_range_51_100": "Usernames 51 ~ 100 (Part 2)",
        "recheck_range_101_200": "Usernames 101 ~ 200 (Part 3)",
        "recheck_range_custom": "Selected Items Only",
        "recheck_completed_msg": "Re-check Completed: {valid} AVAILABLE / {taken} TAKEN out of {total} checked.",

        # Discovered Table
        "table_title": "🎉 Discovered Available Usernames (LIVE)",
        "btn_open_reg": "Open Discord Register",
        "btn_open_reg_tooltip": "Opens Discord registration page in your default browser.\nUse this to instantly claim available usernames.",
        "btn_export_avail": "💾 Export Usernames",
        "btn_export_tooltip": "Export discovered available usernames to an external .txt, .csv, or .json file.",
        "col_time": "Time",
        "col_username": "Username",
        "col_pattern": "Pattern Type",
        "col_latency": "Latency",
        "col_server": "VPN Node (Surfshark)",

        # Context Menu
        "ctx_recheck_selected": "🔄 Re-check Selected Username Now",
        "ctx_recheck_all": "🔄 Re-check All Usernames Now",
        "ctx_copy_username": "📋 Copy Username",
        "ctx_copy_all": "📋 Copy All Usernames",
        "ctx_export_file": "💾 Export to File...",
        "ctx_open_discord": "🚀 Open Discord Registration",
        "no_usernames_to_export": "No available usernames discovered yet to export.",
        "export_success_msg": "Successfully exported {count} usernames to:\n{path}",

        # Search & Filter Bar
        "search_placeholder": "🔍 Search username (e.g. vip, .kr, 777, a*b)...",
        "search_tooltip": "Search discovered usernames in real time:\n• Substring matching (e.g. vip, kr)\n• Wildcards (*, ?) supported (e.g. vip*, *kr, a*b)\n• Dot (.) queries supported",
        "btn_clear_search_tooltip": "Clear search query and show all items.",
        "btn_reset_filters_tooltip": "Reset all search filters (length, pattern, sorting) to default.",
        "filter_len_all": "Length: All",
        "filter_len_3": "3 Chars",
        "filter_len_4": "4 Chars",
        "filter_len_5": "5 Chars",
        "filter_len_6p": "6+ Chars",
        "filter_len_tooltip": "Filter usernames by specific character length.",
        "filter_type_all": "Type: All",
        "filter_type_dict": "Dictionary",
        "filter_type_patt": "Pattern/Symmetry",
        "filter_type_num": "Pure Numeric",
        "filter_type_dot": "Contains Dot (.)",
        "filter_type_comb": "Combinatorial (0-z)",
        "filter_type_custom": "Custom Mask",
        "filter_type_tooltip": "Filter usernames by generation algorithm or pattern type.",
        "filter_sort_latest": "Sort: Latest",
        "filter_sort_alpha_asc": "Username (A-Z)",
        "filter_sort_alpha_desc": "Username (Z-A)",
        "filter_sort_latency_fast": "Latency (Fastest)",
        "filter_sort_tooltip": "Change sorting order of discovered usernames.",
        "export_filter_dialog_title": "Select Export Scope",
        "export_filter_dialog_msg": "A search filter is currently active.\n\nVisible: {filtered} / Total: {total}\n\n[Yes]: Export only {filtered} filtered items\n[No]: Export all {total} discovered items",

        # Status Bar & Progress
        "status_bar_idle": "Status: Ready. Review configuration and click [Start Checking].",
        "status_bar_running": "Stealth Check Running | Active Workers: {workers} | Uptime: {elapsed}",
        "status_bar_stopping": "Stopping workers and safely closing proxy tunnels...",

        # Log Console & Filters
        "log_title": "Real-time Execution & Event Log",
        "log_filter_worker": "Worker Details",
        "log_filter_worker_tooltip": "Displays real-time queries and results (success/taken/latency) for each worker.",
        "log_filter_success": "Hits/Success",
        "log_filter_success_tooltip": "Displays rare username discovery alerts.",
        "log_filter_proxy": "429 & Proxy",
        "log_filter_proxy_tooltip": "Displays Discord 429 rate limit cooldowns and Surfshark IP auto-rotation events.",
        "log_filter_system": "System/Errors",
        "log_filter_system_tooltip": "Displays initialization, DB persistence, warnings, and errors.",
        "log_worker_select": "Worker:",
        "all_workers": "All Workers",
        "btn_clear_log": "🗑️ Clear",
        "btn_save_log": "💾 Save Log (.log)",
        "btn_save_log_tooltip": "Saves entire execution log to a local timestamped .log file.",
        "btn_collapse_log": "🔽 Collapse Log",
        "btn_expand_log": "🔼 Expand Log",
        "btn_toggle_log_tooltip": "Toggle log console to maximize table view or view details.",
        "log_saved_msg": "Log file successfully saved to:\n{path}",

        # Settings Modal
        "settings_modal_title": "⚙️ Proxy Infrastructure & Surfshark Settings",
        "sett_wg_key": "WireGuard Private Key(s) (1 per line or comma-separated for Multi-Account):",
        "sett_wg_key_tooltip": "Registering 2+ account keys enables round-robin distribution across workers, multiplying rate-limit capacity.",
        "sett_wg_key_count": "Registered Surfshark Account Keys: {count}",
        "sett_btn_open_surfshark": "🌐 Open Surfshark in New Browser (Multi-Account Login & Key)",
        "sett_btn_open_surfshark_tooltip": "Immediately opens an isolated browser profile to log in to another account and generate WireGuard keys.",
        "sett_ovpn_user": "Surfshark OpenVPN Username:",
        "sett_ovpn_pass": "Surfshark OpenVPN Password:",
        "sett_http_port": "Local HTTP Proxy Port (Default 1081):",
        "sett_socks5_port": "Local SOCKS5 Proxy Port (Default 1080):",
        "sett_warmup_delay": "Pre-flight Verification Warm-up Delay (sec, default 1.0s):",
        "sett_warmup_tooltip": "Delay after verifying public proxy IP before launching workers. Ensures 100% host IP protection.",
        "sett_btn_save": "💾 Save & Apply",
        "sett_btn_reset": "🔄 Reset Defaults",
        "sett_btn_cancel": "Cancel",
        "sett_saved_msg": "Proxy and account credentials successfully updated and saved.",

        # Sharding & Multi-Window
        "perm_shard_title": "Multi-Window Sharding",
        "perm_shard_tooltip": "Divide permutation work across multiple windows (Window 1: 1st, Window 2: 2nd) for 0% duplicate checks and linear 2x~4x speedup.",
        "perm_custom_range_title": "Custom Letter Range",
        "perm_custom_range_tooltip": "Directly specify the start and end character range for the first letter of usernames (e.g. a ~ c, 0 ~ 9).",
        "perm_start_char_tooltip": "Starting first character (a-z, 0-9, _)",
        "perm_end_char_tooltip": "Ending first character (a-z, 0-9, _)",

        # Help Modal
        "help_modal_title": "📖 Discord Checker V2 User Guide & Documentation",
        "help_modal_content": """
[ Program Overview & Purpose ]
This tool is a high-speed stealth checker designed to discover and secure rare 3-to-6 character Discord Unique Usernames (dictionary words, repeating patterns, prefix/suffix wildcards, and middle-dot handles).
It impersonates official Chrome TLS fingerprints (JA3/JA4) to bypass Cloudflare and Discord WAF restrictions, and uses userspace wireproxy to route traffic exclusively without altering host OS networking or other active applications.

[ 🚀 Multi-Window Sharding: 2x~4x Speedup Guide ]
Run multiple instances of this program in parallel with 0% duplicate work and live SQLite synchronization:
1. [2 Windows (2x Speedup)]:
   - Window 1: Mode = 'Permutation' -> Multi-Window Sharding = '2-Split - [Win 1: a ~ m]' -> Start
   - Window 2: Open another program -> Multi-Window Sharding = '2-Split - [Win 2: n ~ _]' -> Start
   - Both windows run without 1 single duplicate check and finish in half the time!
2. [3 Windows (3x Speedup)]:
   - Win 1: '3-Split - [Win 1: a ~ i]' | Win 2: '3-Split - [Win 2: j ~ r]' | Win 3: '3-Split - [Win 3: s ~ _]'
3. [4 Windows (4x Speedup)]:
   - Win 1: '4-Split - [Win 1: a ~ g]' | Win 2: '4-Split - [Win 2: h ~ n]' | Win 3: '4-Split - [Win 3: o ~ u]' | Win 4: '4-Split - [Win 4: v ~ _]'
4. [Custom Letter Range]:
   - Select 'Custom Letter Range' to target specific starting characters (e.g. digits 0 to 9).

[ 💡 3-Step Quick Start ]
Step 1: [Select Mode] Choose your generation mode (Dictionary, Pattern, Custom Mask, or Permutation) and length (3-6 chars).
Step 2: [Select Proxy & Workers] Surfshark isolated multi-tunnel is recommended with 3-5 workers.
Step 3: [Start & Claim] Click 'Start Checking'. When available usernames are found, they pop up in real-time. Click 'Open Discord Registration' to claim immediately!

[ 🛠️ Key UI Features ]
1. [Real-time Log Controls]: Clear logs, Save logs to .txt/.log, and Collapse/Expand the log console.
2. [Export Results]: Export available usernames to .txt, .csv, or .json.
3. [SQLite Live Sync]: Discovered usernames and deduplication cache synchronize across all windows in real-time.
""",
        "help_close": "Close"
    }
}

class I18nManager:
    _current_lang = "ko"

    @classmethod
    def set_language(cls, lang: str):
        if lang in STRINGS:
            cls._current_lang = lang

    @classmethod
    def get_language(cls) -> str:
        return cls._current_lang

    @classmethod
    def t(cls, key: str, **kwargs) -> str:
        lang_dict = STRINGS.get(cls._current_lang, STRINGS["ko"])
        template = lang_dict.get(key, STRINGS["ko"].get(key, key))
        if kwargs:
            try:
                return template.format(**kwargs)
            except Exception:
                return template
        return template
