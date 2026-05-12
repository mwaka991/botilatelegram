"""
Configuration Module for Telegram Channel Bot

This module handles all configuration settings for the bot,
loading values from environment variables with sensible defaults.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# ============================================
# Load Environment Variables
# ============================================

# Get the directory where this script is located
BASE_DIR = Path(__file__).parent.absolute()

# Load .env file if it exists
env_path = BASE_DIR / '.env'
if env_path.exists():
    load_dotenv(env_path)


# ============================================
# Bot Configuration Class
# ============================================

class Config:
    """
    Configuration class for the Telegram Bot.
    All settings are loaded from environment variables.
    """
    
    # --- Required Settings ---
    BOT_TOKEN: str = os.getenv('BOT_TOKEN', '')
    OWNER_USER_ID: int = 5884640087
    CHANNELS: list = [
        -1003616229345,
        -1003613654933,
        -1003818751718,
        -1003938219620,  # kutombana77 group
        -1003834068464,
        -1003730658824,
    ]
    SHARE_LINK: str = os.getenv('SHARE_LINK', 'https://t.me/chombezo')
    
    # --- Optional Settings ---
    ENVIRONMENT: str = os.getenv('ENVIRONMENT', 'production')
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')
    
    # --- Anti-Spam Settings ---
    MAX_MESSAGES_PER_MINUTE: int = int(os.getenv('MAX_MESSAGES_PER_MINUTE', '5'))
    REMOVE_CAPTIONS: bool = os.getenv('REMOVE_CAPTIONS', 'false').lower() == 'true'
    REMOVE_LINKS: bool = os.getenv('REMOVE_LINKS', 'true').lower() == 'true'
    
    # ============================================
    # Validation Methods
    # ============================================
    
    @classmethod
    def validate(cls) -> bool:
        """
        Validate that all required configuration is present.
        
        Returns:
            bool: True if configuration is valid, False otherwise
        """
        required_fields = [
            ('BOT_TOKEN', cls.BOT_TOKEN),
            ('OWNER_USER_ID', cls.OWNER_USER_ID),
        ]
        
        # Check that channels are configured
        if not cls.CHANNELS:
            print("❌ ERROR: CHANNELS list must not be empty!")
            return False
        
        missing = []
        for name, value in required_fields:
            if not value or value == '0':
                missing.append(name)
        
        if missing:
            print(f"❌ ERROR: Missing required configuration: {', '.join(missing)}")
            return False
        
        return True
    
    @classmethod
    def get_target_channels(cls) -> list:
        """
        Get all target channel identifiers.
        
        Returns:
            list: List of channel IDs to post to
        """
        return cls.CHANNELS
    
    @classmethod
    def is_owner(cls, user_id: int) -> bool:
        """
        Check if a user is the bot owner.
        
        Args:
            user_id: Telegram user ID to check
            
        Returns:
            bool: True if user is the owner, False otherwise
        """
        return user_id == cls.OWNER_USER_ID
    
    @classmethod
    def is_development(cls) -> bool:
        """
        Check if running in development mode.
        
        Returns:
            bool: True if in development mode
        """
        return cls.ENVIRONMENT.lower() == 'development'


# ============================================
# Bot Messages
# ============================================

class Messages:
    """
    Static messages used by the bot.
    Edit these to customize the bot's responses.
    """
    
    # Welcome message sent when user starts the bot
    WELCOME = """
👋 <b>Welcome to the Channel Bot!</b>

I'm here to help you stay connected with our amazing channel.

📢 <b>Join our channel:</b> {channel_link}

<b>Available Commands:</b>
• /start - Show this welcome message
• /help - Get help and instructions
• /channel - Get the channel link

Feel free to explore and join our community! 🎉
"""
    
    # Help message
    HELP = """
❓ <b>Help & Instructions</b>

<b>For Channel Members:</b>
• Use /channel to get the channel link
• Click "Join Channel" button to join

<b>For Bot Owner:</b>
• Send any message, photo, video, or document to post it to the channel
• The bot will automatically forward your content

<b>Need Support?</b>
Contact the bot administrator for assistance.
"""
    
    # Channel promotion message
    CHANNEL_PROMO = """
📢 <b>Join Our Official Channel!</b>

Stay updated with the latest content, news, and announcements.

👉 {channel_link}

<i>Click the button below to join now!</i>
"""
    
    # Message sent when bot is added to a group
    GROUP_WELCOME = """
👋 <b>Hello everyone!</b>

Thanks for adding me to this group!

I'm here to share an amazing channel with you all:
📢 {channel_link}

Feel free to join and stay updated!
"""
    
    # Unauthorized access message
    UNAUTHORIZED = "Join channel: https://t.me/chombezo"
    
    # Rate limit message
    RATE_LIMITED = """
⚠️ <b>Slow Down!</b>

You're sending messages too quickly. Please wait a moment before trying again.
"""
    
    # Success message after posting
    POST_SUCCESS = "✅ Content posted to all channels successfully!"
    
    # Error message
    ERROR = "❌ An error occurred. Please try again later or contact support."


# ============================================
# Initialize Configuration
# ============================================

if __name__ == "__main__":
    # Test configuration loading
    print("🔧 Testing Configuration...")
    
    if Config.validate():
        print("✅ Configuration is valid!")
        print(f"   Target Channels: {Config.CHANNELS}")
        print(f"   Owner ID: {Config.OWNER_USER_ID}")
        print(f"   Environment: {Config.ENVIRONMENT}")
    else:
        print("❌ Configuration validation failed!")
        exit(1)
