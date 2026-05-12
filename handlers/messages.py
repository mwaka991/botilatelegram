"""
Message Handlers for Telegram Channel Bot

Handles all incoming messages from the admin including:
- Text messages
- Photos
- Videos
- Documents

Only the admin can post content to channels.
Non-admin users receive a channel join link.
"""

from telegram import Update
from telegram.ext import ContextTypes

from config import Config, Messages
from utils.logger import (
    log_message_received,
    log_content_posted,
    log_error,
)
from utils.text_utils import remove_links
from middleware.antispam import owner_only


# ============================================
# Helper: Post Content to a Single Channel
# ============================================

async def post_content_to_single_channel(
    context: ContextTypes.DEFAULT_TYPE,
    content_type: str,
    channel_id: int,
    message,
) -> bool:
    """
    Post content to a single target channel.

    Args:
        context: Bot context object
        content_type: Type of content being posted
        channel_id: Target channel ID
        message: The original message object

    Returns:
        bool: True if posted successfully, False otherwise
    """
    try:
        if content_type == 'text':
            # Remove links from text before posting if enabled
            text_content = message.text
            if Config.REMOVE_LINKS:
                text_content = remove_links(text_content)
            
            await context.bot.send_message(
                chat_id=channel_id,
                text=text_content,
                parse_mode='HTML' if message.text_html else None,
                disable_web_page_preview=False,
            )

        elif content_type == 'photo':
            if not message.photo:
                log_error("No photo found in message", None)
                return False
            photo = message.photo[-1]
            # Remove links from caption if enabled
            caption = message.caption
            if caption and not Config.REMOVE_CAPTIONS and Config.REMOVE_LINKS:
                caption = remove_links(caption)
            elif not Config.REMOVE_CAPTIONS:
                caption = caption
            else:
                caption = None

            await context.bot.send_photo(
                chat_id=channel_id,
                photo=photo.file_id,
                caption=caption,
                parse_mode='HTML' if caption and message.caption_html else None,
            )

        elif content_type == 'video':
            # Remove links from caption if enabled
            caption = message.caption
            if caption and not Config.REMOVE_CAPTIONS and Config.REMOVE_LINKS:
                caption = remove_links(caption)
            elif not Config.REMOVE_CAPTIONS:
                caption = caption
            else:
                caption = None

            await context.bot.send_video(
                chat_id=channel_id,
                video=message.video.file_id,
                caption=caption,
                parse_mode='HTML' if caption and message.caption_html else None,
                supports_streaming=True,
            )

        elif content_type == 'document':
            # Remove links from caption if enabled
            caption = message.caption
            if caption and not Config.REMOVE_CAPTIONS and Config.REMOVE_LINKS:
                caption = remove_links(caption)
            elif not Config.REMOVE_CAPTIONS:
                caption = caption
            else:
                caption = None

            await context.bot.send_document(
                chat_id=channel_id,
                document=message.document.file_id,
                caption=caption,
                parse_mode='HTML' if caption and message.caption_html else None,
            )

        else:
            log_error(f"Unknown content type: {content_type}", None)
            return False

        return True

    except Exception as e:
        log_error(
            f"Failed to post {content_type} to channel {channel_id}",
            None,
            e,
        )
        return False


# ============================================
# Helper: Post Content to All Channels
# ============================================

async def post_to_all_channels(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    content_type: str,
) -> None:
    """
    Post content to all configured channels.
    Logs each success and failure. Sends a summary to the admin.

    Args:
        update: Telegram update object
        context: Bot context object
        content_type: Type of content being posted
    """
    message = update.message
    if not message:
        return

    user_id = update.effective_user.id
    success_count = 0
    failed_channels = []

    target_channels = Config.get_target_channels()
    for channel_id in target_channels:
        success = await post_content_to_single_channel(
            context, content_type, channel_id, message
        )
        if success:
            success_count += 1
            log_content_posted(user_id, content_type, str(channel_id))
        else:
            failed_channels.append(str(channel_id))

    # Send summary to admin
    if failed_channels:
        await message.reply_text(
            f"✅ Posted to {success_count}/{len(target_channels)} channels\n"
            f"❌ Failed: {', '.join(failed_channels)}",
            parse_mode='HTML',
        )
    else:
        await message.reply_text(
            Messages.POST_SUCCESS,
            parse_mode='HTML',
        )


# ============================================
# Handler: Text Messages
# ============================================

@owner_only
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle text messages from the admin.
    Posts the text to all configured channels.

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

    # Post to all channels
    await post_to_all_channels(update, context, 'text')


# ============================================
# Handler: Photos
# ============================================

@owner_only
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle photo messages from the admin.
    Posts the photo to all configured channels.

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

    # Post to all channels
    await post_to_all_channels(update, context, 'photo')


# ============================================
# Handler: Videos
# ============================================

@owner_only
async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle video messages from the admin.
    Posts the video to all configured channels.

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

    # Post to all channels
    await post_to_all_channels(update, context, 'video')


# ============================================
# Handler: Documents
# ============================================

@owner_only
async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle document/file messages from the admin.
    Posts the document to all configured channels.

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

    # Post to all channels
    await post_to_all_channels(update, context, 'document')
