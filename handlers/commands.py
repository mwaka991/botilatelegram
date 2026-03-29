"""
Command Handlers for Telegram Channel Bot

Handles all bot commands including:
- /start - Welcome message and channel promotion
- /help - Help instructions
- /channel - Channel link promotion
"""

from telegram import Update
from telegram.ext import ContextTypes

from config import Config, Messages
from utils.logger import log_channel_link_shared
from utils.keyboards import (
    get_join_channel_keyboard, 
    format_welcome_message,
    format_channel_promo
)
from middleware.antispam import spam_protected


# ============================================
# Command: /start
# ============================================

@spam_protected
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle the /start command.
    Sends welcome message with channel promotion and join button.
    
    Args:
        update: Telegram update object
        context: Bot context object
    """
    if not update.effective_user:
        return
    
    user_id = update.effective_user.id
    user_name = update.effective_user.first_name
    
    # Format welcome message with user's name
    welcome_text = format_welcome_message()
    
    # Send welcome message with join channel button
    await update.message.reply_text(
        welcome_text,
        parse_mode='HTML',
        reply_markup=get_join_channel_keyboard(),
        disable_web_page_preview=True
    )
    
    # Log the interaction
    log_channel_link_shared(user_id, 'private')


# ============================================
# Command: /help
# ============================================

@spam_protected
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle the /help command.
    Sends help instructions to the user.
    
    Args:
        update: Telegram update object
        context: Bot context object
    """
    await update.message.reply_text(
        Messages.HELP,
        parse_mode='HTML',
        reply_markup=get_join_channel_keyboard(),
        disable_web_page_preview=True
    )


# ============================================
# Command: /channel
# ============================================

@spam_protected
async def channel_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle the /channel command.
    Sends channel promotion message with join button.
    
    Args:
        update: Telegram update object
        context: Bot context object
    """
    if not update.effective_user:
        return
    
    user_id = update.effective_user.id
    
    # Send channel promotion
    await update.message.reply_text(
        format_channel_promo(),
        parse_mode='HTML',
        reply_markup=get_join_channel_keyboard(),
        disable_web_page_preview=True
    )
    
    # Log the link share
    log_channel_link_shared(user_id, 'private')
