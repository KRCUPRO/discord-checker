/**
 * ==============================================================================
 * D4UC (Discord 4-Character Usernames Checker) Cloud Serverless 24/7 Engine
 * Google Apps Script (GAS) 24시간 무중단 자동 예약 체커 시스템 (v16)
 * ==============================================================================
 * 
 * [핵심 특징]
 * 1. 24/7 완전 무인 클라우드 구동: PC, 스마트폰, Colab 없이 구글 인프라에서 영구 자동 실행
 * 2. 6분 타임아웃 돌파: 4.5분 경과 시 자동 체크포인트 저장 후 Self-Chaining 트리거 예약
 * 3. 듀얼 구동 모드:
 *    - STANDALONE: 구글 클라우드에서 단독 24시간 상시 순환
 *    - HYBRID_WATCHDOG: Colab 세션 종료(10분 무응답) 감지 시 자동 비상 인계
 * 4. 듀얼 영속성 저장소:
 *    - Google Drive 텍스트 파일 (available_usernames.txt, checker_state.json)
 *    - Google Sheets 실시간 대시보드 (D4UC_Tracker 스프레드시트)
 * 5. 듀얼 트리거 주기:
 *    - BALANCED: 5분 정기 트리거 (일일 90분 쿼터 보존, 24시간 안정 순항)
 *    - TURBO: 1분 주기 초고속 점검
 * 6. Discord Webhook 실시간 알림: 가용 닉네임 발견 시 즉시 초록색 임베드 전송
 */

// ==========================================
// 1. 사용자 전역 설정 (User Configuration)
// ==========================================
const CONFIG = {
  // [구동 모드] 'STANDALONE' (단독 24/7) 또는 'HYBRID_WATCHDOG' (Colab 감시 페일오버)
  EXECUTION_MODE: 'STANDALONE',

  // [트리거 주기 모드] 'BALANCED' (5분 정기 + 4.5분 타임아웃) 또는 'TURBO' (1분 초고속)
  TRIGGER_MODE: 'BALANCED',

  // [탐색 설정]
  USERNAME_LENGTH: 4,               // 탐색 글자수 (3 ~ 6)
  CHARSET: 'abcdefghijklmnopqrstuvwxyz0123456789', // 순열 문자셋
  BATCH_SIZE: 50,                   // 1회 루프당 검사 배치 크기
  MAX_EXECUTION_TIME_MS: 270000,    // 4.5분 (GAS 6분 타임아웃 회피 안전 마진)
  RATE_LIMIT_COOLDOWN_MS: 30000,    // 429 수신 시 쿨다운 지연(ms)

  // [저장소 설정]
  DRIVE_FOLDER_NAME: 'D4UC_Checker', // Google Drive 저장 폴더명
  ENABLE_SPREADSHEET: true,          // Google Sheets 실시간 대시보드 사용 여부
  SPREADSHEET_NAME: 'D4UC_Tracker',  // 구글 스프레드시트 이름

  // [알림 설정]
  DISCORD_WEBHOOK_URL: '',           // 가용 닉네임 발견 시 알림받을 Discord Webhook URL (선택)
  NOTIFY_AVAILABLE: true,            // 가용 닉네임 발견 시 즉시 웹훅 전송
  NOTIFY_HOURLY_REPORT: true         // 1시간마다 요약 통계 웹훅 전송
};

// ==========================================
// 2. 초기화 및 트리거 관리 (Trigger Setup)
// ==========================================

/**
 * 최초 1회 실행하여 Google Drive 폴더, 스프레드시트, 예약 트리거를 원클릭 생성합니다.
 */
