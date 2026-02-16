import os
import logging
from telegram.ext import Application, CommandHandler
from bot.handlers import (
    start_command,
    help_command,
    status_command,
    recommend_command,
    schedule_command,
    settings_command,
    lang_command,
    error_handler
)
from bot.scheduler import get_scheduler

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def main():
    """Start the bot"""
    # Get bot token from environment
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    
    if not token:
        logger.error("TELEGRAM_BOT_TOKEN environment variable not set")
        return
    
    # Create application
    application = Application.builder().token(token).build()
    
    # Add command handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("status", status_command))
    application.add_handler(CommandHandler("recommend", recommend_command))
    application.add_handler(CommandHandler("schedule", schedule_command))
    application.add_handler(CommandHandler("settings", settings_command))
    application.add_handler(CommandHandler("lang", lang_command))
    
    # Add error handler
    application.add_error_handler(error_handler)
    
    # Start scheduler
    scheduler = get_scheduler(application.bot)
    scheduler.start()
    
    logger.info("Starting bot...")
    
    # Run the bot
    application.run_polling(allowed_updates=["message", "callback_query"])


if __name__ == "__main__":
    main()
