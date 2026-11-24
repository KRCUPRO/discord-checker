/**
 * ==============================================================================
 * D4UC (Discord 4-Character Usernames Checker) Multi-Account Worker Node
 * Google Apps Script (GAS) 다중 구글 계정 분산 샤딩 전용 워커 템플릿 (v18.0)
 * ==============================================================================
 * 
 * [다중 계정 분산 가동 안내]
 * - 본 파일은 2번째, 3번째... N번째 추가 구글 계정(script.google.com)에 배포하는 전용 스크립트입니다.
 * - 아래 CONFIG에서 WORKER_ID(0 ~ TOTAL_WORKERS - 1)와 TOTAL_WORKERS만 지정하면
 *   각 구글 계정이 서로 전혀 겹치지 않는 구간을 100% 무충돌(Zero-Collision)로 분담 탐색합니다.
 * - 예시 (총 4개 계정 사용 시):
 *   * 계정 1: WORKER_ID = 0, TOTAL_WORKERS = 4 (0000 ~ 8zzz 탐색)
 *   * 계정 2: WORKER_ID = 1, TOTAL_WORKERS = 4 (9000 ~ hzzz 탐색)
 *   * 계정 3: WORKER_ID = 2, TOTAL_WORKERS = 4 (i000 ~ qzzz 탐색)
 *   * 계정 4: WORKER_ID = 3, TOTAL_WORKERS = 4 (r000 ~ zzzz 탐색)
 *   -> 4개 계정 합산 일일 최대 80,000회 초고속 24시간 가용성 탐색!
 */

const CONFIG = {
  // [워커 식별 설정] - 각 구글 계정마다 이 부분을 다르게 지정하세요!
  WORKER_ID: 1,                      // 현재 워커 번호 (계정 1=0, 계정 2=1, 계정 3=2...)
  TOTAL_WORKERS: 4,                  // 전체 운영할 구글 계정/워커 수
  ACCOUNT_LABEL: 'Worker-Node-02',   // 식별용 노드 이름 (디스코드 알림 및 시트에 표기됨)

  // [트리거 주기 모드]
  TRIGGER_MODE: 'BALANCED',          // 'BALANCED' (5분 정기 가동) 또는 'TURBO' (1분 초고속 가동)

  // [알림 설정] - 모든 워커에서 동일한 디스코드 웹훅 URL을 사용하면 한 채널로 취합됩니다!
  DISCORD_WEBHOOK_URL: '',           // 가용 닉네임 발견 시 알림받을 Discord Webhook URL

  // [탐색 설정]
  USERNAME_LENGTH: 4,
  CHARSET: 'abcdefghijklmnopqrstuvwxyz0123456789',
  MAX_EXECUTION_TIME_MS: 270000,    // 4.5분 안전 마진
  RATE_LIMIT_COOLDOWN_MS: 30000,    // 429 쿨다운

  // [저장소 설정]
  DRIVE_FOLDER_NAME: 'D4UC_Checker',
  ENABLE_SPREADSHEET: true,
  SPREADSHEET_NAME: 'D4UC_Tracker'
};

function initWorkerNode() {
  Logger.log(`🚀 [D4UC Worker] 노드 초기화: ${CONFIG.ACCOUNT_LABEL} (${CONFIG.WORKER_ID + 1}/${CONFIG.TOTAL_WORKERS})`);
  const folder = getOrCreateFolder(CONFIG.DRIVE_FOLDER_NAME);
  
  if (CONFIG.ENABLE_SPREADSHEET) {
    getOrCreateSpreadsheet(folder, CONFIG.SPREADSHEET_NAME);
  }

  const totalCombinations = Math.pow(CONFIG.CHARSET.length, CONFIG.USERNAME_LENGTH);
  const shard = getShardRange(CONFIG.WORKER_ID, CONFIG.TOTAL_WORKERS, totalCombinations);
  Logger.log(`🔢 [Shard] 구간: ${shard.start.toLocaleString()} ~ ${shard.end.toLocaleString()} (총 ${shard.total.toLocaleString()}개)`);

  const props = PropertiesService.getScriptProperties();
  const cursorKey = `cursor_index_w${CONFIG.WORKER_ID}`;
  if (!props.getProperty(cursorKey)) {
    props.setProperties({
      [cursorKey]: shard.start.toString(),
      'total_checked': '0',
      'total_available': '0',
      'start_time': Date.now().toString()
    });
  }

  clearAllTriggers();
  setupTrigger();
  Logger.log(`✅ [D4UC Worker] ${CONFIG.ACCOUNT_LABEL} 가동 준비 및 예약 트리거 등록 완료!`);
}

