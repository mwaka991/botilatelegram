"""
Keyboard Utilities for Telegram Channel Bot

Provides inline keyboard builders for the bot's interactive elements.
"""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from config import Config, Messages


# ============================================
# Inline Keyboard Builders
# ============================================

def get_join_channel_keyboard() -> InlineKeyboardMarkup:
    """
    Create an inline keyboard with a "Join Channel" button.
    
    Returns:
        InlineKeyboardMarkup: Keyboard with join channel button
    """
    keyboard = [
        [
            InlineKeyboardButton(
                text="📢 Join Channel",
                url=Config.SHARE_LINK
            )
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_channel_link_keyboard() -> InlineKeyboardMarkup:
    """
    Create an inline keyboard with channel link button.
    Alternative version with different button text.
    
    Returns:
        InlineKeyboardMarkup: Keyboard with channel link button
    """
    keyboard = [
        [
            InlineKeyboardButton(
                text="🔗 Open Channel",
                url=Config.SHARE_LINK
            )
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_promotion_keyboard() -> InlineKeyboardMarkup:
    """
    Create a promotion keyboard with multiple options.
    
    Returns:
        InlineKeyboardMarkup: Keyboard with promotion buttons
    """
    keyboard = [
        [
            InlineKeyboardButton(
                text="📢 Join Our Channel",
                url=Config.SHARE_LINK
            )
        ],
        [
            InlineKeyboardButton(
                text="ℹ️ About",
                callback_data="about"
            )
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


# ============================================
# Helper Functions
# ============================================

def format_welcome_message() -> str:
    """
    Format the welcome message with channel link.
    
    Returns:
        str: Formatted welcome message
    """
    return Messages.WELCOME.format(channel_link=Config.SHARE_LINK)


def format_channel_promo() -> str:
    """
    Format the channel promotion message.
    
    Returns:
        str: Formatted promotion message
    """
    return Messages.CHANNEL_PROMO.format(channel_link=Config.SHARE_LINK)


def format_group_welcome() -> str:
    """
    Format the group welcome message.
    
    Returns:
        str: Formatted group welcome message
    """
    return Messages.GROUP_WELCOME.format(channel_link=Config.SHARE_LINK)


# ============================================
# For testing
# ============================================

if __name__ == "__main__":
    # Test keyboard creation (requires Config to be set)
    try:
        keyboard = get_join_channel_keyboard()
        print("✅ Keyboard created successfully")
        print(f"   Buttons: {keyboard.inline_keyboard}")
    except Exception as e:
        print(f"❌ Error: {e}")
