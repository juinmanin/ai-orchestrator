# AI Quota Orchestrator

[한국어](#한국어) | [English](#english)

---

## 한국어

### 개요

AI 플랫폼 무료 쿼터를 낭비 없이 최대한 활용할 수 있도록 안내하는 스마트 오케스트레이션 플랫폼입니다.

### 주요 기능

- 📊 **통합 쿼터 대시보드**: 모든 AI 플랫폼의 쿼터를 한눈에 확인
- 🤖 **텔레그램 실시간 알림**: 쿼터 리셋 임박, 사용량 경고, 최적 사용 추천
- 🧠 **스마트 추천 엔진**: AI 기반 최적 플랫폼 추천
- 🔒 **안전한 관리**: Fernet 암호화를 통한 API 키 보안 저장
- 🌍 **9개 언어 지원**: 한국어, 영어, 일본어, 중국어, 힌디어, 프랑스어, 스페인어, 말레이어, 베트남어
- 📋 **플랫폼별 가이드**: 각 AI 플랫폼 계정 생성 및 설정 단계별 안내

### 지원 플랫폼

- ChatGPT Free (50 메시지/3시간)
- Google Gemini Free (60 req/분, 1500 req/일)
- Claude Free (30 메시지/일)
- Leonardo AI Free (150 토큰/일)
- Hugging Face Free (제한적 무료)
- Cohere Free (1000 호출/월)

### 기술 스택

- **Backend**: Python FastAPI, SQLAlchemy, SQLite
- **Frontend**: Next.js 15, React 19, TypeScript, Tailwind CSS
- **Telegram Bot**: python-telegram-bot, APScheduler
- **Security**: JWT, bcrypt, Fernet encryption
- **Deployment**: Docker Compose, Nginx

### 빠른 시작

#### 사전 요구사항

- Docker 및 Docker Compose 설치
- 도메인 (선택사항, 로컬 테스트는 localhost 사용)

#### 설치 단계

1. **저장소 클론**

```bash
git clone https://github.com/juinmanin/ai-orchestrator.git
cd ai-orchestrator
```

2. **환경 변수 설정**

```bash
cp .env.example .env
```

`.env` 파일을 편집하여 다음 값을 설정하세요:

```bash
# 암호화 키 (32자 이상의 랜덤 문자열)
ENCRYPTION_KEY=your-secure-encryption-key-32-chars-min

# JWT 시크릿 (랜덤 문자열)
JWT_SECRET=your-secure-jwt-secret

# 텔레그램 봇 토큰 (BotFather에서 받기)
TELEGRAM_BOT_TOKEN=your-telegram-bot-token
```

3. **Docker Compose로 실행**

```bash
docker-compose up -d
```

4. **접속**

- 프론트엔드: http://localhost (포트 80)
- 백엔드 API: http://localhost/api
- API 문서: http://localhost/api/docs

### 텔레그램 봇 설정

1. **봇 생성**
   - Telegram에서 [@BotFather](https://t.me/botfather) 검색
   - `/newbot` 명령 실행
   - 봇 이름과 사용자명 설정
   - 받은 토큰을 `.env` 파일의 `TELEGRAM_BOT_TOKEN`에 입력

2. **봇 연동**
   - 텔레그램에서 봇 검색 및 `/start` 실행
   - 표시된 연동 코드 복사
   - 웹사이트 설정 페이지에서 코드 입력

### open-crow.com 도메인 설정

#### DNS 설정

도메인 제공업체에서 A 레코드 추가:

```
Type: A
Name: @
Value: <your-server-ip>

Type: A
Name: www
Value: <your-server-ip>
```

#### SSL 인증서 설정 (Let's Encrypt)

```bash
# Certbot 설치
apt-get update
apt-get install certbot python3-certbot-nginx

# 인증서 발급
certbot --nginx -d open-crow.com -d www.open-crow.com

# 자동 갱신 설정
certbot renew --dry-run
```

`nginx/nginx.conf`에서 HTTPS 섹션의 주석을 해제하고 다시 시작:

```bash
docker-compose restart nginx
```

### 개발 환경 설정

#### Backend 개발

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

#### Frontend 개발

```bash
cd frontend
npm install
npm run dev
```

#### Telegram Bot 개발

```bash
cd telegram-bot
pip install -r requirements.txt
python -m bot.main
```

### API 문서

서버 실행 후 http://localhost/api/docs 에서 Swagger UI를 통해 전체 API 문서를 확인할 수 있습니다.

주요 엔드포인트:

- `POST /api/auth/register` - 회원가입
- `POST /api/auth/login` - 로그인
- `GET /api/accounts` - 연결된 계정 목록
- `POST /api/accounts` - 계정 추가 (API 키 암호화 저장)
- `GET /api/quota/dashboard` - 쿼터 대시보드
- `GET /api/quota/recommendations` - 추천 플랫폼
- `GET /api/guides` - 플랫폼 가이드 목록

### 보안

- **API 키 암호화**: 모든 API 키는 Fernet (AES-128-CBC) 방식으로 암호화되어 저장됩니다
- **비밀번호 해싱**: bcrypt를 사용한 안전한 비밀번호 해싱
- **JWT 인증**: 토큰 기반 인증으로 세션 관리
- **사용 로그**: 모든 중요 작업에 대한 감사 로그 기록
- **보안 업데이트**: 모든 의존성이 최신 보안 패치 버전으로 업데이트됨 (2026-02-16)
  - cryptography 46.0.5 (취약점 수정)
  - fastapi 0.115.6 (ReDoS 취약점 수정)
  - python-multipart 0.0.22 (파일 쓰기 취약점 수정)
  - next 15.0.8 (DoS 취약점 수정, React 19 포함)
  - react 19.0.0 (Next.js 15 필수 요구사항)

**보안 권장사항**: 정기적으로 `SECURITY.md` 파일을 확인하여 보안 업데이트를 적용하세요.

### 기여하기

Pull Request를 환영합니다! 주요 변경사항의 경우 먼저 이슈를 열어 논의해주세요.

### 라이선스

MIT License

### 문의

- Website: https://open-crow.com
- Issues: https://github.com/juinmanin/ai-orchestrator/issues

---

## English

### Overview

A smart orchestration platform to help users maximize their free AI platform quotas without waste.

### Key Features

- 📊 **Unified Quota Dashboard**: Monitor all AI platform quotas at a glance
- 🤖 **Telegram Real-time Notifications**: Reset alerts, usage warnings, and recommendations
- 🧠 **Smart Recommendation Engine**: AI-powered optimal platform suggestions
- 🔒 **Secure Management**: API keys encrypted with Fernet encryption
- 🌍 **9 Language Support**: Korean, English, Japanese, Chinese, Hindi, French, Spanish, Malay, Vietnamese
- 📋 **Platform Guides**: Step-by-step guides for each AI platform

### Supported Platforms

- ChatGPT Free (50 messages/3 hours)
- Google Gemini Free (60 req/min, 1500 req/day)
- Claude Free (30 messages/day)
- Leonardo AI Free (150 tokens/day)
- Hugging Face Free (Limited free tier)
- Cohere Free (1000 calls/month)

### Tech Stack

- **Backend**: Python FastAPI, SQLAlchemy, SQLite
- **Frontend**: Next.js 15, React 19, TypeScript, Tailwind CSS
- **Telegram Bot**: python-telegram-bot, APScheduler
- **Security**: JWT, bcrypt, Fernet encryption
- **Deployment**: Docker Compose, Nginx

### Quick Start

#### Prerequisites

- Docker and Docker Compose installed
- Domain name (optional, use localhost for local testing)

#### Installation Steps

1. **Clone the repository**

```bash
git clone https://github.com/juinmanin/ai-orchestrator.git
cd ai-orchestrator
```

2. **Configure environment variables**

```bash
cp .env.example .env
```

Edit the `.env` file with your values:

```bash
# Encryption key (random string, 32+ chars)
ENCRYPTION_KEY=your-secure-encryption-key-32-chars-min

# JWT secret (random string)
JWT_SECRET=your-secure-jwt-secret

# Telegram bot token (from BotFather)
TELEGRAM_BOT_TOKEN=your-telegram-bot-token
```

3. **Run with Docker Compose**

```bash
docker-compose up -d
```

4. **Access the application**

- Frontend: http://localhost (port 80)
- Backend API: http://localhost/api
- API Docs: http://localhost/api/docs

### Telegram Bot Setup

1. **Create a bot**
   - Search for [@BotFather](https://t.me/botfather) on Telegram
   - Run `/newbot` command
   - Set bot name and username
   - Copy the token to `.env` file as `TELEGRAM_BOT_TOKEN`

2. **Connect the bot**
   - Search for your bot on Telegram and run `/start`
   - Copy the connection code displayed
   - Enter the code in the Settings page on the website

### open-crow.com Domain Setup

#### DNS Configuration

Add A records in your domain provider:

```
Type: A
Name: @
Value: <your-server-ip>

Type: A
Name: www
Value: <your-server-ip>
```

#### SSL Certificate Setup (Let's Encrypt)

```bash
# Install Certbot
apt-get update
apt-get install certbot python3-certbot-nginx

# Obtain certificate
certbot --nginx -d open-crow.com -d www.open-crow.com

# Setup auto-renewal
certbot renew --dry-run
```

Uncomment the HTTPS section in `nginx/nginx.conf` and restart:

```bash
docker-compose restart nginx
```

### Development Setup

#### Backend Development

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

#### Frontend Development

```bash
cd frontend
npm install
npm run dev
```

#### Telegram Bot Development

```bash
cd telegram-bot
pip install -r requirements.txt
python -m bot.main
```

### API Documentation

After starting the server, visit http://localhost/api/docs for full API documentation via Swagger UI.

Key endpoints:

- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `GET /api/accounts` - List connected accounts
- `POST /api/accounts` - Add account (API key encrypted)
- `GET /api/quota/dashboard` - Quota dashboard
- `GET /api/quota/recommendations` - Platform recommendations
- `GET /api/guides` - Platform guide list

### Security

- **API Key Encryption**: All API keys are encrypted using Fernet (AES-128-CBC)
- **Password Hashing**: Secure password hashing with bcrypt
- **JWT Authentication**: Token-based authentication for session management
- **Usage Logging**: Audit logs for all critical operations
- **Security Updates**: All dependencies updated to latest secure versions (2026-02-16)
  - cryptography 46.0.5 (vulnerability fixes)
  - fastapi 0.115.6 (ReDoS vulnerability fix)
  - python-multipart 0.0.22 (file write vulnerability fix)
  - next 15.0.8 (DoS vulnerability fix, includes React 19)
  - react 19.0.0 (required for Next.js 15)

**Security Recommendation**: Regularly check `SECURITY.md` file for security updates.

### Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

### License

MIT License

### Contact

- Website: https://open-crow.com
- Issues: https://github.com/juinmanin/ai-orchestrator/issues