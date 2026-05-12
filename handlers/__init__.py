"""
Handlers Package for Telegram Channel Bot

Contains all Telegram bot handlers including:
- Command handlers (/start, /help, /channel)
- Message handlers (text, photo, video, document)
- Callback handlers (inline button callbacks)
- Group handlers (bot added to groups)
"""

from .commands import start_command, help_command, channel_command
from .messages import handle_text, handle_photo, handle_video, handle_document
from .groups import handle_new_chat_member, handle_bot_added, handle_bot_removed
from .callbacks import handle_callback_query

__all__ = [
    # Commands
    'start_command',
    'help_command', 
    'channel_command',
    # Messages
    'handle_text',
    'handle_photo',
    'handle_video',
    'handle_document',
    # Groups
    'handle_new_chat_member',
    'handle_bot_added',
    'handle_bot_removed',
    # Callbacks
    'handle_callback_query',
]
