"""
Message Handlers for Telegram Channel Bot

Handles all incoming messages from the owner including:
- Text messages
- Photos
- Videos
- Documents

Only the owner can post content to the channel.
"""

from telegram import Update
from telegram.ext import ContextTypes

from config import Config, Messages
from utils.logger import (
    log_message_received, 
    log_content_posted, 
    log_error
)
from middleware.antispam import owner_only


# ============================================
# Helper: Post Content to Channel
# ============================================

async def post_to_channel(
    update: Update, 
    context: ContextTypes.DEFAULT_TYPE,
    content_type: str
) -> bool:
    """
    Post content to the target channel.
    
    Args:
        update: Telegram update object
        context: Bot context object
        content_type: Type of content being posted
        
    Returns:
        bool: True if posted successfully, False otherwise
    """
    try:
        target_channel = Config.get_target_channel()
        message = update.message
        
        if not message:
            return False
        
        # Handle different content types
        if content_type == 'text':
            # Post text message
            await context.bot.send_message(
                chat_id=target_channel,
                text=message.text,
                parse_mode='HTML' if message.text_html else None,
                disable_web_page_preview=False
            )
            
        elif content_type == 'photo':
            # Get the largest photo
            photo = message.photo[-1]  # Last item is the largest
            
            # Handle caption removal option
            caption = message.caption if not Config.REMOVE_CAPTIONS else None
            
            await context.bot.send_photo(
                chat_id=target_channel,
                photo=photo.file_id,
                caption=caption,
                parse_mode='HTML' if caption and message.caption_html else None
            )
            
        elif content_type == 'video':
            # Handle caption removal option
            caption = message.caption if not Config.REMOVE_CAPTIONS else None
            
            await context.bot.send_video(
                chat_id=target_channel,
                video=message.video.file_id,
                caption=caption,
                parse_mode='HTML' if caption and message.caption_html else None,
                supports_streaming=True
            )
            
        elif content_type == 'document':
            # Handle caption removal option
            caption = message.caption if not Config.REMOVE_CAPTIONS else None
            
            await context.bot.send_document(
                chat_id=target_channel,
                document=message.document.file_id,
                caption=caption,
                parse_mode='HTML' if caption and message.caption_html else None
            )
        
        else:
            log_error(f"Unknown content type: {content_type}", update.effective_user.id)
            return False
        
        # Log successful post
        log_content_posted(update.effective_user.id, content_type, target_channel)
        
        # Confirm to owner
        await message.reply_text(
            Messages.POST_SUCCESS,
            parse_mode='HTML'
        )
        
        return True
        
    except Exception as e:
        log_error(f"Failed to post {content_type}", update.effective_user.id, e)
        await update.message.reply_text(
            f"{Messages.ERROR}\n\n<i>Error: {str(e)}</i>",
            parse_mode='HTML'
        )
        return False


# ============================================
# Handler: Text Messages
# ============================================

@owner_only
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle text messages from the owner.
    Posts the text to the channel.
    
    Args:
        update: Telegram update object
        context: Bot context object
    """
    if not update.message or not update.message.text:
        return
    
    user_id = update.effective_user.id
    text_preview = update.message.text[:50]
    
    # Log the received message
    log_message_received(user_id, 'text', text_preview)
    
    # Post to channel
    await post_to_channel(update, context, 'text')


# ============================================
# Handler: Photos
# ============================================

@owner_only
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle photo messages from the owner.
    Posts the photo to the channel.
    
    Args:
        update: Telegram update object
        context: Bot context object
    """
    if not update.message or not update.message.photo:
        return
    
    user_id = update.effective_user.id
    caption_preview = update.message.caption[:30] if update.message.caption else "(no caption)"
    
    # Log the received message
    log_message_received(user_id, 'photo', f"Caption: {caption_preview}")
    
    # Post to channel
    await post_to_channel(update, context, 'photo')


# ============================================
# Handler: Videos
# ============================================

@owner_only
async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle video messages from the owner.
    Posts the video to the channel.
    
    Args:
        update: Telegram update object
        context: Bot context object
    """
    if not update.message or not update.message.video:
        return
    
    user_id = update.effective_user.id
    caption_preview = update.message.caption[:30] if update.message.caption else "(no caption)"
    
    # Log the received message
    log_message_received(user_id, 'video', f"Caption: {caption_preview}")
    
    # Post to channel
    await post_to_channel(update, context, 'video')


# ============================================
# Handler: Documents
# ============================================

@owner_only
async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle document/file messages from the owner.
    Posts the document to the channel.
    
    Args:
        update: Telegram update object
        context: Bot context object
    """
    if not update.message or not update.message.document:
        return
    
    user_id = update.effective_user.id
    file_name = update.message.document.file_name or "unnamed"
    caption_preview = update.message.caption[:30] if update.message.caption else "(no caption)"
    
    # Log the received message
    log_message_received(user_id, 'document', f"File: {file_name}, Caption: {caption_preview}")
    
    # Post to channel
    await post_to_channel(update, context, 'document')
