from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime
import httpx
import os

API_BASE_URL = os.getenv("API_BASE_URL", "http://backend:8000")


class QuotaScheduler:
    """Scheduler for automatic quota notifications"""
    
    def __init__(self, bot):
        self.bot = bot
        self.scheduler = AsyncIOScheduler()
    
    def start(self):
        """Start the scheduler"""
        # Check quota resets every hour
        self.scheduler.add_job(
            self.check_quota_resets,
            IntervalTrigger(hours=1),
            id="quota_reset_check"
        )
        
        # Send daily summaries at 9 PM
        self.scheduler.add_job(
            self.send_daily_summaries,
            CronTrigger(hour=21, minute=0),
            id="daily_summary"
        )
        
        # Send weekly reports on Sundays at 8 PM
        self.scheduler.add_job(
            self.send_weekly_reports,
            CronTrigger(day_of_week="sun", hour=20, minute=0),
            id="weekly_report"
        )
        
        # Check usage warnings every 3 hours
        self.scheduler.add_job(
            self.check_usage_warnings,
            IntervalTrigger(hours=3),
            id="usage_warnings"
        )
        
        self.scheduler.start()
        print("Scheduler started successfully")
    
    def stop(self):
        """Stop the scheduler"""
        self.scheduler.shutdown()
        print("Scheduler stopped")
    
    async def check_quota_resets(self):
        """Check for upcoming quota resets and send alerts"""
        print(f"[{datetime.now()}] Checking quota resets...")
        
        try:
            # In production, this would:
            # 1. Query all users with telegram_chat_id
            # 2. Check their quota reset times
            # 3. Send alerts for quotas resetting in < 1 hour
            pass
        except Exception as e:
            print(f"Error checking quota resets: {e}")
    
    async def check_usage_warnings(self):
        """Check for high quota usage and send warnings"""
        print(f"[{datetime.now()}] Checking usage warnings...")
        
        try:
            # In production, this would:
            # 1. Query all users
            # 2. Check quota usage > 90%
            # 3. Send warnings
            pass
        except Exception as e:
            print(f"Error checking usage warnings: {e}")
    
    async def send_daily_summaries(self):
        """Send daily usage summaries"""
        print(f"[{datetime.now()}] Sending daily summaries...")
        
        try:
            # In production, this would:
            # 1. Query all users with telegram_chat_id
            # 2. Generate daily usage summary
            # 3. Send to each user in their preferred language
            pass
        except Exception as e:
            print(f"Error sending daily summaries: {e}")
    
    async def send_weekly_reports(self):
        """Send weekly usage reports"""
        print(f"[{datetime.now()}] Sending weekly reports...")
        
        try:
            # In production, this would:
            # 1. Query all users
            # 2. Generate weekly stats and waste analysis
            # 3. Send to each user
            pass
        except Exception as e:
            print(f"Error sending weekly reports: {e}")


# Singleton instance
_scheduler = None


def get_scheduler(bot):
    """Get or create scheduler instance"""
    global _scheduler
    if _scheduler is None:
        _scheduler = QuotaScheduler(bot)
    return _scheduler
