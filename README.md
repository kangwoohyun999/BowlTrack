# 🎳 BowlTrack — 볼링 기록 웹앱

## Railway 배포 순서 (처음부터 끝까지)

```
https://web-production-c2004.up.railway.app/
```

### 1단계 — GitHub 레포 만들기
1. [github.com](https://github.com) 접속 → 로그인
2. 우상단 `+` → **New repository**
3. Repository name: `bowling-app` → **Create repository**
4. 다운받은 zip 압축 해제 후 아래 명령어 실행:
```bash
cd bowling_app
git init
git add .
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/[내아이디]/bowling-app.git
git push -u origin main
```

### 2단계 — Railway 프로젝트 생성
1. [railway.app](https://railway.app) 접속 → **GitHub으로 로그인**
2. **New Project** 클릭
3. **Deploy from GitHub repo** → `bowling-app` 선택
4. 자동으로 배포 시작됨 (아직 DB 없어서 에러 남 — 정상)

### 3단계 — PostgreSQL DB 추가
1. Railway 프로젝트 화면에서 **+ New** 클릭
2. **Database** → **Add PostgreSQL** 선택
3. PostgreSQL 서비스가 생성되면 클릭
4. **Variables** 탭 → `DATABASE_URL` 값 복사해두기

### 4단계 — 환경변수 설정
1. Railway에서 웹앱 서비스(bowling-app) 클릭
2. **Variables** 탭 → **New Variable** 클릭
3. 아래 두 개 추가:

| 키 | 값 |
|---|---|
| `DATABASE_URL` | (3단계에서 복사한 값) |
| `SECRET_KEY` | (아무 랜덤 문자열, 예: `my_super_secret_123`) |

4. **Deploy** 자동 재시작됨

### 5단계 — 도메인 확인
1. 웹앱 서비스 → **Settings** → **Networking**
2. **Generate Domain** 클릭
3. `https://bowling-app-xxxx.railway.app` 형태의 주소 생성
4. 접속 완료! 🎉

---

## 로컬 테스트 방법 (선택)
```bash
pip install flask gunicorn psycopg2-binary

# PostgreSQL이 없으면 로컬 테스트 불가
# Railway에서 DATABASE_URL 복사 후:
export DATABASE_URL="postgresql://..."
export SECRET_KEY="test_secret"
python app.py
# → http://localhost:5000
```

---

## 파일 구조
```
bowling_app/
├── app.py              # Flask 서버 (PostgreSQL 연동)
├── Procfile            # Railway/Heroku 실행 명령
├── runtime.txt         # Python 버전
├── requirements.txt    # 패키지 목록
└── templates/
    ├── base.html       # 공통 레이아웃
    ├── login.html      # 로그인
    ├── register.html   # 회원가입
    ├── home.html       # 홈
    ├── calendar.html   # 달력 기록
    ├── stats.html      # 투구 통계
    ├── info.html       # 볼링 정보
    ├── profile.html    # 프로필
    └── settings.html   # 설정
```

## DB 구조
```sql
users   — 사용자 정보 (username, password, nickname, style, dark_mode, strikes, spares, misses)
records — 날짜별 볼링 기록 (username, date, score, note, strikes, spares, misses)
```
