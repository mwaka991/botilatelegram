# 🤖 Telegram Channel Bot

A production-ready Telegram bot that automatically posts content from the owner to a channel, with channel promotion features and anti-spam protection.

## ✨ Features

- 📨 **Auto-Posting**: Send content to the bot inbox and it automatically posts to your channel
- 📸 **Media Support**: Handles text, photos, videos, and documents
- 🔒 **Owner-Only Access**: Only the bot owner can post content
- 🛡️ **Anti-Spam**: Rate limiting prevents abuse from random users
- 📢 **Channel Promotion**: Automatically shares channel link with users and groups
- 🔘 **Inline Buttons**: "Join Channel" buttons for easy access
- 📝 **Comprehensive Logging**: All events and errors are logged
- ⚙️ **Configurable**: Environment-based configuration with `.env` file- 🌐 **Cloud Ready**: Easily deploy to Render.com, Heroku, or other cloud platforms
- 🔗 **Link Removal**: Automatically strips all links from content before posting
## 📋 Requirements

- Python 3.9 or higher
- A Telegram Bot Token (from [@BotFather](https://t.me/BotFather))
- A Telegram Channel where the bot is an admin
- Your Telegram User ID

## 🚀 Installation

### Step 1: Clone or Download the Project

```bash
# Create project directory
mkdir telegram-channel-bot
cd telegram-channel-bot

# Copy all the bot files here
```

### Step 2: Create Virtual Environment (Recommended)

**Windows:**
```cmd
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure the Bot

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Edit `.env` with your configuration:

```env
# Required Settings
BOT_TOKEN=your_bot_token_here
OWNER_USER_ID=your_user_id_here
CHANNELS=-1001234567890,-1009876543210
SHARE_LINK=https://t.me/yourchannel
```

## 🔧 Configuration Guide

### Getting Required IDs

#### 1. BOT_TOKEN
Get your bot token from [@BotFather](https://t.me/BotFather):
1. Start a chat with @BotFather
2. Send `/newbot`
3. Follow instructions to create your bot
4. Copy the token (looks like: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

#### 2. OWNER_USER_ID
Get your Telegram User ID:
1. Message [@userinfobot](https://t.me/userinfobot)
2. It will reply with your ID (e.g., `123456789`)
3. Copy the number

#### 3. CHANNELS
Get your channel IDs or usernames:

**Method 1 - Using a Bot:**
1. Add [@getidsbot](https://t.me/getidsbot) to your channel as administrator
2. Send any message in the channel
3. The bot will reply with the channel ID (e.g., `-1001234567890`)
4. Copy the full ID including the `-100` prefix

**Method 2 - Using Web:**
1. Open your channel in Telegram Web
2. Look at the URL: `https://web.telegram.org/a/#-1001234567890`
3. The number after `#` is your channel ID

You can configure one or more target channels by separating values with commas:
```env
CHANNELS=-1001234567890,-1009876543210
```

#### 4. CHANNEL_USERNAME (Optional)
Instead of channel IDs, you can optionally use a channel username:
```env
CHANNEL_USERNAME=@yourchannel
```

#### 5. SHARE_LINK
This is the public link to your channel:
```env
SHARE_LINK=https://t.me/yourchannel
```

### Optional Settings

```env
# Remove captions from media before posting (true/false)
REMOVE_CAPTIONS=false

# Rate limiting: max messages per minute for non-owners
MAX_MESSAGES_PER_MINUTE=5

# Logging level: DEBUG, INFO, WARNING, ERROR
LOG_LEVEL=INFO
```

## 🎮 Usage

### Running the Bot

```bash
python bot.py
```

You'll see output like:
```
🤖 Bot Startup
Bot is starting up...
   Username: @YourBot
   Started at: 2024-01-15 10:30:00
   Log file: logs/bot_2024-01-15.log

🚀 Starting bot...
   Press Ctrl+C to stop
```

### Posting Content

1. **Start the bot** in private chat: Send `/start`
2. **Send any content** to the bot:
   - Text messages
   - Photos
   - Videos
   - Documents
3. The bot automatically posts it to your channel!

### Available Commands

| Command | Description |
|---------|-------------|
| `/start` | Show welcome message with channel link |
| `/help` | Display help instructions |
| `/channel` | Get the channel link |

### Bot in Groups

When you add the bot to a group:
- It automatically sends a welcome message with your channel link
- Regular users cannot use it for posting (owner-only)
- Non-owners are rate-limited

## 📁 Project Structure

```
telegram-channel-bot/
├── bot.py                  # Main entry point
├── config.py               # Configuration management
├── requirements.txt        # Python dependencies
├── .env.example           # Example environment file
├── README.md              # This file
├── utils/                 # Utility modules
│   ├── __init__.py
│   ├── logger.py          # Logging utilities
│   └── keyboards.py       # Inline keyboard builders
├── handlers/              # Telegram handlers
│   ├── __init__.py
│   ├── commands.py        # Command handlers
│   ├── messages.py        # Message handlers
│   ├── groups.py          # Group event handlers
│   └── callbacks.py       # Callback handlers
├── middleware/            # Security middleware
│   ├── __init__.py
│   └── antispam.py        # Rate limiting & protection
└── logs/                  # Log files (created automatically)
    └── bot_2024-01-15.log
```

## 🔒 Security Features

### Owner-Only Access
- Only the configured `OWNER_USER_ID` can post content
- Other users receive an "Access Denied" message

### Anti-Spam Protection
- Rate limiting for non-owner users (default: 5 messages per minute)
- Automatic temporary blocking for abusers (5 minutes)
- Owner is exempt from rate limits

### Secure Configuration
- Bot token stored in environment variables
- `.env` file excluded from version control
- No sensitive data in code

## 📝 Logging

The bot logs all important events:

- **Startup/Shutdown**: When the bot starts or stops
- **Messages Received**: Content sent by owner
- **Content Posted**: Successful posts to channel
- **Link Shares**: When channel link is shared
- **Errors**: Any errors that occur

Logs are stored in:
- Console (with beautiful formatting)
- `logs/bot_YYYY-MM-DD.log` files

## 🐛 Troubleshooting

### Bot Not Responding
1. Check if the bot token is correct
2. Ensure `.env` file exists and is properly configured
3. Check logs for errors

### Cannot Post to Channel
1. Make sure the bot is an admin in your channel
2. Verify the channel ID is correct (must include `-100` prefix)
3. Check that your user ID matches `OWNER_USER_ID`

### Permission Errors
1. In your channel settings, add the bot as administrator
2. Required permissions: Post Messages, Edit Messages, Delete Messages

### Rate Limiting Issues
If you're the owner and getting rate limited:
1. Check that `OWNER_USER_ID` matches your actual Telegram ID
2. Restart the bot after changing configuration

## 🔄 Updating the Bot

To update the bot:
1. Stop the bot (Ctrl+C)
2. Pull/download new files
3. Reinstall dependencies if `requirements.txt` changed
4. Start the bot again

## 🌐 Cloud Deployment

### Render.com (Recommended)

Deploy to [Render.com](https://render.com) for free 24/7 hosting:

1. Push your code to GitHub
2. Create a new Background Worker on Render
3. Set environment variables:
   - `BOT_TOKEN` - Your Telegram bot token
   - `SHARE_LINK` - Your channel URL
4. Render will automatically build and run your bot

**For detailed instructions, see [DEPLOYMENT.md](./DEPLOYMENT.md)**

### Features on Render
✅ Free tier available  
✅ Auto-restart on crashes  
✅ Built-in logging dashboard  
✅ Easy environment variable management  
✅ No credit card required to start  

### Other Deployment Options
- Heroku (paid after free tier)
- AWS Lambda (serverless)
- DigitalOcean (low-cost VPS)
- Your own server/VPS

## 📄 License

This project is open source. Feel free to modify and distribute.

## 🤝 Support

For issues or questions:
1. Check the troubleshooting section
2. Review the logs in `logs/` directory
3. Ensure all configuration is correct

## 🎯 Next Steps

1. ✅ Set up your `.env` file with your bot token and IDs
2. ✅ Add your bot to your channel as an admin
3. ✅ Run `python bot.py`
4. ✅ Send a test message to your bot!

---

**Made with ❤️ for Telegram Channel Management**
