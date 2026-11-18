# 🚀 D4UC 깃허브(GitHub) 안전 푸시 및 배포 가이드

이 폴더(`github-ready/`)는 **실제 결제 계정 정보, 유료 WireGuard 개인키, 스크랩 결과 텍스트, SQLite 데이터베이스가 100% 안전하게 제거된 공식 깃허브 배포용 클린 패키지**입니다.

이 폴더의 소스코드는 **공개(Public) 저장소로 올려도 서프샤크 계정이 정지되거나 개인키가 털릴 위험이 0%**입니다.

---

## 📌 방법 1: 기존 저장소(`Discord-4Character-Usernames-Checker`)에서 바로 푸시하기

이미 로컬 저장소의 `.gitignore`와 소스코드에서 시크릿이 완벽하게 차단되었으므로, 터미널에서 바로 푸시할 수 있습니다:

```bash
# 1. 저장소 폴더로 이동
cd Discord-4Character-Usernames-Checker

# 2. 변경 사항 확인 (시크릿이나 결과 파일이 안 들어가는지 확인)
git status

# 3. 모든 안전한 클린 소스코드 스테이징
git add .

# 4. 커밋 생성
git commit -m "feat: D4UC v12 multi-platform release (TLS stealth, Docker, Termux & architecture mapping)"

# 5. 깃허브 푸시
git push origin main
```

---

## 📌 방법 2: 신규 깃허브 저장소를 새로 만들어 `github-ready/`를 올리기

새로운 깃허브 저장소(Public 또는 Private)를 파서 깔끔하게 새로 시작하고 싶을 때:

```bash
# 1. 저장소 폴더로 이동
cd discord-checker

# 2. 깃 저장소 초기화
git init

# 3. 모든 파일 스테이징 및 초기 커밋
git add .
git commit -m "Initial commit: D4UC v12 production release"

# 4. 기본 브랜치를 main으로 설정
git branch -M main

# 5. 내 깃허브 저장소 원격(remote) 주소 연결
# (주의: 아래 URL을 본인의 실제 깃허브 저장소 주소로 바꾸세요)
git remote add origin https://github.com/KRCUPRO/discord-checker.git

# 6. 푸시 실행
git push -u origin main
```

---

## 🔑 배포 후 다른 컴퓨터나 사용자가 쓸 때의 세팅법

깃허브에서 코드를 클론(다운로드)한 사람은 아래 방법으로 본인 서프샤크 키를 넣어 실행합니다:

1. **`.env` 파일 생성**:
   ```bash
   cp .env.example .env
   ```
2. **`.env` 파일에 본인 키 입력**:
   ```ini
   SURFSHARK_PRIVATE_KEYS=본인의_와이어가드_개인키_입력
   ```
3. **실행**:
   - 데스크톱 GUI: `python gui_ko.py`
   - CLI: `python run.py`
   - 도커: `docker compose up -d`
