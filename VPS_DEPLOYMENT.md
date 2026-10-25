# Ubuntu/Debian VPS Deployment

This guide runs the Telegram bot as a dedicated, unprivileged Linux user managed by systemd. The bot uses Telegram polling and needs no public web port.

## Before you start

- An Ubuntu 22.04/24.04 or Debian VPS with sudo access.
- A Telegram bot token from [@BotFather](https://t.me/BotFather).
- The bot added as an administrator to each target channel, with permission to post messages.
- The bot should run on only one server/instance at a time. A second polling instance can conflict and will also duplicate scheduled promotions.

## Install

Connect to the VPS over SSH, then install Git and Python:

```bash
sudo apt update
sudo apt install -y git python3 python3-venv python3-pip
python3 --version
```

Use Python 3.9 or newer. Create a dedicated service account and clone the repository:

```bash
sudo adduser --system --group --home /opt/telegram-channel-bot --no-create-home --shell /usr/sbin/nologin telegrambot
sudo mkdir -p /opt/telegram-channel-bot
sudo chown telegrambot:telegrambot /opt/telegram-channel-bot
sudo -u telegrambot git clone https://github.com/mwaka991/botilatelegram.git /opt/telegram-channel-bot
```

Create an isolated Python environment and install the pinned project dependencies:

```bash
sudo -u telegrambot python3 -m venv /opt/telegram-channel-bot/.venv
sudo -u telegrambot /opt/telegram-channel-bot/.venv/bin/python -m pip install --upgrade pip
sudo -u telegrambot /opt/telegram-channel-bot/.venv/bin/pip install -r /opt/telegram-channel-bot/requirements.txt
sudo -u telegrambot mkdir -p /opt/telegram-channel-bot/logs
```

## Configure secrets

Create a root-owned environment file outside the Git checkout:

```bash
sudo install -o root -g telegrambot -m 640 /dev/null /etc/telegram-channel-bot.env
sudo nano /etc/telegram-channel-bot.env
```

Add the following values, replacing examples with your actual settings:

```dotenv
BOT_TOKEN=your_new_bot_token
OWNER_USER_ID=your_telegram_user_id
CHANNELS=-1001234567890,-1009876543210
SHARE_LINK=https://t.me/yourchannel
ENVIRONMENT=production
LOG_LEVEL=INFO
MAX_MESSAGES_PER_MINUTE=5
REMOVE_CAPTIONS=true
REMOVE_LINKS=true
```

Save the file and confirm its permissions:

```bash
sudo chown root:telegrambot /etc/telegram-channel-bot.env
sudo chmod 640 /etc/telegram-channel-bot.env
```

Never place a real token in Git or paste it into public logs/issues. If a token has been exposed, revoke it with BotFather and use its replacement here.

## Install and start the systemd service

Install the service unit from the repository and enable it at boot:

```bash
sudo cp /opt/telegram-channel-bot/deploy/telegram-channel-bot.service /etc/systemd/system/telegram-channel-bot.service
sudo systemctl daemon-reload
sudo systemctl enable --now telegram-channel-bot
```

Check the service and follow its logs:

```bash
sudo systemctl status telegram-channel-bot
sudo journalctl -u telegram-channel-bot -f
```

The application also writes dated log files under `/opt/telegram-channel-bot/logs/`.

The scheduled promotional text is sent to all configured channels every four hours, with the first scheduled send four hours after startup. Restarting the service restarts that interval.

## Update the bot

Pull and install updates as the service account, then restart the service:

```bash
sudo systemctl stop telegram-channel-bot
sudo -u telegrambot git -C /opt/telegram-channel-bot pull --ff-only
sudo -u telegrambot /opt/telegram-channel-bot/.venv/bin/pip install -r /opt/telegram-channel-bot/requirements.txt
sudo systemctl start telegram-channel-bot
sudo systemctl status telegram-channel-bot
```

## Operations

```bash
sudo systemctl restart telegram-channel-bot
sudo systemctl stop telegram-channel-bot
sudo systemctl start telegram-channel-bot
sudo journalctl -u telegram-channel-bot --since today
```

If the bot does not start, inspect `systemctl status` and `journalctl` for missing environment values, dependency errors, or Telegram API errors. For channel posting failures, confirm the bot remains an administrator with posting permission.
