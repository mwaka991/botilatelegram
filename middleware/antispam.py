"""
Anti-Spam Middleware for Telegram Channel Bot

Provides rate limiting and spam protection to prevent abuse.
Tracks message frequency per user and blocks users who exceed limits.
"""

import time
from collections import defaultdict
from typing import Dict, List
from functools import wraps

from telegram import Update
from telegram.ext import ContextTypes

from config import Config, Messages
from utils.logger import log_error


# ============================================
# Anti-Spam Manager
# ============================================

class AntiSpamMiddleware:
    """
    Middleware to handle rate limiting and spam protection.
    Tracks user message frequency and blocks abusers.
    """
    
    def __init__(self, max_messages: int = None, time_window: int = 60):
        """
        Initialize the anti-spam middleware.
        
        Args:
            max_messages: Maximum messages allowed per time window (default from config)
            time_window: Time window in seconds (default 60 seconds)
        """
        self.max_messages = max_messages or Config.MAX_MESSAGES_PER_MINUTE
        self.time_window = time_window
        
        # Store message timestamps per user: {user_id: [timestamp1, timestamp2, ...]}
        self.user_messages: Dict[int, List[float]] = defaultdict(list)
        
        # Blocked users: {user_id: unblock_timestamp}
        self.blocked_users: Dict[int, float] = {}
        
        # Block duration in seconds (5 minutes)
        self.block_duration = 300
    
    def is_allowed(self, user_id: int) -> bool:
        """
        Check if a user is allowed to send messages.
        Owner is always allowed.
        
        Args:
            user_id: Telegram user ID
            
        Returns:
            bool: True if user can send messages, False otherwise
        """
        # Owner is always allowed
        if Config.is_owner(user_id):
            return True
        
        current_time = time.time()
        
        # Check if user is blocked
        if user_id in self.blocked_users:
            if current_time < self.blocked_users[user_id]:
                return False
            else:
                # Unblock user
                del self.blocked_users[user_id]
        
        # Clean old messages outside the time window
        self.user_messages[user_id] = [
            timestamp for timestamp in self.user_messages[user_id]
            if current_time - timestamp < self.time_window
        ]
        
        # Check if user has exceeded rate limit
        if len(self.user_messages[user_id]) >= self.max_messages:
            # Block user temporarily
            self.blocked_users[user_id] = current_time + self.block_duration
            log_error(
                f"User rate limited - blocked for {self.block_duration} seconds",
                user_id
            )
            return False
        
        # Record this message
        self.user_messages[user_id].append(current_time)
        return True
    
    def get_remaining_time(self, user_id: int) -> int:
        """
        Get remaining block time for a user.
        
        Args:
            user_id: Telegram user ID
            
        Returns:
            int: Remaining block time in seconds, 0 if not blocked
        """
        if user_id not in self.blocked_users:
            return 0
        
        remaining = int(self.blocked_users[user_id] - time.time())
        return max(0, remaining)


# ============================================
# Decorator for Handler Protection
# ============================================

def spam_protected(handler_func):
    """
    Decorator to add spam protection to handlers.
    Automatically checks rate limits before processing.
    
    Usage:
        @spam_protected
        async def my_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
            # Your handler code
    """
    @wraps(handler_func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        # Get or create anti-spam instance in bot data
        if 'antispam' not in context.bot_data:
            context.bot_data['antispam'] = AntiSpamMiddleware()
        
        antispam = context.bot_data['antispam']
        
        # Get user ID
        user_id = update.effective_user.id if update.effective_user else None
        
        if not user_id:
            return await handler_func(update, context, *args, **kwargs)
        
        # Check if user is allowed
        if not antispam.is_allowed(user_id):
            remaining = antispam.get_remaining_time(user_id)
            
            # Send rate limit message
            if update.message:
                await update.message.reply_text(
                    Messages.RATE_LIMITED + f"\n\n⏳ Try again in {remaining} seconds.",
                    parse_mode='HTML'
                )
            elif update.callback_query:
                await update.callback_query.answer(
                    f"Rate limited. Try again in {remaining} seconds.",
                    show_alert=True
                )
            
            return  # Stop processing
        
        # User is allowed, proceed with handler
        return await handler_func(update, context, *args, **kwargs)
    
    return wrapper


# ============================================
# Owner-only Decorator
# ============================================

def owner_only(handler_func):
    """
    Decorator to restrict handlers to bot owner only.
    
    Usage:
        @owner_only
        async def admin_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
            # Only owner can access this
    """
    @wraps(handler_func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        user_id = update.effective_user.id if update.effective_user else None
        
        if not user_id or not Config.is_owner(user_id):
            # Send unauthorized message
            if update.message:
                await update.message.reply_text(
                    Messages.UNAUTHORIZED,
                    parse_mode='HTML'
                )
            elif update.callback_query:
                await update.callback_query.answer(
                    "You are not authorized!",
                    show_alert=True
                )
            
            log_error("Unauthorized access attempt", user_id)
            return  # Stop processing
        
        # User is owner, proceed
        return await handler_func(update, context, *args, **kwargs)
    
    return wrapper


# ============================================
# Combined Protection
# ============================================

def protected_handler(handler_func):
    """
    Combined decorator that applies both spam protection and owner verification.
    Use this for handlers that should only be accessible by the owner
    and need rate limiting.
    
    Usage:
        @protected_handler
        async def admin_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
            # Only owner, with rate limiting
    """
    return owner_only(spam_protected(handler_func))


# ============================================
# For testing
# ============================================

if __name__ == "__main__":
    # Test anti-spam functionality
    antispam = AntiSpamMiddleware(max_messages=3, time_window=60)
    
    # Simulate messages from a user
    test_user = 123456789
    
    print(f"Testing rate limiting for user {test_user}:")
    for i in range(5):
        allowed = antispam.is_allowed(test_user)
        print(f"  Message {i+1}: {'✅ Allowed' if allowed else '❌ Blocked'}")
    
    # Test owner bypass
    owner_user = Config.OWNER_USER_ID if Config.OWNER_USER_ID else 999999
    print(f"\nTesting owner bypass for user {owner_user}:")
    for i in range(5):
        allowed = antispam.is_allowed(owner_user)
        print(f"  Message {i+1}: {'✅ Allowed' if allowed else '❌ Blocked'}")
