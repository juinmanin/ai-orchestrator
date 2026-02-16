from telegram import Update
from telegram.ext import ContextTypes
import httpx
import os
from datetime import datetime

# Import message modules
from bot.messages import ko, en, ja, zh

# Language map
MESSAGES = {
    "ko": ko,
    "en": en,
    "ja": ja,
    "zh": zh,
    "hi": en,  # Fallback to English
    "fr": en,
    "es": en,
    "ms": en,
    "vi": en
}

API_BASE_URL = os.getenv("API_BASE_URL", "http://backend:8000")

# Store user language preferences (in production, this should be in a database)
user_languages = {}


def get_messages(chat_id: int):
    """Get message module for user's language"""
    lang = user_languages.get(chat_id, "en")
    return MESSAGES.get(lang, en)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    chat_id = update.effective_chat.id
    messages = get_messages(chat_id)
    
    welcome_text = messages.WELCOME.format(chat_id=chat_id)
    await update.message.reply_text(welcome_text, parse_mode="Markdown")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    chat_id = update.effective_chat.id
    messages = get_messages(chat_id)
    
    await update.message.reply_text(messages.HELP, parse_mode="Markdown")


async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /status command"""
    chat_id = update.effective_chat.id
    messages = get_messages(chat_id)
    
    try:
        # In production, we'd look up the user by chat_id
        # For now, send a generic response
        status_text = messages.NO_ACCOUNTS
        await update.message.reply_text(status_text, parse_mode="Markdown")
    
    except Exception as e:
        error_text = messages.ERROR.format(error=str(e))
        await update.message.reply_text(error_text, parse_mode="Markdown")


async def recommend_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /recommend command"""
    chat_id = update.effective_chat.id
    messages = get_messages(chat_id)
    
    try:
        # In production, fetch from API
        recommendation_text = messages.NO_ACCOUNTS
        await update.message.reply_text(recommendation_text, parse_mode="Markdown")
    
    except Exception as e:
        error_text = messages.ERROR.format(error=str(e))
        await update.message.reply_text(error_text, parse_mode="Markdown")


async def schedule_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /schedule command"""
    chat_id = update.effective_chat.id
    messages = get_messages(chat_id)
    
    try:
        # In production, fetch from API
        schedule_text = messages.NO_ACCOUNTS
        await update.message.reply_text(schedule_text, parse_mode="Markdown")
    
    except Exception as e:
        error_text = messages.ERROR.format(error=str(e))
        await update.message.reply_text(error_text, parse_mode="Markdown")


async def settings_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /settings command"""
    chat_id = update.effective_chat.id
    messages = get_messages(chat_id)
    
    settings_text = """
⚙️ **Settings**

Use these commands:
/lang - Change language

More settings available at https://open-crow.com/settings
"""
    await update.message.reply_text(settings_text, parse_mode="Markdown")


async def lang_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /lang command"""
    chat_id = update.effective_chat.id
    
    if context.args and len(context.args) > 0:
        lang = context.args[0].lower()
        if lang in MESSAGES:
            user_languages[chat_id] = lang
            messages = get_messages(chat_id)
            await update.message.reply_text(messages.LANGUAGE_CHANGED)
        else:
            await update.message.reply_text(
                f"Language '{lang}' not supported. Available: ko, en, ja, zh"
            )
    else:
        current_lang = user_languages.get(chat_id, "en")
        await update.message.reply_text(
            f"Current language: {current_lang}\n\n"
            f"Change with: /lang <code>\n"
            f"Available: ko, en, ja, zh, hi, fr, es, ms, vi"
        )


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle errors"""
    print(f"Update {update} caused error {context.error}")
    
    if update and update.effective_chat:
        chat_id = update.effective_chat.id
        messages = get_messages(chat_id)
        error_text = messages.ERROR.format(error="An unexpected error occurred")
        
        try:
            await update.message.reply_text(error_text, parse_mode="Markdown")
        except:
            pass
