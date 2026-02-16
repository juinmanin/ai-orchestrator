"""Japanese messages for Telegram bot"""

WELCOME = """
👋 AI Quota Orchestratorへようこそ！

このボットは、無料のAIプラットフォームのクォータを効率的に管理するのに役立ちます。

🔗 **接続方法:**
1. https://open-crow.comでアカウントを作成してください
2. 設定ページに移動してください
3. この接続コードを入力してください:

`{chat_id}`

✅ 接続後、リアルタイムでクォータ通知を受け取れます！

/helpと入力してコマンドを確認してください。
"""

HELP = """
📚 **利用可能なコマンド:**

/start - ボット開始と接続コード確認
/status - 現在のクォータ状況確認
/recommend - おすすめのプラットフォーム推奨
/schedule - 今日の最適使用スケジュール
/settings - 通知設定
/lang - 言語変更
/help - このヘルプを表示

💡 **ヒント:**
- クォータリセット1時間前に自動通知
- クォータ90%使用時に警告
- 毎晩使用状況の要約を受信
"""

STATUS = """
📊 **クォータ状況**

{platform_list}

最終更新: {timestamp}
"""

STATUS_PLATFORM = """
{icon} **{name}**
└ {quota_type}: {used}/{total} ({percentage}%)
└ リセット: {reset_time}
"""

NO_ACCOUNTS = """
❌ 接続されたアカウントがありません。

https://open-crow.comでAIプラットフォームアカウントを接続してください！
"""

RECOMMENDATION = """
💡 **推奨プラットフォーム**

{platform_name}
{reason}

代替オプション:
{alternatives}
"""

SCHEDULE = """
📅 **今日の推奨スケジュール**

{schedule_items}

このスケジュールはクォータの無駄を最小限に抑えるよう最適化されています。
"""

QUOTA_ALERT = """
⏰ **クォータリセット間近！**

{platform_name}のクォータが{time}後にリセットされます！
残り: {remaining}/{total}

今すぐ使用して無駄を防ぎましょう！
"""

USAGE_WARNING = """
⚠️ **クォータ使用警告**

{platform_name}クォータの{percentage}%を使用しました。
制限に近づいています！
"""

DAILY_SUMMARY = """
📊 **今日の使用状況**

{summary}

合計{platforms_count}個のプラットフォームを使用
"""

WEEKLY_REPORT = """
📈 **週次レポート**

{weekly_stats}

💡 無駄の分析:
{waste_analysis}
"""

ERROR = """
❌ エラーが発生しました: {error}

後でもう一度お試しください。
"""

LANGUAGE_CHANGED = """
✅ 言語が日本語に変更されました。
"""
