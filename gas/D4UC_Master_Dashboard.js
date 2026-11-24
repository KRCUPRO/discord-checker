/**
 * ==============================================================================
 * D4UC (Discord 4-Character Usernames Checker) Master Fleet Dashboard
 * Google Apps Script (GAS) 전체 분산 워커 상태 집계 및 종합 대시보드 (v18.0)
 * ==============================================================================
 * 
 * [역할 및 기능]
 * 1. 복수의 워커 계정들이 Google Drive에 기록한 상태 파일(checker_state_w*.json)을 실시간 취합
 * 2. Google Sheets의 '📈 Fleet Overview' 시트에 전 워커의 가동률, 처리량, 발견수 자동 렌더링
 * 3. 1시간마다 Discord Webhook으로 전체 함대 종합 하트비트 임베드 리포트 자동 전송
 */

const DASHBOARD_CONFIG = {
  DRIVE_FOLDER_NAME: 'D4UC_Checker',
  SPREADSHEET_NAME: 'D4UC_Tracker',
  DISCORD_WEBHOOK_URL: '',          // 전체 함대 종합 보고서를 수신할 Discord Webhook
  TOTAL_EXPECTED_WORKERS: 4,        // 모니터링할 총 워커 수
  ENABLE_HOURLY_DISCORD_REPORT: true
};

function initFleetDashboard() {
  Logger.log('🚀 [D4UC Master Dashboard] 대시보드 모니터 초기화 시작...');
  clearDashboardTriggers();
  
  // 1시간마다 종합 집계 실행
  ScriptApp.newTrigger('aggregateFleetStatus')
    .timeBased()
    .everyHours(1)
    .create();

  Logger.log('✅ [D4UC Master Dashboard] 1시간 주기 종합 모니터링 트리거 등록 완료.');
}

function clearDashboardTriggers() {
  const triggers = ScriptApp.getProjectTriggers();
  for (let i = 0; i < triggers.length; i++) {
    ScriptApp.deleteTrigger(triggers[i]);
  }
}

function aggregateFleetStatus() {
  Logger.log('📊 [D4UC Master] 전체 워커 상태 집계 시작...');
  const folder = getFolder(DASHBOARD_CONFIG.DRIVE_FOLDER_NAME);
  if (!folder) {
    Logger.log('⚠️ [D4UC Master] 작업 폴더가 아직 존재하지 않습니다.');
    return;
  }

  const files = folder.getFiles();
  let workerStats = [];
  let totalCheckedAll = 0;
  let totalAvailableAll = 0;

  while (files.hasNext()) {
    const file = files.next();
    const name = file.getName();
    if (name.startsWith('checker_state_w') && name.endsWith('.json')) {
      try {
        const content = file.getBlob().getDataAsString();
        const stat = JSON.parse(content);
        workerStats.push(stat);
        totalCheckedAll += (stat.total_checked || 0);
        totalAvailableAll += (stat.total_available || 0);
      } catch (e) {
        Logger.log('⚠️ [Parse Error] ' + name + ': ' + e.toString());
      }
    }
  }

  Logger.log(`📈 [D4UC Master] 활성 워커: ${workerStats.length}개 | 누적 검사: ${totalCheckedAll.toLocaleString()} | 누적 가용: ${totalAvailableAll.toLocaleString()}`);

  // 1. Google Sheets 대시보드 갱신
  updateSheetsDashboard(folder, workerStats, totalCheckedAll, totalAvailableAll);

  // 2. Discord Webhook 종합 리포트 전송
  if (DASHBOARD_CONFIG.ENABLE_HOURLY_DISCORD_REPORT && DASHBOARD_CONFIG.DISCORD_WEBHOOK_URL) {
    sendDiscordFleetReport(workerStats, totalCheckedAll, totalAvailableAll);
  }
}

