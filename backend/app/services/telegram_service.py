from typing import Optional, Dict
import httpx
from app.config import settings


class TelegramService:
    """Service for sending Telegram notifications"""
    
    def __init__(self):
        self.bot_token = settings.telegram_bot_token
        self.base_url = f"https://api.telegram.org/bot{self.bot_token}"
    
    async def send_message(self, chat_id: str, message: str, parse_mode: str = "HTML") -> bool:
        """Send a message to a Telegram chat"""
        if not self.bot_token or not chat_id:
            return False
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/sendMessage",
                    json={
                        "chat_id": chat_id,
                        "text": message,
                        "parse_mode": parse_mode
                    },
                    timeout=10.0
                )
                return response.status_code == 200
        except Exception as e:
            print(f"Error sending Telegram message: {e}")
            return False
    
    async def send_quota_alert(self, chat_id: str, platform_name: str, quota_info: Dict, language: str = "en"):
        """Send quota-related alert"""
        messages = {
            "en": "⏰ <b>{platform}</b> quota resets in {time}!\nRemaining: {remaining}/{total}\nUse it now to avoid waste!",
            "ko": "⏰ <b>{platform}</b> 쿼터가 {time} 후 리셋됩니다!\n잔여: {remaining}/{total}\n지금 사용하여 낭비를 막으세요!",
            "ja": "⏰ <b>{platform}</b>のクォータが{time}後にリセットされます！\n残り: {remaining}/{total}\n今すぐ使用して無駄を防ぎましょう！",
            "zh": "⏰ <b>{platform}</b> 配额将在 {time} 后重置！\n剩余: {remaining}/{total}\n立即使用以避免浪费！",
        }
        
        template = messages.get(language, messages["en"])
        message = template.format(
            platform=platform_name,
            time=quota_info.get("time_until_reset", "soon"),
            remaining=quota_info.get("remaining_quota", 0),
            total=quota_info.get("total_quota", 0)
        )
        
        await self.send_message(chat_id, message)
    
    async def send_usage_warning(self, chat_id: str, platform_name: str, usage_percentage: float, language: str = "en"):
        """Send usage warning when approaching quota limit"""
        messages = {
            "en": "⚠️ <b>{platform}</b> quota usage: {percentage}%\nYou're approaching the limit!",
            "ko": "⚠️ <b>{platform}</b> 쿼터 사용량: {percentage}%\n한도에 근접하고 있습니다!",
            "ja": "⚠️ <b>{platform}</b>クォータ使用量: {percentage}%\n制限に近づいています！",
            "zh": "⚠️ <b>{platform}</b> 配额使用量: {percentage}%\n您正在接近限制！",
        }
        
        template = messages.get(language, messages["en"])
        message = template.format(
            platform=platform_name,
            percentage=round(usage_percentage, 1)
        )
        
        await self.send_message(chat_id, message)


# Singleton instance
telegram_service = TelegramService()
