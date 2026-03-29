"""
Logging Utility for Telegram Channel Bot

Provides structured logging for bot events, errors, and activities.
Uses Rich for beautiful console output and Python's built-in logging.
"""

import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

from rich.console import Console
from rich.logging import RichHandler
from rich.panel import Panel
from rich.text import Text

# ============================================
# Initialize Rich Console
# ============================================

console = Console()

# ============================================
# Configure Logging
# ============================================

# Create logs directory if it doesn't exist
LOGS_DIR = Path(__file__).parent.parent / 'logs'
LOGS_DIR.mkdir(exist_ok=True)

# Log file path with date
log_file = LOGS_DIR / f"bot_{datetime.now().strftime('%Y-%m-%d')}.log"

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        # Rich console handler for beautiful terminal output
        RichHandler(
            console=console,
            rich_tracebacks=True,
            show_time=True,
            show_path=False
        ),
        # File handler for persistent logging
        logging.FileHandler(log_file, encoding='utf-8')
    ]
)

# Get logger instance
logger = logging.getLogger('ChannelBot')


# ============================================
# Logger Functions
# ============================================

def get_logger() -> logging.Logger:
    """
    Get the logger instance.
    
    Returns:
        logging.Logger: The bot logger instance
    """
    return logger


def log_event(event_type: str, details: str, user_id: Optional[int] = None) -> None:
    """
    Log a bot event with structured information.
    
    Args:
        event_type: Type of event (e.g., 'message', 'post', 'error')
        details: Description of the event
        user_id: Optional Telegram user ID associated with the event
    """
    user_info = f" [User: {user_id}]" if user_id else ""
    message = f"[{event_type.upper()}]{user_info} {details}"
    logger.info(message)


def log_message_received(user_id: int, message_type: str, content_preview: str = "") -> None:
    """
    Log when a message is received from the owner.
    
    Args:
        user_id: Telegram user ID of the sender
        message_type: Type of message (text, photo, video, document)
        content_preview: Preview of the message content
    """
    preview = f" - {content_preview[:50]}..." if content_preview else ""
    log_event('message_received', f"{message_type}{preview}", user_id)
    
    # Also log to console with Rich formatting
    console.print(Panel(
        f"[green]New {message_type} received[/green]\n"
        f"[dim]From User:[/dim] {user_id}\n"
        f"[dim]Content:[/dim] {content_preview[:100]}{'...' if len(content_preview) > 100 else ''}",
        title="📨 Message Received",
        border_style="green"
    ))


def log_content_posted(user_id: int, message_type: str, channel: str) -> None:
    """
    Log when content is posted to the channel.
    
    Args:
        user_id: Telegram user ID who posted
        message_type: Type of content posted
        channel: Target channel identifier
    """
    log_event('content_posted', f"{message_type} posted to {channel}", user_id)
    
    console.print(Panel(
        f"[blue]{message_type.capitalize()} posted to channel[/blue]\n"
        f"[dim]Channel:[/dim] {channel}",
        title="📤 Content Posted",
        border_style="blue"
    ))


def log_channel_link_shared(user_id: int, chat_type: str, chat_title: str = "") -> None:
    """
    Log when the channel link is shared.
    
    Args:
        user_id: User ID or chat ID where link was shared
        chat_type: Type of chat (private, group, supergroup)
        chat_title: Title of the group (if applicable)
    """
    location = f"group '{chat_title}'" if chat_title else f"{chat_type} chat"
    log_event('link_shared', f"Channel link shared in {location}", user_id)
    
    console.print(Panel(
        f"[yellow]Channel link shared in {chat_type}[/yellow]\n"
        f"[dim]Location:[/dim] {location}",
        title="🔗 Link Shared",
        border_style="yellow"
    ))


def log_error(error_message: str, user_id: Optional[int] = None, exception: Optional[Exception] = None) -> None:
    """
    Log an error with optional exception details.
    
    Args:
        error_message: Description of the error
        user_id: Optional user ID associated with the error
        exception: Optional exception object
    """
    user_info = f" [User: {user_id}]" if user_id else ""
    full_message = f"{error_message}{user_info}"
    
    if exception:
        logger.exception(full_message)
    else:
        logger.error(full_message)
    
    # Pretty print error to console
    error_text = Text()
    error_text.append("❌ ERROR: ", style="bold red")
    error_text.append(error_message, style="red")
    if user_id:
        error_text.append(f"\nUser ID: {user_id}", style="dim")
    console.print(error_text)


def log_startup(bot_username: str) -> None:
    """
    Log bot startup information.
    
    Args:
        bot_username: Username of the bot
    """
    console.print(Panel(
        f"[bold green]Bot is starting up...[/bold green]\n\n"
        f"[dim]Username:[/dim] @{bot_username}\n"
        f"[dim]Started at:[/dim] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"[dim]Log file:[/dim] {log_file}",
        title="🤖 Bot Startup",
        border_style="green"
    ))
    logger.info(f"Bot @{bot_username} started successfully")


def log_shutdown() -> None:
    """Log bot shutdown."""
    console.print(Panel(
        "[bold yellow]Bot is shutting down...[/bold yellow]",
        title="🛑 Bot Shutdown",
        border_style="yellow"
    ))
    logger.info("Bot stopped")


# ============================================
# For testing
# ============================================

if __name__ == "__main__":
    # Test logging
    log_startup("TestBot")
    log_message_received(123456789, "text", "Hello, this is a test message!")
    log_content_posted(123456789, "photo", "@testchannel")
    log_channel_link_shared(123456789, "private")
    log_error("Test error message", 123456789)
    log_shutdown()
