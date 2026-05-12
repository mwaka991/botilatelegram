# 📋 Environment Variables Reference

This guide explains all environment variables used by the Telegram Channel Bot for Render deployment.

## Required Variables

These MUST be set in Render for the bot to work:

### BOT_TOKEN
- **Description**: Telegram Bot API token from @BotFather
- **Format**: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`
- **Required**: YES
- **Scope**: Keep secret! 🔐
- **Where to get**: https://t.me/botfather

**Example**:
```
BOT_TOKEN=5123456789:ABCdefGHIjklMNOpqrsTUVwxyz_ExampleToken
```

### SHARE_LINK
- **Description**: URL to your Telegram channel for promotion
- **Format**: `https://t.me/yourchannel`
- **Required**: YES
- **Default**: `https://t.me/chombezo`
- **Scope**: Public

**Example**:
```
SHARE_LINK=https://t.me/mychannel
```

---

## Optional Variables

These have sensible defaults but can be customized:

### ENVIRONMENT
- **Description**: Deployment environment mode
- **Options**: `production` or `development`
- **Default**: `production`
- **Impact**: Affects logging verbosity and error handling

**Example**:
```
ENVIRONMENT=production
```

### LOG_LEVEL
- **Description**: Minimum logging level
- **Options**: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`
- **Default**: `INFO`
- **Impact**: Controls what messages are logged

**Recommended for different scenarios**:
- `DEBUG` - Development and troubleshooting
- `INFO` - Normal production use (recommended)
- `WARNING` - Only warnings and errors
- `ERROR` - Only errors

**Example**:
```
LOG_LEVEL=INFO
```

### REMOVE_LINKS
- **Description**: Automatically remove all links from content before posting
- **Options**: `true` or `false`
- **Default**: `true`
- **Impact**: Links in text/captions are stripped

**What gets removed**:
- HTTP/HTTPS URLs (`https://example.com`)
- WWW links (`www.example.com`)
- Telegram links (`t.me/channel`)
- Markdown links (`[text](url)`)

**Example**:
```
REMOVE_LINKS=true
```

### REMOVE_CAPTIONS
- **Description**: Remove all captions from media before posting
- **Options**: `true` or `false`
- **Default**: `false`
- **Impact**: Photos, videos, documents are posted without captions

**Example**:
```
REMOVE_CAPTIONS=false
```

### MAX_MESSAGES_PER_MINUTE
- **Description**: Rate limit for non-owner users
- **Format**: Numeric value (messages per minute)
- **Default**: `5`
- **Impact**: Users exceeding this limit are blocked for 5 minutes
- **Note**: Bot owner is always exempt from rate limiting

**Example**:
```
MAX_MESSAGES_PER_MINUTE=5
```

---

## How to Set Variables in Render

1. Go to your service's dashboard
2. Click **Environment** tab
3. Click **Add Environment Variable**
4. Enter:
   - **Key**: Variable name (e.g., `BOT_TOKEN`)
   - **Value**: Variable value (e.g., your token)
5. Click **Save Changes**
6. Render automatically restarts the service with new variables

## In render.yaml

Variables are defined in `render.yaml`:

```yaml
envVars:
  - key: BOT_TOKEN
    scope: run
    sync: false
  - key: SHARE_LINK
    scope: run
    sync: false
  - key: REMOVE_LINKS
    value: "true"
  - key: REMOVE_CAPTIONS
    value: "false"
  - key: MAX_MESSAGES_PER_MINUTE
    value: "5"
  - key: ENVIRONMENT
    value: "production"
  - key: LOG_LEVEL
    value: "INFO"
```

## For Local Development

Create a `.env` file in project root:

```env
BOT_TOKEN=your_bot_token_here
SHARE_LINK=https://t.me/yourchannel
ENVIRONMENT=production
LOG_LEVEL=INFO
REMOVE_LINKS=true
REMOVE_CAPTIONS=false
MAX_MESSAGES_PER_MINUTE=5
```

**Important**: Never commit `.env` to git! It's in `.gitignore` for security.

## Configuration Validation

The bot validates required settings on startup:

```
❌ Configuration validation failed. Please check your .env file.
```

This error means:
- `BOT_TOKEN` is missing or empty
- `OWNER_USER_ID` is not configured (hardcoded in config.py)
- `CHANNELS` list is empty

## Troubleshooting Variables

### "Bot not responding"
- Check `BOT_TOKEN` is correct
- Copy from @BotFather exactly (no spaces)

### "Posts not going to channels"
- Check `SHARE_LINK` is valid
- Verify bot is admin in all channels

### "Links still appearing in posts"
- Check `REMOVE_LINKS=true`
- Restart the service after changing

### "Rate limiting not working"
- Check `MAX_MESSAGES_PER_MINUTE` value
- Owner is always exempt (check `OWNER_USER_ID` in code)

---

## Summary Table

| Variable | Required | Default | Scope | Example |
|----------|----------|---------|-------|---------|
| BOT_TOKEN | YES | - | Secret | `123456:ABC...` |
| SHARE_LINK | YES | - | Public | `https://t.me/mychannel` |
| ENVIRONMENT | NO | production | Public | `production` |
| LOG_LEVEL | NO | INFO | Public | `INFO` |
| REMOVE_LINKS | NO | true | Public | `true` |
| REMOVE_CAPTIONS | NO | false | Public | `false` |
| MAX_MESSAGES_PER_MINUTE | NO | 5 | Public | `5` |

---

For more information, see:
- [DEPLOYMENT.md](./DEPLOYMENT.md) - Full deployment guide
- [RENDER_CHECKLIST.md](./RENDER_CHECKLIST.md) - Pre-deployment checklist
- [.env.example](./.env.example) - Example configuration
