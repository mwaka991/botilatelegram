"""
Telegram Channel Bot - Main Entry Point

A production-ready Telegram bot that:
- Receives content from the bot owner via private chat
- Automatically posts content to a Telegram channel
- Supports text, photos, videos, and documents
- Promotes the channel with inline buttons
- Includes anti-spam protection and logging

Author: Chombezo Bot
Version: 1.0.0
"""

import asyncio
import signal
import sys
from pathlib import Path

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ChatMemberHandler,
    filters,
    ContextTypes,
)

# Import configuration
from config import Config, Messages

# Import handlers
from handlers import (
    start_command,
    help_command,
    channel_command,
    handle_text,
    handle_photo,
    handle_video,
    handle_document,
    handle_new_chat_member,
    handle_bot_added,
    handle_callback_query,
)

# Import utilities
from utils import get_logger, log_startup, log_shutdown, log_error

# Import middleware
from middleware import AntiSpamMiddleware


# ============================================
# Global Variables
# ============================================

application: Application = None


# ============================================
# Error Handler
# ============================================

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle errors that occur during updates.
    
    Args:
        update: Telegram update object (may be None)
        context: Bot context object with error information
    """
    user_id = update.effective_user.id if update and update.effective_user else None
    
    # Log the error
    log_error(
        f"Update '{update}' caused error: {context.error}",
        user_id,
        context.error
    )
    
    # Try to notify user if possible
    if update and update.effective_message:
        try:
            await update.effective_message.reply_text(
                Messages.ERROR,
                parse_mode='HTML'
            )
        except Exception:
            pass  # Ignore errors in error handler


# ============================================
# Shutdown Handler
# ============================================

def signal_handler(signum, frame):
    """Handle shutdown signals gracefully."""
    log_shutdown()
    sys.exit(0)


# ============================================
# Bot Setup
# ============================================

def setup_bot() -> Application:
    """
    Set up the Telegram bot application.
    
    Returns:
        Application: Configured bot application
    """
    # Validate configuration
    if not Config.validate():
        print("❌ Configuration validation failed. Please check your .env file.")
        sys.exit(1)
    
    # Create application
    app = Application.builder().token(Config.BOT_TOKEN).build()
    
    # Initialize anti-spam middleware in bot data
    app.bot_data['antispam'] = AntiSpamMiddleware()
    
    # ============================================
    # Register Command Handlers
    # ============================================
    
    # /start command - Welcome message
    app.add_handler(CommandHandler('start', start_command))
    
    # /help command - Help instructions
    app.add_handler(CommandHandler('help', help_command))
    
    # /channel command - Channel promotion
    app.add_handler(CommandHandler('channel', channel_command))
    
    # ============================================
    # Register Message Handlers (Owner Only)
    # ============================================
    
    # Text messages
    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND & filters.ChatType.PRIVATE,
            handle_text
        )
    )
    
    # Photos
    app.add_handler(
        MessageHandler(
            filters.PHOTO & filters.ChatType.PRIVATE,
            handle_photo
        )
    )
    
    # Videos
    app.add_handler(
        MessageHandler(
            filters.VIDEO & filters.ChatType.PRIVATE,
            handle_video
        )
    )
    
    # Documents
    app.add_handler(
        MessageHandler(
            filters.Document.ALL & filters.ChatType.PRIVATE,
            handle_document
        )
    )
    
    # ============================================
    # Register Group Handlers
    # ============================================
    
    # When bot is added to a group
    app.add_handler(
        MessageHandler(
            filters.StatusUpdate.NEW_CHAT_MEMBERS,
            handle_new_chat_member
        )
    )
    
    # Track chat member updates (bot added/removed)
    app.add_handler(
        ChatMemberHandler(handle_bot_added, ChatMemberHandler.MY_CHAT_MEMBER)
    )
    
    # ============================================
    # Register Callback Handler
    # ============================================
    
    app.add_handler(CallbackQueryHandler(handle_callback_query))
    
    # ============================================
    # Register Error Handler
    # ============================================
    
    app.add_error_handler(error_handler)
    
    return app


# ============================================
# Main Function
# ============================================

async def main() -> None:
    """
    Main entry point for the bot.
    Sets up and runs the bot application.
    """
    global application
    
    # Set up signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Setup bot
    application = setup_bot()
    
    # Get bot info for startup log
    async with application:
        bot = application.bot
        bot_info = await bot.get_me()
        log_startup(bot_info.username)
    
    # Start the bot
    print("\n🚀 Starting bot...")
    print("   Press Ctrl+C to stop\n")
    
    # Run the bot until Ctrl+C is pressed
    await application.initialize()
    await application.start()
    await application.updater.start_polling(
        drop_pending_updates=True,
        allowed_updates=Update.ALL_TYPES
    )
    
    # Keep running until interrupted
    while True:
        await asyncio.sleep(1)


# ============================================
# Entry Point
# ============================================

if __name__ == '__main__':
    try:
        # Check Python version
        if sys.version_info < (3, 9):
            print("❌ Python 3.9 or higher is required!")
            sys.exit(1)
        
        # Run the bot
        asyncio.run(main())
    except KeyboardInterrupt:
        log_shutdown()
        print("\n👋 Bot stopped. Goodbye!")
    except Exception as e:
        log_error("Fatal error during bot startup", exception=e)
        print(f"\n❌ Fatal error: {e}")
        sys.exit(1)
