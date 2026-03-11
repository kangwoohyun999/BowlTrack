# 🎳 BowlTrack — 볼링 기록 웹앱

## 빠른 실행 방법

### 1. 패키지 설치
```bash
pip install flask
```

### 2. 서버 실행
```bash
python app.py
```

### 3. 브라우저에서 접속
```
http://localhost:5000
```

---

## 파일 구조
```
bowling_app/
├── app.py              # Flask 서버 (백엔드)
├── data.json           # 자동 생성되는 사용자 데이터 파일
├── requirements.txt
└── templates/
    ├── base.html       # 공통 레이아웃 (상단바, 하단 네비게이션)
    ├── login.html      # 로그인 페이지
    ├── register.html   # 회원가입 페이지
    ├── home.html       # 홈 (3개 메뉴 박스)
    ├── calendar.html   # 볼링 점수 달력 기록
    ├── stats.html      # 투구 통계 (스트라이크/스페어/미스 확률)
    ├── info.html       # 볼링 정보 (쇼핑몰, 구질별 장단점, 팁)
    ├── profile.html    # 프로필 설정
    └── settings.html   # 앱 설정 (구질 선택, 다크모드)
```

## 기능
- ✅ 로그인 / 회원가입
- ✅ 홈 화면: 구질 배지, 3가지 메뉴 박스
- ✅ 달력 점수 기록: 날짜별 점수 + 스트라이크/스페어/미스 횟수 + 메모
- ✅ 투구 통계: 도넛 차트 + 확률 바
- ✅ 볼링 정보: 쇼핑몰 링크, 구질별 장단점, 꿀팁
- ✅ 프로필: 닉네임 / 상태메시지 편집, 로그아웃
- ✅ 설정: 구질 선택, 다크모드 전환

## Node.js 다운로드
https://nodejs.org/ko/download/
접속 후 20.xx.xx 버전 선택 후 다운로드

## npm 다운로드
터미널창에서 npm install npx -g

## 📌 expo 다운로드
* npm install expo

## ✅ 버전 오류 해결 방법
### 1번
* npm uninstall @expo/webpack-config
### 2번
* @expo/webpack-config@19.0.3
* npm install @expo/webpack-config@19.0.3 --save-dev
### ⚠️ 절대로 하면 안 되는 것
* npm install --force
* npm install --legacy-peer-deps

## 📌 expo fix
* npm audit fix
* npm audit fix --force

## 📌 라이브러리 설치
* npm install react-native-chart-kit
* npm install @react-native-async-storage/async-storage
* npx expo install expo-font
* npx expo install react-native-svg
* npx expo install expo-linear-gradient
* npm install victory
* npm install victory-native
* npx expo install react-native-svg
### 웹
* npx expo install @expo/webpack-config@^18.0.1

## 📌 Expo 실행
* npx expo start

## 🍎 iOS 설치 및 실행 가이드
📋 사전 요구사항
macOS에서 실행 시:

macOS Catalina (10.15) 이상
Xcode 14.0 이상
CocoaPods 1.11 이상
Node.js 16 이상

Windows에서 실행 시:

Expo Go 앱만 사용 가능 (시뮬레이터 불가)

## 📌 ios 필수 라이브러리
* npx pod-install ios
* npm install react-native-reanimated@~2.14.4
* npm install react-native-safe-area-context@4.5.0
* npx expo install expo-build-properties

## ios 오류 시 해결 방법
### 1. 완전히 클린 설치
* rm -rf node_modules
* rm -rf .expo
* rm -rf ios
* rm package-lock.json
* npm cache clean --force

### 2. 재설치
* npm install

### 3. Metro 캐시 클리어하고 재시작
* npx expo start -c

### 4. iOS에서 실행
* npx expo start --ios
