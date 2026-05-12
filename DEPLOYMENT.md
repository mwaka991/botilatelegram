# Render.com Deployment Guide

This guide explains how to deploy the Telegram Channel Bot to Render.com as a background worker.

## Prerequisites

- Telegram Bot Token from [@BotFather](https://t.me/BotFather)
- GitHub account (to push your code)
- Render.com account (create at [render.com](https://render.com))
- Your bot's channel links and configuration

## Deployment Steps

### Step 1: Prepare Your Repository

1. Initialize git in your project directory (if not already done):
```bash
git init
git add .
git commit -m "Initial commit: Telegram bot ready for Render"
```

2. Push your code to GitHub:
```bash
git remote add origin https://github.com/yourusername/telegram-channel-bot.git
git branch -M main
git push -u origin main
```

### Step 2: Create a New Service on Render

1. Go to [render.com](https://render.com) and sign in
2. Click **New +** → **Background Worker**
3. Connect your GitHub repository
4. Fill in the service details:
   - **Name**: `telegram-channel-bot`
   - **Runtime**: Python 3.13
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python bot.py`
   - **Instance Type**: Free (or paid if you want guaranteed uptime)

### Step 3: Set Environment Variables

In the Render dashboard, add these environment variables:

**Required:**
- `BOT_TOKEN` - Your Telegram bot token from @BotFather
- `SHARE_LINK` - Your channel URL (e.g., `https://t.me/yourchannel`)

**Optional (defaults provided):**
- `REMOVE_LINKS` - Set to `true` to remove all links from content (default: `true`)
- `REMOVE_CAPTIONS` - Set to `true` to remove captions from media (default: `false`)
- `MAX_MESSAGES_PER_MINUTE` - Rate limit for non-owner users (default: `5`)
- `ENVIRONMENT` - Set to `production` (default: `production`)
- `LOG_LEVEL` - Set to `INFO` for normal operations (default: `INFO`)

**Important**: DO NOT commit sensitive variables to git. Always set them in Render's environment variables dashboard.

### Step 4: Deploy

1. Click **Create Service**
2. Render will automatically:
   - Clone your repository
   - Install dependencies from `requirements.txt`
   - Start the bot with `python bot.py`
   - Keep it running continuously

3. Monitor the bot's status:
   - Go to your service dashboard
   - Check **Logs** tab to see real-time output
   - The bot will log all events, errors, and postings

### Step 5: Verify Deployment

1. Send a test message to your bot:
   - Open Telegram and find your bot
   - Send `/start` command
   - You should see the welcome message

2. Check the logs:
   - Go to the **Logs** tab in your Render dashboard
   - Look for startup messages and activity logs

## Important Notes

### How It Works on Render

- **Background Worker**: Runs continuously in the background without exposing an HTTP endpoint
- **Polling**: The bot uses polling (not webhooks) to listen for updates
- **Auto-restart**: If the bot crashes, Render automatically restarts it
- **Logging**: All logs are written to stdout and appear in Render's **Logs** tab
- **No File Storage**: Log files are not persisted (they only appear in the **Logs** dashboard)

### Bot Features on Render

✅ **Working Features:**
- Auto-posting to multiple channels
- Media support (text, photos, videos, documents)
- Link removal from content
- Anti-spam protection
- Command handling (/start, /help, /channel)
- Channel promotion
- Comprehensive logging

✅ **What's Different:**
- Logs appear in Render's dashboard instead of local files
- No need for .env file (use environment variables instead)
- Automatic restart on crashes
- Always-on background worker (with free tier limitations)

### Render Free Tier Limitations

- Services spin down after 15 minutes of inactivity
- One concurrent instance maximum
- Monthly credits apply to all services

For production use, consider upgrading to a paid plan for:
- Guaranteed uptime
- Always-on service without spin-down
- Better performance

## Updating the Bot

To deploy updates:

1. Make changes to your code locally
2. Test locally (optional):
   ```bash
   pip install -r requirements.txt
   python bot.py
   ```
3. Commit and push to GitHub:
   ```bash
   git add .
   git commit -m "Description of changes"
   git push origin main
   ```
4. Render automatically deploys the latest code

### Rollback

If something breaks:
1. Go to your service's **Deploys** tab
2. Click on a previous successful deployment
3. Click **Redeploy** to roll back

## Troubleshooting

### Bot Not Starting

- Check the **Logs** tab for error messages
- Ensure all required environment variables are set
- Verify `BOT_TOKEN` is correct

### Messages Not Posting

- Check channel IDs in `config.py` are correct
- Ensure the bot is an admin in all target channels
- Check the **Logs** tab for posting errors

### Bot Keeps Crashing

- Check **Logs** tab for exception messages
- Ensure all channel IDs are valid
- Verify the bot has proper permissions in channels

### High Memory Usage

- This typically indicates an infinite loop or memory leak
- Check recent code changes
- Review **Logs** for patterns

## Support

- Check [Render Documentation](https://render.com/docs)
- Review [python-telegram-bot Documentation](https://python-telegram-bot.readthedocs.io/)
- Check bot logs in Render's **Logs** tab for error messages

## Additional Resources

- [Telegram Bot API](https://core.telegram.org/bots/api)
- [Render Background Workers](https://render.com/docs/background-workers)
- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)

---

**Deployment Ready!** Your bot is now configured for Render.com deployment. Follow the steps above to get it running! 🚀
