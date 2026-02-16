"""Korean messages for Telegram bot"""

WELCOME = """
👋 안녕하세요! AI Quota Orchestrator에 오신 것을 환영합니다.

이 봇은 여러분의 AI 플랫폼 무료 쿼터를 효율적으로 관리하는 데 도움을 드립니다.

🔗 **연동 방법:**
1. https://open-crow.com에서 계정을 만드세요
2. 설정 페이지로 이동하세요
3. 아래 연동 코드를 입력하세요:

`{chat_id}`

✅ 연동 후 실시간 쿼터 알림을 받으실 수 있습니다!

명령어를 보려면 /help를 입력하세요.
"""

HELP = """
📚 **사용 가능한 명령어:**

/start - 봇 시작 및 연동 코드 확인
/status - 현재 쿼터 현황 확인
/recommend - 지금 사용하면 좋은 플랫폼 추천
/schedule - 오늘의 최적 사용 스케줄
/settings - 알림 설정
/lang - 언어 변경
/help - 이 도움말 표시

💡 **팁:**
- 쿼터 리셋 1시간 전에 자동 알림을 받습니다
- 쿼터 90% 사용 시 경고를 받습니다
- 매일 밤 사용 현황 요약을 받습니다
"""

STATUS = """
📊 **쿼터 현황**

{platform_list}

마지막 업데이트: {timestamp}
"""

STATUS_PLATFORM = """
{icon} **{name}**
└ {quota_type}: {used}/{total} ({percentage}%)
└ 리셋: {reset_time}
"""

NO_ACCOUNTS = """
❌ 연결된 계정이 없습니다.

https://open-crow.com에서 AI 플랫폼 계정을 연결하세요!
"""

RECOMMENDATION = """
💡 **추천 플랫폼**

{platform_name}
{reason}

대체 옵션:
{alternatives}
"""

SCHEDULE = """
📅 **오늘의 추천 스케줄**

{schedule_items}

이 스케줄은 쿼터 낭비를 최소화하기 위해 최적화되었습니다.
"""

QUOTA_ALERT = """
⏰ **쿼터 리셋 임박!**

{platform_name} 쿼터가 {time} 후 리셋됩니다!
잔여: {remaining}/{total}

지금 사용하여 낭비를 막으세요!
"""

USAGE_WARNING = """
⚠️ **쿼터 사용 경고**

{platform_name} 쿼터의 {percentage}%를 사용했습니다.
한도에 근접하고 있습니다!
"""

DAILY_SUMMARY = """
📊 **오늘의 사용 현황**

{summary}

총 {platforms_count}개 플랫폼 사용
"""

WEEKLY_REPORT = """
📈 **주간 리포트**

{weekly_stats}

💡 낭비 분석:
{waste_analysis}
"""

ERROR = """
❌ 오류가 발생했습니다: {error}

나중에 다시 시도해주세요.
"""

LANGUAGE_CHANGED = """
✅ 언어가 한국어로 변경되었습니다.
"""
