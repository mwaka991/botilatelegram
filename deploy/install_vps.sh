#!/usr/bin/env bash
set -euo pipefail

APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BOT_USER="${BOT_USER:-chombezo}"
SERVICE_NAME="chombezo-bot"

if [[ "$(id -u)" -ne 0 ]]; then
    echo "Run this script as root: sudo bash deploy/install_vps.sh"
    exit 1
fi

apt-get update
apt-get install -y python3 python3-venv python3-pip

if ! id "$BOT_USER" >/dev/null 2>&1; then
    useradd --system --home-dir "$APP_DIR" --shell /usr/sbin/nologin "$BOT_USER"
fi

python3 -m venv "$APP_DIR/.venv"
"$APP_DIR/.venv/bin/python" -m pip install --upgrade pip
"$APP_DIR/.venv/bin/pip" install --requirement "$APP_DIR/requirements.txt"

chown -R "$BOT_USER:$BOT_USER" "$APP_DIR"

sed \
    -e "s|__BOT_USER__|$BOT_USER|g" \
    -e "s|__APP_DIR__|$APP_DIR|g" \
    "$APP_DIR/deploy/$SERVICE_NAME.service" \
    > "/etc/systemd/system/$SERVICE_NAME.service"

systemctl daemon-reload
systemctl enable --now "$SERVICE_NAME"

echo
echo "Installed and started $SERVICE_NAME."
echo "Status: sudo systemctl status $SERVICE_NAME"
echo "Logs:   sudo journalctl -u $SERVICE_NAME -f"