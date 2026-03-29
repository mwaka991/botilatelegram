"""
Middleware Package for Telegram Channel Bot

Contains middleware for anti-spam protection, rate limiting,
and other security features.
"""

from .antispam import AntiSpamMiddleware

__all__ = ['AntiSpamMiddleware']
