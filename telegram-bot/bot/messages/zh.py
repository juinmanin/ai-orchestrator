"""Chinese messages for Telegram bot"""

WELCOME = """
👋 欢迎使用 AI Quota Orchestrator！

此机器人帮助您高效管理免费AI平台配额。

🔗 **连接方法:**
1. 在 https://open-crow.com 创建账户
2. 进入设置页面
3. 输入此连接代码:

`{chat_id}`

✅ 连接后，您将收到实时配额通知！

输入 /help 查看可用命令。
"""

HELP = """
📚 **可用命令:**

/start - 启动机器人并获取连接代码
/status - 检查当前配额状态
/recommend - 获取平台推荐
/schedule - 查看今日最佳使用计划
/settings - 配置通知
/lang - 更改语言
/help - 显示此帮助信息

💡 **提示:**
- 在配额重置前1小时收到自动提醒
- 在90%配额使用时收到警告
- 每晚收到每日使用摘要
"""

STATUS = """
📊 **配额状态**

{platform_list}

最后更新: {timestamp}
"""

STATUS_PLATFORM = """
{icon} **{name}**
└ {quota_type}: {used}/{total} ({percentage}%)
└ 重置: {reset_time}
"""

NO_ACCOUNTS = """
❌ 未找到已连接的账户。

请在 https://open-crow.com 连接您的AI平台账户！
"""

RECOMMENDATION = """
💡 **推荐平台**

{platform_name}
{reason}

备选方案:
{alternatives}
"""

SCHEDULE = """
📅 **今日推荐计划**

{schedule_items}

此计划已优化以最小化配额浪费。
"""

QUOTA_ALERT = """
⏰ **配额重置提醒！**

{platform_name} 配额将在 {time} 后重置！
剩余: {remaining}/{total}

立即使用以避免浪费！
"""

USAGE_WARNING = """
⚠️ **配额使用警告**

{platform_name} 配额使用量: {percentage}%
您正在接近限制！
"""

DAILY_SUMMARY = """
📊 **今日使用摘要**

{summary}

今日使用 {platforms_count} 个平台
"""

WEEKLY_REPORT = """
📈 **周报**

{weekly_stats}

💡 浪费分析:
{waste_analysis}
"""

ERROR = """
❌ 发生错误: {error}

请稍后重试。
"""

LANGUAGE_CHANGED = """
✅ 语言已更改为中文。
"""
