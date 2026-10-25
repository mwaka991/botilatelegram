# VPS Deployment

The VPS deployment runs the bot with Telegram long polling under `systemd`.
This keeps the bot alive and restarts it automatically after a crash or VPS
reboot.

## Requirements

- Ubuntu/Debian VPS with SSH access
- A user with `sudo` access
- The bot added as an administrator in all 9 target groups/channels
- Permission to post media in each target

## Install

Clone or upload this repository to the VPS, then run from its root directory:

```bash
sudo bash deploy/install_vps.sh
```

The installer creates the `chombezo` system user, installs dependencies in
`.venv`, installs the `chombezo-bot.service` unit, and starts the bot.

To use another service user:

```bash
sudo env BOT_USER=telegrambot bash deploy/install_vps.sh
```

## Verify and monitor

```bash
sudo systemctl status chombezo-bot
sudo journalctl -u chombezo-bot -f
```

The status command should be:

```bash
sudo systemctl status chombezo-bot
```

Test the bot by sending `/start`, then send a video from Telegram user
`5884640087`. It should be posted to all configured targets with the fixed
caption from `Config.MEDIA_CAPTION`.

## Updates

```bash
git pull
sudo bash deploy/install_vps.sh
```

The installer refreshes dependencies and restarts the service.

## Configuration and security

The requested configuration is hardcoded in `config.py`, and no `.env` file
is needed. The Telegram token has been exposed in chat and should be rotated
with BotFather before production; update `Config.BOT_TOKEN` after rotating it.