function stopWorkerNode() {
  clearAllTriggers();
  Logger.log(`🛑 [D4UC Worker] ${CONFIG.ACCOUNT_LABEL} 예약 트리거 해제 완료.`);
}

function setupTrigger() {
  clearAllTriggers();
  const triggerBuilder = ScriptApp.newTrigger('runWorkerBatch').timeBased();
  if (CONFIG.TRIGGER_MODE === 'TURBO') {
    triggerBuilder.everyMinutes(1).create();
  } else {
    triggerBuilder.everyMinutes(5).create();
  }
}

function clearAllTriggers() {
  const triggers = ScriptApp.getProjectTriggers();
  for (let i = 0; i < triggers.length; i++) {
    ScriptApp.deleteTrigger(triggers[i]);
  }
}

function getShardRange(workerId, totalWorkers, maxCombinations) {
  const safeWorkers = Math.max(1, totalWorkers);
  const safeId = Math.min(Math.max(0, workerId), safeWorkers - 1);
  const chunkSize = Math.floor(maxCombinations / safeWorkers);
  const start = safeId * chunkSize;
  const end = (safeId === safeWorkers - 1) ? maxCombinations : (safeId + 1) * chunkSize;
  return { start: start, end: end, total: end - start };
}

function runWorkerBatch() {
  const batchStartTime = Date.now();
  const props = PropertiesService.getScriptProperties();
  const charset = CONFIG.CHARSET;
  const len = CONFIG.USERNAME_LENGTH;
  const maxCombinations = Math.pow(charset.length, len);
  const shard = getShardRange(CONFIG.WORKER_ID, CONFIG.TOTAL_WORKERS, maxCombinations);

  const cursorKey = `cursor_index_w${CONFIG.WORKER_ID}`;
  let cursorIndex = parseInt(props.getProperty(cursorKey) || shard.start.toString(), 10);
  if (cursorIndex < shard.start) cursorIndex = shard.start;

  let totalChecked = parseInt(props.getProperty('total_checked') || '0', 10);
  let totalAvailable = parseInt(props.getProperty('total_available') || '0', 10);

  const folder = getOrCreateFolder(CONFIG.DRIVE_FOLDER_NAME);
  const shardProgress = (((cursorIndex - shard.start) / shard.total) * 100).toFixed(2);

  while (cursorIndex < shard.end) {
    if (Date.now() - batchStartTime > CONFIG.MAX_EXECUTION_TIME_MS) {
      break;
    }

    const username = indexToUsername(cursorIndex, charset, len);
    cursorIndex++;
    totalChecked++;

    const checkResult = checkDiscordUsername(username);

    if (checkResult.status === 'AVAILABLE') {
      totalAvailable++;
      appendAvailableToFile(folder, username);

      if (CONFIG.ENABLE_SPREADSHEET) {
        appendAvailableToSheet(folder, username, checkResult.latency, CONFIG.ACCOUNT_LABEL, `${shardProgress}%`);
      }

      if (CONFIG.DISCORD_WEBHOOK_URL) {
        sendDiscordWebhookAvailable(username, checkResult.latency, CONFIG.ACCOUNT_LABEL, `${shardProgress}%`);
      }
    } else if (checkResult.status === 'RATE_LIMIT') {
      Utilities.sleep(CONFIG.RATE_LIMIT_COOLDOWN_MS);
      break;
    }

    Utilities.sleep(120);
  }

  if (cursorIndex >= shard.end) {
    cursorIndex = shard.start;
  }

  props.setProperties({
    [cursorKey]: cursorIndex.toString(),
    'total_checked': totalChecked.toString(),
    'total_available': totalAvailable.toString(),
    'last_run_time': Date.now().toString()
  });

  saveStateToDriveJson(folder, {
    worker_id: CONFIG.WORKER_ID,
    total_workers: CONFIG.TOTAL_WORKERS,
    account_label: CONFIG.ACCOUNT_LABEL,
    cursor_index: cursorIndex,
    shard_progress_pct: shardProgress,
    total_checked: totalChecked,
    total_available: totalAvailable,
    last_run_iso: new Date().toISOString()
  });
}

