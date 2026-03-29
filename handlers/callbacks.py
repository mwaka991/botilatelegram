"""
Callback Query Handlers for Telegram Channel Bot

Handles inline button callbacks including:
- Join Channel button
- About button
- Other interactive buttons
"""

from telegram import Update
from telegram.ext import ContextTypes

from config import Config, Messages
from utils.logger import log_event
from utils.keyboards import get_join_channel_keyboard, format_channel_promo


# ============================================
# Handler: Callback Queries
# ============================================

async def handle_callback_query(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle inline button callbacks.
    
    Args:
        update: Telegram update object
        context: Bot context object
    """
    if not update.callback_query:
        return
    
    query = update.callback_query
    user_id = update.effective_user.id if update.effective_user else None
    data = query.data
    
    # Answer the callback query immediately
    await query.answer()
    
    # Handle different callback data
    if data == 'about':
        await handle_about_callback(query, user_id)
    elif data == 'channel_link':
        await handle_channel_link_callback(query, user_id)
    else:
        # Unknown callback - log it
        log_event('unknown_callback', f"Unknown callback data: {data}", user_id)


# ============================================
# Handler: About Callback
# ============================================

async def handle_about_callback(query, user_id: int) -> None:
    """
    Handle the 'about' button callback.
    
    Args:
        query: Callback query object
        user_id: Telegram user ID
    """
    about_text = """
📋 <b>About This Bot</b>

This bot helps manage and promote our Telegram channel.

<b>Features:</b>
• Automatic content posting to channel
• Support for text, photos, videos, and documents
• Channel promotion with inline buttons
• Anti-spam protection

<b>For support or inquiries:</b>
Contact the bot administrator.

Thank you for using our bot! 🎉
"""
    
    await query.edit_message_text(
        text=about_text,
        parse_mode='HTML',
        reply_markup=get_join_channel_keyboard()
    )
    
    log_event('about_viewed', "User viewed about information", user_id)


# ============================================
# Handler: Channel Link Callback
# ============================================

async def handle_channel_link_callback(query, user_id: int) -> None:
    """
    Handle the 'channel_link' button callback.
    Resend the channel promotion message.
    
    Args:
        query: Callback query object
        user_id: Telegram user ID
    """
    await query.edit_message_text(
        text=format_channel_promo(),
        parse_mode='HTML',
        reply_markup=get_join_channel_keyboard(),
        disable_web_page_preview=True
    )
    
    log_event('channel_link_clicked', "User clicked channel link button", user_id)
