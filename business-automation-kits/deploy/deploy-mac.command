#!/bin/bash
# ============================================================
#  Kit 1 — Universal Business Core Deployer (Mac)
#  Edit the three lines below, then double-click this file.
# ============================================================

CONFIG_FILE="/Users/yourname/path/to/my-business.json"
N8N_URL="https://yourname.app.n8n.cloud"
N8N_API_KEY="your-n8n-api-key-here"

# ── don't edit below this line ──────────────────────────────

cd "$(dirname "$0")"

echo ""
echo "================================================"
echo "  Kit 1 — Universal Business Core Deployer"
echo "================================================"
echo ""

# Check Python 3
if ! command -v python3 &>/dev/null; then
  echo "ERROR: Python 3 not found."
  echo "Install it from https://www.python.org/downloads/ then try again."
  read -p "Press Enter to close..."
  exit 1
fi

# Install requests if needed
python3 -c "import requests" 2>/dev/null || {
  echo "Installing required packages..."
  pip3 install -r requirements.txt --quiet
}

# Run deploy
python3 setup.py \
  --config "$CONFIG_FILE" \
  --n8n-url "$N8N_URL" \
  --n8n-key "$N8N_API_KEY"

echo ""
read -p "Press Enter to close..."