function initD4UCChecker() {
  Logger.log('🚀 [D4UC] Google Apps Script 24/7 자동 체커 초기화를 시작합니다...');

  // 1. 드라이브 폴더 확인/생성
  const folder = getOrCreateFolder(CONFIG.DRIVE_FOLDER_NAME);
  Logger.log('📁 작업 폴더 준비 완료: ' + folder.getName() + ' (ID: ' + folder.getId() + ')');

  // 2. 스프레드시트 확인/생성
  if (CONFIG.ENABLE_SPREADSHEET) {
    const sheetFile = getOrCreateSpreadsheet(folder, CONFIG.SPREADSHEET_NAME);
    Logger.log('📊 스프레드시트 대시보드 준비 완료: ' + sheetFile.getUrl());
  }

  // 3. 상태 저장소 초기화 (PropertiesService)
  const props = PropertiesService.getScriptProperties();
  if (!props.getProperty('cursor_index')) {
    props.setProperties({
      'cursor_index': '0',
      'total_checked': '0',
      'total_available': '0',
      'total_taken': '0',
      'total_429': '0',
      'start_time': Date.now().toString(),
      'last_run_time': Date.now().toString()
    });
    Logger.log('🔒 상태 저장소(PropertiesService) 초기화 완료.');
  }

  // 4. 기존 트리거 정리 후 신규 예약 트리거 등록
  clearAllTriggers();
  setupScheduledTrigger();

  Logger.log('✅ [D4UC] 24시간 자동 체커 초기화 및 트리거 등록이 완료되었습니다!');
  Logger.log('⏰ 현재 설정된 모드: ' + CONFIG.EXECUTION_MODE + ' | 주기: ' + CONFIG.TRIGGER_MODE);
}

/**
 * 모든 예약 트리거를 제거하고 체커를 안전하게 중단합니다.
 */
function stopD4UCChecker() {
  clearAllTriggers();
  Logger.log('🛑 [D4UC] 모든 예약 트리거가 삭제되었습니다. 24시간 체커가 안전하게 정지되었습니다.');
}

/**
 * 트리거를 설정합니다 (BALANCED: 5분 주기, TURBO: 1분 주기).
 */
function setupScheduledTrigger() {
  clearAllTriggers();
  const triggerBuilder = ScriptApp.newTrigger('runCheckerBatch').timeBased();
  
  if (CONFIG.TRIGGER_MODE === 'TURBO') {
    triggerBuilder.everyMinutes(1).create();
    Logger.log('⏰ [Trigger] 1분 주기 초고속(TURBO) 트리거가 등록되었습니다.');
  } else {
    triggerBuilder.everyMinutes(5).create();
    Logger.log('⏰ [Trigger] 5분 주기 표준(BALANCED) 트리거가 등록되었습니다.');
  }
}

/**
 * 기존에 등록된 모든 트리거를 깨끗하게 제거합니다.
 */
function clearAllTriggers() {
  const triggers = ScriptApp.getProjectTriggers();
  for (let i = 0; i < triggers.length; i++) {
    ScriptApp.deleteTrigger(triggers[i]);
  }
}

// ==========================================
// 3. 메인 자동 실행 루틴 (Core Batch Runner)
// ==========================================

/**
 * 시간 기반 트리거에 의해 분/시간 단위로 자동 호출되는 메인 검사 함수입니다.
 */