function updateSheetsDashboard(folder, stats, totalChecked, totalAvailable) {
  try {
    const sheetFiles = folder.getFilesByName(DASHBOARD_CONFIG.SPREADSHEET_NAME);
    if (!sheetFiles.hasNext()) return;
    const ss = SpreadsheetApp.open(sheetFiles.next());
    
    let sheet = ss.getSheetByName('📈 Fleet Overview');
    if (!sheet) {
      sheet = ss.insertSheet('📈 Fleet Overview');
    }
    sheet.clear();

    // 헤더 작성
    sheet.appendRow(['D4UC Cloud Fleet Real-Time Status', '', '', '', '']);
    sheet.appendRow(['최종 집계 일시 (UTC)', new Date().toISOString(), '', '총 발견 가용 닉네임', totalAvailable]);
    sheet.appendRow(['총 검사 완료 닉네임', totalChecked, '', '활성 감지 워커 수', stats.length]);
    sheet.appendRow([]);
    sheet.appendRow(['워커 노드 라벨', '담당 구간', '현재 커서', '샤드 진행률', '노드별 발견수', '마지막 런타임']);

    sheet.getRange('A1:E1').setFontWeight('bold').setFontSize(14).setBackground('#0d1117').setFontColor('#58a6ff');
    sheet.getRange('A5:F5').setFontWeight('bold').setBackground('#21262d').setFontColor('#ffffff');

    stats.sort((a, b) => (a.worker_id || 0) - (b.worker_id || 0));
    stats.forEach(s => {
      const rangeStr = `${(s.shard_start || 0).toLocaleString()} ~ ${(s.shard_end || 0).toLocaleString()}`;
      sheet.appendRow([
        s.account_label || `Worker-${s.worker_id}`,
        rangeStr,
        (s.cursor_index || 0).toLocaleString(),
        `${s.shard_progress_pct || 0}%`,
        s.total_available || 0,
        s.last_run_iso || 'N/A'
      ]);
    });
  } catch (e) {
    Logger.log('⚠️ [Sheets Update Error] ' + e.toString());
  }
}

function sendDiscordFleetReport(stats, totalChecked, totalAvailable) {
  const fields = stats.map(s => ({
    name: `🤖 ${s.account_label || 'Node-' + s.worker_id}`,
    value: `진행률: \`${s.shard_progress_pct || 0}%\`\n발견: **${s.total_available || 0}개** (검사: ${(s.total_checked || 0).toLocaleString()})\n최종 갱신: <t:${Math.floor(new Date(s.last_run_iso).getTime() / 1000)}:R>`,
    inline: true
  }));

  const payload = {
    embeds: [{
      title: `📊 [D4UC Cloud Fleet] 전체 워커 1시간 정기 리포트`,
      description: `현재 **${stats.length}개 노드**가 24시간 가용성 탐색을 무중단 수행 중입니다.`,
      color: 0x5865f2, // Blurple
      fields: [
        { name: '🌐 총 검사 완료 수', value: `\`${totalChecked.toLocaleString()}\` 회`, inline: true },
        { name: '🏆 총 발견 가용 닉네임', value: `\`${totalAvailable.toLocaleString()}\` 개`, inline: true },
        { name: '⚡ 활성 워커', value: `\`${stats.length} / ${DASHBOARD_CONFIG.TOTAL_EXPECTED_WORKERS}\` 노드`, inline: true },
        ...fields
      ],
      footer: { text: 'D4UC Master Central Dashboard • 24/7 Serverless Fleet' },
      timestamp: new Date().toISOString()
    }]
  };

  try {
    UrlFetchApp.fetch(DASHBOARD_CONFIG.DISCORD_WEBHOOK_URL, {
      method: 'post',
      contentType: 'application/json',
      payload: JSON.stringify(payload),
      muteHttpExceptions: true
    });
  } catch (e) {
    Logger.log('⚠️ [Report Webhook Error] ' + e.toString());
  }
}

function getFolder(folderName) {
  const folders = DriveApp.getFoldersByName(folderName);
  return folders.hasNext() ? folders.next() : null;
}
