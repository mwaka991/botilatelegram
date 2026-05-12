"""
Utilities Package for Telegram Channel Bot

This package contains utility modules for logging, keyboard builders,
and other helper functions used throughout the bot.
"""

from .logger import (
    get_logger, 
    log_event, 
    log_message_received,
    log_content_posted,
    log_channel_link_shared,
    log_error,
    log_startup,
    log_shutdown
)
from .keyboards import (
    get_join_channel_keyboard,
    get_channel_link_keyboard,
    get_promotion_keyboard,
    format_welcome_message,
    format_channel_promo,
    format_group_welcome
)
from .text_utils import (
    remove_links,
    has_links
)

__all__ = [
    'get_logger', 
    'log_event', 
    'log_message_received',
    'log_content_posted',
    'log_channel_link_shared',
    'log_error',
    'log_startup',
    'log_shutdown',
    'get_join_channel_keyboard',
    'get_channel_link_keyboard',
    'get_promotion_keyboard',
    'format_welcome_message',
    'format_channel_promo',
    'format_group_welcome',
    'remove_links',
    'has_links'
]