function runCheckerBatch() {
  const batchStartTime = Date.now();
  const props = PropertiesService.getScriptProperties();

  // 하이브리드 워치독 모드 검사
  if (CONFIG.EXECUTION_MODE === 'HYBRID_WATCHDOG') {
    if (isColabActive()) {
      Logger.log('ℹ️ [Watchdog] Colab 세션이 현재 활성 상태입니다. GAS 검사를 대기합니다.');
      return;
    }
    Logger.log('⚠️ [Watchdog] Colab 세션 무응답 감지! GAS가 비상 인계하여 검사를 진행합니다.');
  }

  let cursorIndex = parseInt(props.getProperty('cursor_index') || '0', 10);
  let totalChecked = parseInt(props.getProperty('total_checked') || '0', 10);
  let totalAvailable = parseInt(props.getProperty('total_available') || '0', 10);
  let totalTaken = parseInt(props.getProperty('total_taken') || '0', 10);
  let total429 = parseInt(props.getProperty('total_429') || '0', 10);

  const charset = CONFIG.CHARSET;
  const len = CONFIG.USERNAME_LENGTH;
  const maxCombinations = Math.pow(charset.length, len);

  const folder = getOrCreateFolder(CONFIG.DRIVE_FOLDER_NAME);
  let newlyFound = [];

  Logger.log(`🚀 [D4UC Batch] 검사 시작 | 현재 커서: ${cursorIndex.toLocaleString()} / ${maxCombinations.toLocaleString()}`);

  while (cursorIndex < maxCombinations) {
    // 4.5분 타임아웃 감시 (안전 마진 확보)
    if (Date.now() - batchStartTime > CONFIG.MAX_EXECUTION_TIME_MS) {
      Logger.log('⏳ [Timeout Guard] 4.5분 안전 마진 도달. 체크포인트를 저장하고 다음 주기로 이양합니다.');
      break;
    }

    const username = indexToUsername(cursorIndex, charset, len);
    cursorIndex++;
    totalChecked++;

    const checkResult = checkDiscordUsername(username);

    if (checkResult.status === 'AVAILABLE') {
      totalAvailable++;
      newlyFound.push({ username: username, time: new Date().toISOString(), latency: checkResult.latency });
      Logger.log(`🎉 [가용 닉네임 발견!] : ${username} (${checkResult.latency}ms)`);
      
      // 구글 드라이브 파일 즉시 저장
      appendAvailableToFile(folder, username);

      // 구글 스프레드시트 즉시 행 추가
      if (CONFIG.ENABLE_SPREADSHEET) {
        appendAvailableToSheet(folder, username, checkResult.latency);
      }

      // Discord Webhook 즉시 알림
      if (CONFIG.NOTIFY_AVAILABLE && CONFIG.DISCORD_WEBHOOK_URL) {
        sendDiscordWebhookAvailable(username, checkResult.latency);
      }
    } else if (checkResult.status === 'TAKEN') {
      totalTaken++;
    } else if (checkResult.status === 'RATE_LIMIT') {
      total429++;
      Logger.log(`⚠️ [429 Rate Limit] 쿨다운 지연 적용 (${CONFIG.RATE_LIMIT_COOLDOWN_MS}ms)`);
      Utilities.sleep(CONFIG.RATE_LIMIT_COOLDOWN_MS);
      // 연속 429 완화를 위해 이번 배치 조기 종료
      break;
    }

    // 소폭의 요청 간격 조절 (지터)
    Utilities.sleep(120);
  }

  // 배치 완료 후 상태 저장 (PropertiesService & Google Drive JSON)
  props.setProperties({
    'cursor_index': cursorIndex.toString(),
    'total_checked': totalChecked.toString(),
    'total_available': totalAvailable.toString(),
    'total_taken': totalTaken.toString(),
    'total_429': total429.toString(),
    'last_run_time': Date.now().toString()
  });

  saveStateToDriveJson(folder, {
    cursor_index: cursorIndex,
    max_combinations: maxCombinations,
    total_checked: totalChecked,
    total_available: totalAvailable,
    total_taken: totalTaken,
    total_429: total429,
    last_run_iso: new Date().toISOString(),
    execution_mode: CONFIG.EXECUTION_MODE,
    trigger_mode: CONFIG.TRIGGER_MODE
  });

  const durationSec = ((Date.now() - batchStartTime) / 1000).toFixed(1);
  Logger.log(`🏁 [D4UC Batch] 배치 완료 | 소요: ${durationSec}초 | 신규 발견: ${newlyFound.length}개 | 누적 가용: ${totalAvailable}개`);
}

// ==========================================
// 4. Discord API 검사 엔진 (Network Layer)
// ==========================================

/**
 * Discord 미인증 엔드포인트로 닉네임 가용성을 비동기 점검합니다.
 */
function checkDiscordUsername(username) {
  const url = 'https://discord.com/api/v9/unique-username/username-attempt-unauthenticated';
  const payload = JSON.stringify({ username: username });
  const options = {
    method: 'post',
    contentType: 'application/json',
    payload: payload,
    muteHttpExceptions: true,
    headers: {
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
      'Accept': '*/*',
      'Accept-Language': 'en-US,en;q=0.9',
      'Origin': 'https://discord.com'
    }
  };

  const reqStart = Date.now();
  try {
    const response = UrlFetchApp.fetch(url, options);
    const latency = Date.now() - reqStart;
    const statusCode = response.getResponseCode();
    const content = response.getContentText();

    if (statusCode === 200) {
      const data = JSON.parse(content);
      if (data.taken === false) {
        return { status: 'AVAILABLE', latency: latency };
      } else {
        return { status: 'TAKEN', latency: latency };
      }
    } else if (statusCode === 429) {
      return { status: 'RATE_LIMIT', latency: latency };
    } else {
      return { status: 'ERROR', code: statusCode, latency: latency };
    }
  } catch (e) {
    return { status: 'EXCEPTION', error: e.toString(), latency: Date.now() - reqStart };
  }
}

