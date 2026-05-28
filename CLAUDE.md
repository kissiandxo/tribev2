# Business Automation Kit — Claude Code Instructions

## When a user drags a file into this chat

If the user drops any file (CSV, JSON, .env, .txt, spreadsheet export), treat it as a **business config file** and do the following automatically:

1. Read the file
2. Extract business details: business_name, website_url, industry, city, phone, email, owner_whatsapp, owner_name, and any other fields present
3. Ask the user for their n8n cloud URL and API key if not already known (check env for N8N_URL and N8N_API_KEY first)
4. Run: `python business-automation-kits/deploy/setup.py --config <dropped-file-path> --n8n-url <url> --n8n-key <key>`
5. Show the deployment summary and next steps

## File formats supported
- JSON: `{"business_name": "...", "email": "..."}`
- CSV: Google Sheets export, first row = headers
- .env: `BUSINESS_NAME=Acme Plumbing`
- Plain text: Claude extracts fields using judgment

## Kit deployment order
1. Kit 1 — Universal Business Core (deploy/setup.py)
2. Kit 7 — City Presence Grid (deploy/setup_kit7.py) — coming soon

## Environment variables needed
Set these before running setup.py, or pass as CLI args:
- N8N_URL — e.g. https://yourname.app.n8n.cloud
- N8N_API_KEY — from n8n Settings → API
