# src/ui/colab_gui.py
"""
D4UC Google Colab Native Interactive Web GUI
Provides an in-cell HTML5/CSS/JavaScript responsive dark-theme dashboard
with real-time KPI metrics, visual progress bar, live discovered usernames table,
streamed terminal logs, and 10-language instant switching.
"""
import json
import time
from typing import Dict, Any, List, Optional
from src.ui.i18n import I18nManager, SUPPORTED_LANGUAGES, LANG_NAMES, LANG_FLAGS

try:
    from IPython.display import display, HTML, Javascript
    _IPYTHON_AVAILABLE = True
except ImportError:
    _IPYTHON_AVAILABLE = False


class ColabDashboard:
    """
    Colab-Native Web GUI Dashboard rendered directly inside Jupyter/Colab notebook output.
    """
    def __init__(self, lang: str = "ko", title: str = "D4UC Cloud Checker"):
        self.lang = lang if lang in SUPPORTED_LANGUAGES else "ko"
        I18nManager.set_language(self.lang)
        self.title = title
        self.container_id = f"d4uc_dashboard_{int(time.time()*1000)}"
        self._rendered = False
        self._usernames: List[Dict[str, Any]] = []
        self._logs: List[str] = []

    def get_html(self) -> str:
        """Generates self-contained HTML/CSS/JS for the Colab cell."""
        lang_options = "".join([
            f'<option value="{code}" {"selected" if code == self.lang else ""}>{LANG_FLAGS.get(code, "")} {LANG_NAMES.get(code, code)}</option>'
            for code in SUPPORTED_LANGUAGES
        ])

        html_code = f"""
        <div id="{self.container_id}" class="d4uc-wrapper">
            <style>
                #{self.container_id} {{
                    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
                    background: #0f111a;
                    color: #e6edf3;
                    border-radius: 12px;
                    padding: 18px 22px;
                    box-shadow: 0 8px 24px rgba(0,0,0,0.5);
                    max-width: 1000px;
                    margin: 12px auto;
                    box-sizing: border-box;
                    border: 1px solid #2d3348;
                }}
                #{self.container_id} * {{ box-sizing: border-box; }}
                #{self.container_id} .d4uc-header {{
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    border-bottom: 1px solid #2d3348;
                    padding-bottom: 12px;
                    margin-bottom: 16px;
                }}
                #{self.container_id} .d4uc-title {{
                    font-size: 20px;
                    font-weight: 700;
                    color: #58a6ff;
                    display: flex;
                    align-items: center;
                    gap: 8px;
                }}
                #{self.container_id} .d4uc-lang-select {{
                    background: #1e2233;
                    color: #c9d1d9;
                    border: 1px solid #3d4461;
                    padding: 6px 12px;
                    border-radius: 6px;
                    font-size: 13px;
                    cursor: pointer;
                    outline: none;
                }}
                #{self.container_id} .d4uc-kpi-grid {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
                    gap: 12px;
                    margin-bottom: 16px;
                }}
                #{self.container_id} .d4uc-kpi-card {{
                    background: #171b26;
                    border: 1px solid #2a3147;
                    border-radius: 8px;
                    padding: 12px 14px;
                    text-align: center;
                    transition: transform 0.15s ease;
                }}
                #{self.container_id} .d4uc-kpi-card:hover {{
                    transform: translateY(-2px);
                    border-color: #58a6ff;
                }}
                #{self.container_id} .d4uc-kpi-label {{
                    font-size: 12px;
                    color: #8b949e;
                    margin-bottom: 6px;
                    text-transform: uppercase;
                    letter-spacing: 0.5px;
                }}
                #{self.container_id} .d4uc-kpi-value {{
                    font-size: 24px;
                    font-weight: 700;
                    color: #f0f6fc;
                }}
                #{self.container_id} .d4uc-kpi-value.avail {{ color: #2ea043; }}
                #{self.container_id} .d4uc-kpi-value.taken {{ color: #8b949e; }}
                #{self.container_id} .d4uc-kpi-value.rate429 {{ color: #d29922; }}
                #{self.container_id} .d4uc-kpi-value.rps {{ color: #58a6ff; }}
                #{self.container_id} .d4uc-kpi-value.skip {{ color: #bc8cff; }}
                
                #{self.container_id} .d4uc-progress-section {{
                    margin-bottom: 16px;
                }}
                #{self.container_id} .d4uc-progress-meta {{
                    display: flex;
                    justify-content: space-between;
                    font-size: 13px;
                    color: #8b949e;
                    margin-bottom: 6px;
                }}
                #{self.container_id} .d4uc-progress-bar-bg {{
                    background: #21262d;
                    height: 10px;
                    border-radius: 5px;
                    overflow: hidden;
                }}
                #{self.container_id} .d4uc-progress-bar-fill {{
                    background: linear-gradient(90deg, #1f6feb, #2ea043);
                    height: 100%;
                    width: 0%;
                    transition: width 0.3s ease;
                }}

                #{self.container_id} .d4uc-table-section {{
                    background: #171b26;
                    border: 1px solid #2a3147;
                    border-radius: 8px;
                    padding: 14px;
                    margin-bottom: 16px;
                }}
                #{self.container_id} .d4uc-table-header {{
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    margin-bottom: 10px;
                }}
                #{self.container_id} .d4uc-table-header h3 {{
                    margin: 0;
                    font-size: 15px;
                    color: #7ee787;
                    display: flex;
                    align-items: center;
                    gap: 6px;
                }}
                #{self.container_id} .d4uc-table-scroll {{
                    max-height: 220px;
                    overflow-y: auto;
                    border-radius: 6px;
                    border: 1px solid #21262d;
                }}
                #{self.container_id} table {{
                    width: 100%;
                    border-collapse: collapse;
                    font-size: 13px;
                }}
                #{self.container_id} th {{
                    background: #1e2233;
                    color: #8b949e;
                    padding: 8px 12px;
                    text-align: left;
                    font-weight: 600;
                    position: sticky;
                    top: 0;
                }}
                #{self.container_id} td {{
                    padding: 8px 12px;
                    border-top: 1px solid #21262d;
                    color: #c9d1d9;
                }}
                #{self.container_id} tr:hover td {{
                    background: rgba(88, 166, 255, 0.08);
                }}
                #{self.container_id} .d4uc-btn-sm {{
                    background: #238636;
                    color: #ffffff;
                    border: none;
                    border-radius: 4px;
                    padding: 4px 8px;
                    font-size: 11px;
                    font-weight: 600;
                    cursor: pointer;
                    margin-right: 4px;
                    text-decoration: none;
                    display: inline-block;
                }}
                #{self.container_id} .d4uc-btn-sm.copy {{
                    background: #30363d;
                    color: #c9d1d9;
                }}
                #{self.container_id} .d4uc-btn-sm:hover {{
                    opacity: 0.85;
                }}

                #{self.container_id} .d4uc-log-section {{
                    background: #0d1117;
                    border: 1px solid #2a3147;
                    border-radius: 8px;
                    padding: 12px;
                }}
                #{self.container_id} .d4uc-log-header {{
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    margin-bottom: 8px;
                }}
                #{self.container_id} .d4uc-log-header span {{
                    font-size: 13px;
                    font-weight: 600;
                    color: #8b949e;
                }}
                #{self.container_id} .d4uc-log-controls {{
                    display: flex;
                    gap: 6px;
                }}
                #{self.container_id} .d4uc-btn-ctrl {{
                    background: #21262d;
                    color: #8b949e;
                    border: 1px solid #30363d;
                    border-radius: 4px;
                    padding: 3px 8px;
                    font-size: 11px;
                    cursor: pointer;
                }}
                #{self.container_id} .d4uc-btn-ctrl:hover {{
                    color: #c9d1d9;
                    border-color: #8b949e;
                }}
                #{self.container_id} .d4uc-log-box {{
                    background: #090d13;
                    border: 1px solid #161b22;
                    border-radius: 4px;
                    padding: 10px;
                    font-family: ui-monospace, SFMono-Regular, Consolas, "Liberation Mono", Menlo, monospace;
                    font-size: 12px;
                    color: #7ee787;
                    height: 140px;
                    overflow-y: auto;
                    white-space: pre-wrap;
                    line-height: 1.4;
                }}
            </style>

            <div class="d4uc-header">
                <div class="d4uc-title">
                    <span>⚡</span>
                    <span id="{self.container_id}_title">{I18nManager.t('app_title')}</span>
                </div>
                <div>
                    <select class="d4uc-lang-select" onchange="window.d4uc_set_lang(this.value)">
                        {lang_options}
                    </select>
                </div>
            </div>

            <!-- KPI Cards -->
            <div class="d4uc-kpi-grid">
                <div class="d4uc-kpi-card">
                    <div class="d4uc-kpi-label" id="{self.container_id}_lbl_rps">{I18nManager.t('kpi_rps')}</div>
                    <div class="d4uc-kpi-value rps" id="{self.container_id}_val_rps">0.0</div>
                </div>
                <div class="d4uc-kpi-card">
                    <div class="d4uc-kpi-label" id="{self.container_id}_lbl_total">{I18nManager.t('kpi_total')}</div>
                    <div class="d4uc-kpi-value" id="{self.container_id}_val_total">0</div>
                </div>
                <div class="d4uc-kpi-card">
                    <div class="d4uc-kpi-label" id="{self.container_id}_lbl_avail">{I18nManager.t('kpi_avail')}</div>
                    <div class="d4uc-kpi-value avail" id="{self.container_id}_val_avail">0</div>
                </div>
                <div class="d4uc-kpi-card">
                    <div class="d4uc-kpi-label" id="{self.container_id}_lbl_taken">{I18nManager.t('kpi_taken')}</div>
                    <div class="d4uc-kpi-value taken" id="{self.container_id}_val_taken">0</div>
                </div>
                <div class="d4uc-kpi-card">
                    <div class="d4uc-kpi-label" id="{self.container_id}_lbl_429">{I18nManager.t('kpi_429')}</div>
                    <div class="d4uc-kpi-value rate429" id="{self.container_id}_val_429">0</div>
                </div>
                <div class="d4uc-kpi-card">
                    <div class="d4uc-kpi-label" id="{self.container_id}_lbl_skip">{I18nManager.t('kpi_skipped')}</div>
                    <div class="d4uc-kpi-value skip" id="{self.container_id}_val_skip">0</div>
                </div>
            </div>

            <!-- Visual Progress -->
            <div class="d4uc-progress-section">
                <div class="d4uc-progress-meta">
                    <span id="{self.container_id}_progress_text">진행률: 0% (0 / 0)</span>
                    <span id="{self.container_id}_status_badge" style="color: #58a6ff;">● {I18nManager.t('status_idle')}</span>
                </div>
                <div class="d4uc-progress-bar-bg">
                    <div class="d4uc-progress-bar-fill" id="{self.container_id}_progress_fill"></div>
                </div>
            </div>

            <!-- Discovered Usernames Table -->
            <div class="d4uc-table-section">
                <div class="d4uc-table-header">
                    <h3 id="{self.container_id}_table_title">🏆 {I18nManager.t('table_title')}</h3>
                    <span style="font-size: 12px; color: #8b949e;">{I18nManager.t('auto_save_indicator', count=0)}</span>
                </div>
                <div class="d4uc-table-scroll">
                    <table>
                        <thead>
                            <tr>
                                <th>#</th>
                                <th>{I18nManager.t('col_username')}</th>
                                <th>{I18nManager.t('col_time')}</th>
                                <th>{I18nManager.t('col_latency')}</th>
                                <th>{I18nManager.t('col_pattern')}</th>
                                <th>작업 (Action)</th>
                            </tr>
                        </thead>
                        <tbody id="{self.container_id}_tbody">
                            <tr id="{self.container_id}_no_data">
                                <td colspan="6" style="text-align: center; color: #484f58; padding: 24px;">발견된 사용 가능한 닉네임이 여기에 실시간으로 표시됩니다.</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- Live Terminal Log -->
            <div class="d4uc-log-section">
                <div class="d4uc-log-header">
                    <span id="{self.container_id}_log_title">📋 {I18nManager.t('log_title')}</span>
                    <div class="d4uc-log-controls">
                        <button class="d4uc-btn-ctrl" onclick="window.d4uc_toggle_log('{self.container_id}')" id="{self.container_id}_btn_toggle">접기 ▲</button>
                        <button class="d4uc-btn-ctrl" onclick="window.d4uc_clear_log('{self.container_id}')">지우기 🗑️</button>
                        <button class="d4uc-btn-ctrl" onclick="window.d4uc_download_log('{self.container_id}')">다운로드 💾</button>
                    </div>
                </div>
                <div class="d4uc-log-box" id="{self.container_id}_log_box"></div>
            </div>

            <!-- Client Script -->
            <script>
                (function() {{
                    window.d4uc_state_{self.container_id} = {{
                        usernamesCount: 0,
                        logs: []
                    }};

                    window.d4uc_copy = function(text) {{
                        navigator.clipboard.writeText(text).then(() => {{
                            alert('클립보드에 복사되었습니다: ' + text);
                        }}).catch(() => {{
                            prompt('복사하세요:', text);
                        }});
                    }};

                    window.d4uc_toggle_log = function(cid) {{
                        const box = document.getElementById(cid + '_log_box');
                        const btn = document.getElementById(cid + '_btn_toggle');
                        if (!box || !btn) return;
                        if (box.style.display === 'none') {{
                            box.style.display = 'block';
                            btn.innerText = '접기 ▲';
                        }} else {{
                            box.style.display = 'none';
                            btn.innerText = '펼치기 ▼';
                        }}
                    }};

                    window.d4uc_clear_log = function(cid) {{
                        const box = document.getElementById(cid + '_log_box');
                        if (box) box.innerText = '';
                    }};

                    window.d4uc_download_log = function(cid) {{
                        const box = document.getElementById(cid + '_log_box');
                        if (!box) return;
                        const text = box.innerText;
                        const blob = new Blob([text], {{ type: 'text/plain;charset=utf-8' }});
                        const a = document.createElement('a');
                        a.href = URL.createObjectURL(blob);
                        a.download = 'd4uc_colab_log_' + Date.now() + '.txt';
                        a.click();
                    }};

                    window.d4uc_set_lang = function(code) {{
                        console.log('Language switched to:', code);
                        // Can be coupled with python backend via kernel
                    }};
                }})();
            </script>
        </div>
        """
        return html_code

    def render(self):
        """Renders the dashboard inside IPython output."""
        if _IPYTHON_AVAILABLE:
            display(HTML(self.get_html()))
            self._rendered = True
        else:
            print(f"[{self.title}] ColabDashboard instantiated (IPython display unavailable).")

    def update_metrics(self, rps: float, total: int, avail: int, taken: int, rate429: int, skipped: int, progress: float = 0.0, max_comb: int = 0):
        """Updates real-time KPI metrics in the DOM."""
        if not _IPYTHON_AVAILABLE:
            return
        pct_text = f"진행률: {progress:.1f}% ({total:,} / {max_comb:,})" if max_comb > 0 else f"진행률: {total:,}건 검사완료"
        pct_width = f"{min(100.0, max(0.0, progress)):.1f}%"
        js = f"""
        (function() {{
            const cid = '{self.container_id}';
            const elRps = document.getElementById(cid + '_val_rps');
            const elTot = document.getElementById(cid + '_val_total');
            const elAvail = document.getElementById(cid + '_val_avail');
            const elTaken = document.getElementById(cid + '_val_taken');
            const el429 = document.getElementById(cid + '_val_429');
            const elSkip = document.getElementById(cid + '_val_skip');
            const elProgText = document.getElementById(cid + '_progress_text');
            const elProgFill = document.getElementById(cid + '_progress_fill');

            if (elRps) elRps.innerText = '{rps:.1f}';
            if (elTot) elTot.innerText = '{total:,}';
            if (elAvail) elAvail.innerText = '{avail:,}';
            if (elTaken) elTaken.innerText = '{taken:,}';
            if (el429) el429.innerText = '{rate429:,}';
            if (elSkip) elSkip.innerText = '{skipped:,}';
            if (elProgText) elProgText.innerText = '{pct_text}';
            if (elProgFill) elProgFill.style.width = '{pct_width}';
        }})();
        """
        display(Javascript(js))

    def add_username(self, username: str, timestamp: str, latency_ms: int, pattern: str = "4char"):
        """Adds a discovered available username to the table top."""
        self._usernames.append({"username": username, "time": timestamp, "latency": latency_ms, "pattern": pattern})
        if not _IPYTHON_AVAILABLE:
            return
        idx = len(self._usernames)
        row_html = f"""
        <tr>
            <td><strong>#{idx}</strong></td>
            <td style="color: #7ee787; font-weight: 700; font-family: monospace; font-size: 14px;">{username}</td>
            <td style="color: #8b949e;">{timestamp}</td>
            <td style="color: #79c0ff;">{latency_ms}ms</td>
            <td><span style="background: #1f6feb22; color: #58a6ff; padding: 2px 6px; border-radius: 4px; font-size: 11px;">{pattern}</span></td>
            <td>
                <button class="d4uc-btn-sm copy" onclick="window.d4uc_copy('{username}')">복사 📋</button>
                <a class="d4uc-btn-sm" href="https://discord.com/register" target="_blank">등록 🚀</a>
            </td>
        </tr>
        """.replace('\n', '')

        js = f"""
        (function() {{
            const tbody = document.getElementById('{self.container_id}_tbody');
            const noData = document.getElementById('{self.container_id}_no_data');
            if (noData) noData.remove();
            if (tbody) {{
                tbody.insertAdjacentHTML('afterbegin', `{row_html}`);
            }}
        }})();
        """
        display(Javascript(js))

    def append_log(self, text: str):
        """Appends a new line of text to the live log window."""
        self._logs.append(text)
        if not _IPYTHON_AVAILABLE:
            return
        escaped_text = text.replace('\\', '\\\\').replace('`', '\\`').replace('$', '\\$')
        js = f"""
        (function() {{
            const box = document.getElementById('{self.container_id}_log_box');
            if (box) {{
                box.innerText += `{escaped_text}\\n`;
                box.scrollTop = box.scrollHeight;
            }}
        }})();
        """
        display(Javascript(js))