function checkDiscordUsername(username) {
  const url = 'https://discord.com/api/v9/unique-username/username-attempt-unauthenticated';
  const options = {
    method: 'post',
    contentType: 'application/json',
    payload: JSON.stringify({ username: username }),
    muteHttpExceptions: true,
    headers: {
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
      'Accept': '*/*',
      'Origin': 'https://discord.com'
    }
  };

  const reqStart = Date.now();
  try {
    const response = UrlFetchApp.fetch(url, options);
    const latency = Date.now() - reqStart;
    const statusCode = response.getResponseCode();
    if (statusCode === 200) {
      const data = JSON.parse(response.getContentText());
      return { status: data.taken === false ? 'AVAILABLE' : 'TAKEN', latency: latency };
    } else if (statusCode === 429) {
      return { status: 'RATE_LIMIT', latency: latency };
    }
    return { status: 'ERROR', code: statusCode, latency: latency };
  } catch (e) {
    return { status: 'EXCEPTION', error: e.toString(), latency: Date.now() - reqStart };
  }
}

function getOrCreateFolder(folderName) {
  const folders = DriveApp.getFoldersByName(folderName);
  return folders.hasNext() ? folders.next() : DriveApp.createFolder(folderName);
}

function appendAvailableToFile(folder, username) {
  const fileName = 'available_usernames.txt';
  const files = folder.getFilesByName(fileName);
  if (files.hasNext()) {
    const file = files.next();
    const currentText = file.getBlob().getDataAsString();
    if (!currentText.split('\n').includes(username)) {
      file.setContent(currentText + username + '\n');
    }
  } else {
    folder.createFile(fileName, username + '\n');
  }
}

function saveStateToDriveJson(folder, stateObj) {
  const fileName = `checker_state_w${CONFIG.WORKER_ID}.json`;
  const files = folder.getFilesByName(fileName);
  const jsonStr = JSON.stringify(stateObj, null, 2);
  if (files.hasNext()) {
    files.next().setContent(jsonStr);
  } else {
    folder.createFile(fileName, jsonStr);
  }
}

function getOrCreateSpreadsheet(folder, sheetName) {
  const files = folder.getFilesByName(sheetName);
  if (files.hasNext()) {
    return SpreadsheetApp.open(files.next());
  }
  const ss = SpreadsheetApp.create(sheetName);
  const file = DriveApp.getFileById(ss.getId());
  folder.addFile(file);
  DriveApp.getRootFolder().removeFile(file);
  const sheet = ss.getActiveSheet();
  sheet.setName('🏆 Available Usernames');
  sheet.appendRow(['발견 일시 (UTC)', '닉네임 (Username)', '글자수', '응답속도', '워커 노드', '샤드 진행률', 'Discord 등록 링크']);
  sheet.getRange('A1:G1').setBackground('#1f6feb').setFontColor('#ffffff').setFontWeight('bold');
  sheet.setFrozenRows(1);
  return ss;
}

function appendAvailableToSheet(folder, username, latency, workerLabel, progressPct) {
  try {
    const ss = getOrCreateSpreadsheet(folder, CONFIG.SPREADSHEET_NAME);
    const sheet = ss.getSheetByName('🏆 Available Usernames') || ss.getActiveSheet();
    sheet.appendRow([new Date().toISOString(), username, username.length, `${latency}ms`, workerLabel, progressPct, 'https://discord.com/register']);
  } catch (e) {}
}

function indexToUsername(index, charset, length) {
  let result = '';
  const base = charset.length;
  for (let i = 0; i < length; i++) {
    result = charset[index % base] + result;
    index = Math.floor(index / base);
  }
  return result;
}

function sendDiscordWebhookAvailable(username, latency, workerLabel, progressPct) {
  if (!CONFIG.DISCORD_WEBHOOK_URL) return;
  const payload = {
    content: `🎉 **[D4UC GAS 24/7] 사용 가능한 고유 닉네임 발견!** @here`,
    embeds: [{
      title: `✨ \`${username}\` 선점 가능!`,
      description: `Google Apps Script 분산 워커(${workerLabel})가 희귀 닉네임을 발견했습니다.`,
      color: 0x2ea043,
      fields: [
        { name: '닉네임', value: `\`${username}\``, inline: true },
        { name: '글자수', value: `${username.length}자`, inline: true },
        { name: '응답속도', value: `${latency}ms`, inline: true },
        { name: '워커 노드', value: `🤖 ${workerLabel}`, inline: true },
        { name: '샤드 진행률', value: `📊 ${progressPct}`, inline: true },
        { name: '선점 링크', value: `[Discord 회원가입 바로가기](https://discord.com/register)`, inline: false }
      ],
      footer: { text: `D4UC Multi-Account Fleet • 노드: ${workerLabel}` },
      timestamp: new Date().toISOString()
    }]
  };
  try {
    UrlFetchApp.fetch(CONFIG.DISCORD_WEBHOOK_URL, {
      method: 'post',
      contentType: 'application/json',
      payload: JSON.stringify(payload),
      muteHttpExceptions: true
    });
  } catch (e) {}
}