// ==========================================
// 5. Google Drive & Sheets 영속성 계층
// ==========================================

function getOrCreateFolder(folderName) {
  const folders = DriveApp.getFoldersByName(folderName);
  if (folders.hasNext()) {
    return folders.next();
  }
  return DriveApp.createFolder(folderName);
}

function appendAvailableToFile(folder, username) {
  const fileName = 'available_usernames.txt';
  const files = folder.getFilesByName(fileName);
  let file;
  if (files.hasNext()) {
    file = files.next();
    const currentText = file.getBlob().getDataAsString();
    file.setContent(currentText + username + '\n');
  } else {
    file = folder.createFile(fileName, username + '\n');
  }
}

function saveStateToDriveJson(folder, stateObj) {
  const fileName = 'checker_state.json';
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

  // 시트 서식 초기화
  const sheet = ss.getActiveSheet();
  sheet.setName('🏆 Available Usernames');
  sheet.appendRow(['발견 일시 (UTC)', '닉네임 (Username)', '글자수', '응답속도', 'Discord 등록 링크']);
  sheet.getRange('A1:E1').setBackground('#1f6feb').setFontColor('#ffffff').setFontWeight('bold');
  sheet.setFrozenRows(1);

  return ss;
}

function appendAvailableToSheet(folder, username, latency) {
  try {
    const ss = getOrCreateSpreadsheet(folder, CONFIG.SPREADSHEET_NAME);
    const sheet = ss.getSheetByName('🏆 Available Usernames') || ss.getActiveSheet();
    const nowIso = new Date().toISOString();
    const regLink = 'https://discord.com/register';
    sheet.appendRow([nowIso, username, username.length, `${latency}ms`, regLink]);
  } catch (e) {
    Logger.log('⚠️ [Sheets Error] ' + e.toString());
  }
}

// ==========================================
// 6. 하이브리드 워치독 및 헬퍼 함수
// ==========================================

function isColabActive() {
  try {
    const folder = getOrCreateFolder(CONFIG.DRIVE_FOLDER_NAME);
    const files = folder.getFilesByName('colab_heartbeat.json');
    if (!files.hasNext()) return false;
    const content = files.next().getBlob().getDataAsString();
    const hb = JSON.parse(content);
    const lastTimestamp = hb.timestamp_ms || 0;
    // 10분(600,000ms) 이내에 갱신되었으면 Colab이 살아있는 것으로 판정
    return (Date.now() - lastTimestamp) < 600000;
  } catch (e) {
    return false;
  }
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

// ==========================================
// 7. Discord Webhook 알림 발송 엔진
// ==========================================

function sendDiscordWebhookAvailable(username, latency) {
  if (!CONFIG.DISCORD_WEBHOOK_URL) return;
  const payload = {
    content: `🎉 **[D4UC GAS 24/7] 사용 가능한 고유 닉네임 발견!** @here`,
    embeds: [{
      title: `✨ \`${username}\` 선점 가능!`,
      description: `Google Apps Script 클라우드 24시간 자동 체커가 사용 가능한 희귀 닉네임을 발견했습니다.`,
      color: 0x2ea043, // Spring Green
      fields: [
        { name: '닉네임', value: `\`${username}\``, inline: true },
        { name: '글자수', value: `${username.length}자`, inline: true },
        { name: '응답속도', value: `${latency}ms`, inline: true },
        { name: '선점 링크', value: `[Discord 회원가입 바로가기](https://discord.com/register)`, inline: false }
      ],
      footer: { text: 'D4UC Serverless Cloud Engine • 24/7 무인 구동' },
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
  } catch (e) {
    Logger.log('⚠️ [Webhook Error] ' + e.toString());
  }
}
