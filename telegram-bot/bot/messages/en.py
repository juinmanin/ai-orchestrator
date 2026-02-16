"""English messages for Telegram bot"""

WELCOME = """
👋 Welcome to AI Quota Orchestrator!

This bot helps you efficiently manage your free AI platform quotas.

🔗 **How to Connect:**
1. Create an account at https://open-crow.com
2. Go to the Settings page
3. Enter this connection code:

`{chat_id}`

✅ Once connected, you'll receive real-time quota notifications!

Type /help to see available commands.
"""

HELP = """
📚 **Available Commands:**

/start - Start bot and get connection code
/status - Check current quota status
/recommend - Get platform recommendations
/schedule - View today's optimal usage schedule
/settings - Configure notifications
/lang - Change language
/help - Show this help message

💡 **Tips:**
- Get automatic alerts 1 hour before quota resets
- Receive warnings at 90% quota usage
- Get daily usage summaries every evening
"""

STATUS = """
📊 **Quota Status**

{platform_list}

Last updated: {timestamp}
"""

STATUS_PLATFORM = """
{icon} **{name}**
└ {quota_type}: {used}/{total} ({percentage}%)
└ Resets: {reset_time}
"""

NO_ACCOUNTS = """
❌ No connected accounts found.

Connect your AI platform accounts at https://open-crow.com!
"""

RECOMMENDATION = """
💡 **Recommended Platform**

{platform_name}
{reason}

Alternatives:
{alternatives}
"""

SCHEDULE = """
📅 **Today's Recommended Schedule**

{schedule_items}

This schedule is optimized to minimize quota waste.
"""

QUOTA_ALERT = """
⏰ **Quota Reset Alert!**

{platform_name} quota resets in {time}!
Remaining: {remaining}/{total}

Use it now to avoid waste!
"""

USAGE_WARNING = """
⚠️ **Quota Usage Warning**

{platform_name} quota usage: {percentage}%
You're approaching the limit!
"""

DAILY_SUMMARY = """
📊 **Today's Usage Summary**

{summary}

Used {platforms_count} platforms today
"""

WEEKLY_REPORT = """
📈 **Weekly Report**

{weekly_stats}

💡 Waste Analysis:
{waste_analysis}
"""

ERROR = """
❌ An error occurred: {error}

Please try again later.
"""

LANGUAGE_CHANGED = """
✅ Language changed to English.
"""
