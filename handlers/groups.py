"""
Group Handlers for Telegram Channel Bot

Handles events when the bot is added to groups including:
- Sending welcome message with channel promotion
- Detecting when bot is added to a new group
"""

from telegram import Update
from telegram.ext import ContextTypes

from config import Config
from utils.logger import log_channel_link_shared
from utils.keyboards import get_join_channel_keyboard, format_group_welcome


# ============================================
# Handler: New Chat Member (Bot Added)
# ============================================

async def handle_new_chat_member(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle when the bot is added to a group.
    Sends a welcome message with channel promotion.
    
    Args:
        update: Telegram update object
        context: Bot context object
    """
    if not update.message or not update.message.new_chat_members:
        return
    
    # Check if bot itself was added
    bot = await context.bot.get_me()
    bot_added = any(
        member.id == bot.id 
        for member in update.message.new_chat_members
    )
    
    if not bot_added:
        return
    
    # Get chat information
    chat = update.effective_chat
    chat_id = chat.id
    chat_title = chat.title or "this group"
    chat_type = chat.type
    
    # Log the event
    log_channel_link_shared(
        user_id=chat_id,
        chat_type=chat_type,
        chat_title=chat_title
    )
    
    # Send welcome message to the group
    try:
        await context.bot.send_message(
            chat_id=chat_id,
            text=format_group_welcome(),
            parse_mode='HTML',
            reply_markup=get_join_channel_keyboard(),
            disable_web_page_preview=True
        )
    except Exception as e:
        # Bot might not have permission to send messages
        from utils.logger import log_error
        log_error(
            f"Could not send welcome message to group {chat_title}",
            chat_id,
            e
        )


# ============================================
# Handler: Bot Joined Chat (Alternative)
# ============================================

async def handle_bot_added(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Alternative handler for when bot joins a chat.
    This handles the my_chat_member update.
    
    Args:
        update: Telegram update object
        context: Bot context object
    """
    if not update.my_chat_member:
        return
    
    # Check if bot was just added to a group
    old_status = update.my_chat_member.old_chat_member.status
    new_status = update.my_chat_member.new_chat_member.status
    
    # Bot was just added if old status was 'left' or 'kicked' and new is 'member' or 'administrator'
    was_added = (
        old_status in ['left', 'kicked'] and 
        new_status in ['member', 'administrator']
    )
    
    if not was_added:
        return
    
    chat = update.effective_chat
    
    # Only handle groups (not private chats)
    if chat.type not in ['group', 'supergroup']:
        return
    
    chat_id = chat.id
    chat_title = chat.title or "this group"
    chat_type = chat.type
    
    # Log the event
    log_channel_link_shared(
        user_id=chat_id,
        chat_type=chat_type,
        chat_title=chat_title
    )
    
    # Send welcome message
    try:
        await context.bot.send_message(
            chat_id=chat_id,
            text=format_group_welcome(),
            parse_mode='HTML',
            reply_markup=get_join_channel_keyboard(),
            disable_web_page_preview=True
        )
    except Exception as e:
        from utils.logger import log_error
        log_error(
            f"Could not send welcome message to group {chat_title}",
            chat_id,
            e
        )


# ============================================
# Handler: Group Left/Removed
# ============================================

async def handle_bot_removed(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle when the bot is removed from a group.
    Logs the event for monitoring purposes.
    
    Args:
        update: Telegram update object
        context: Bot context object
    """
    if not update.my_chat_member:
        return
    
    old_status = update.my_chat_member.old_chat_member.status
    new_status = update.my_chat_member.new_chat_member.status
    
    # Bot was removed if old status was 'member' or 'administrator' and new is 'left' or 'kicked'
    was_removed = (
        old_status in ['member', 'administrator'] and 
        new_status in ['left', 'kicked']
    )
    
    if not was_removed:
        return
    
    chat = update.effective_chat
    chat_id = chat.id
    chat_title = chat.title or "Unknown"
    
    # Log the removal
    from utils.logger import log_event
    log_event(
        'bot_removed',
        f"Bot removed from group '{chat_title}' (status: {new_status})",
        chat_id
    )
