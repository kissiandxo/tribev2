#!/usr/bin/env python3
"""
Universal Business Core — Kit 1 Deploy Script
Deploys all 8 workflows to an n8n cloud instance.

Usage:
  python setup.py --config <path-to-business-config-file> --n8n-url <url> --n8n-key <api-key>

Or use env vars: N8N_URL, N8N_API_KEY
"""

import argparse
import csv
import json
import os
import sys
from pathlib import Path

try:
    import requests
except ImportError:
    print("ERROR: 'requests' library not found. Run: pip install requests")
    sys.exit(1)


# ---------------------------------------------------------------------------
# Config parsing
# ---------------------------------------------------------------------------

REQUIRED_FIELDS = [
    "business_name",
    "website_url",
    "industry",
    "city",
    "phone",
    "email",
    "owner_whatsapp",
    "owner_name",
    "google_review_link",
]

OPTIONAL_FIELDS = [
    "facebook_page_id",
    "instagram_account_id",
]

PLACEHOLDER_API_KEYS = [
    ("TWILIO_ACCOUNT_SID", "get from twilio.com"),
    ("TWILIO_AUTH_TOKEN", "get from twilio.com"),
    ("TWILIO_PHONE_NUMBER", "your Twilio WhatsApp-enabled number, e.g. +61400000000"),
    ("ANTHROPIC_API_KEY", "get from console.anthropic.com"),
    ("GOOGLE_SHEETS_CREDENTIALS", "service account JSON from Google Cloud Console"),
    ("BUSINESS_CONFIG_SHEET_ID", "your Google Sheets document ID from the URL"),
    ("GOOGLE_MAPS_API_KEY", "get from console.cloud.google.com"),
    ("GOOGLE_PLACE_ID", "your Google Maps place_id"),
    ("GOOGLE_BUSINESS_ACCOUNT_ID", "from Google Business Profile API"),
    ("GOOGLE_BUSINESS_LOCATION_ID", "from Google Business Profile API"),
    ("GOOGLE_BUSINESS_ACCESS_TOKEN", "OAuth2 token from Google Business Profile"),
    ("FACEBOOK_PAGE_ACCESS_TOKEN", "from Meta for Developers — Page Access Token"),
    ("INSTAGRAM_DEFAULT_IMAGE_URL", "default image URL for Instagram posts (optional)"),
    ("N8N_WEBHOOK_URL", "your n8n webhook base URL, e.g. https://yourname.app.n8n.cloud/webhook"),
]


def parse_json_config(path: str) -> dict:
    with open(path, "r") as f:
        return json.load(f)


def parse_csv_config(path: str) -> dict:
    config = {}
    with open(path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # First row is used
            config = {k.strip().lower().replace(" ", "_"): v.strip() for k, v in row.items()}
            break
    return config


def parse_env_config(path: str) -> dict:
    config = {}
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                key, _, value = line.partition("=")
                # Strip quotes
                value = value.strip().strip('"').strip("'")
                config[key.strip().lower()] = value
    return config


def parse_text_config(path: str) -> dict:
    """Best-effort key:value extraction from plain text."""
    config = {}
    with open(path, "r") as f:
        content = f.read()

    known_patterns = {
        "business_name": ["business name", "business:", "company name", "company:"],
        "website_url": ["website", "url:", "site:"],
        "industry": ["industry:", "sector:", "type of business"],
        "city": ["city:", "location:", "suburb:", "town:"],
        "phone": ["phone:", "telephone:", "mobile:", "contact number"],
        "email": ["email:", "e-mail:"],
        "owner_whatsapp": ["whatsapp:", "owner whatsapp", "owner mobile"],
        "owner_name": ["owner:", "owner name:", "contact name:"],
        "google_review_link": ["google review", "review link", "google maps"],
        "facebook_page_id": ["facebook page id", "fb page id"],
        "instagram_account_id": ["instagram account", "ig account id"],
    }

    lines = content.split("\n")
    for line in lines:
        line_lower = line.lower()
        for field, patterns in known_patterns.items():
            for pattern in patterns:
                if pattern in line_lower and ":" in line:
                    value = line.split(":", 1)[1].strip()
                    if value and field not in config:
                        config[field] = value
                    break

    return config


def load_config(path: str) -> dict:
    """Auto-detect format and parse the config file."""
    suffix = Path(path).suffix.lower()
    name = Path(path).name.lower()

    if suffix == ".json":
        raw = parse_json_config(path)
    elif suffix == ".csv":
        raw = parse_csv_config(path)
    elif suffix == ".env" or name == ".env":
        raw = parse_env_config(path)
    else:
        # Try JSON first, then env format, then plain text
        try:
            raw = parse_json_config(path)
        except (json.JSONDecodeError, UnicodeDecodeError):
            try:
                raw = parse_env_config(path)
                if not raw:
                    raw = parse_text_config(path)
            except Exception:
                raw = parse_text_config(path)

    # Normalise keys: lowercase, underscores
    return {k.lower().replace("-", "_").replace(" ", "_"): v for k, v in raw.items()}


def prompt_missing_fields(config: dict) -> dict:
    """Interactively prompt for any missing required fields."""
    print("\n--- Business Details ---")
    for field in REQUIRED_FIELDS:
        if not config.get(field):
            value = input(f"  Enter {field.replace('_', ' ').title()}: ").strip()
            config[field] = value

    print("\n--- Optional Fields (press Enter to skip) ---")
    for field in OPTIONAL_FIELDS:
        if not config.get(field):
            value = input(f"  Enter {field.replace('_', ' ').title()} (optional): ").strip()
            if value:
                config[field] = value

    return config


# ---------------------------------------------------------------------------
# n8n API
# ---------------------------------------------------------------------------

class N8NClient:
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url.rstrip("/")
        self.api_url = f"{self.base_url}/api/v1"
        self.session = requests.Session()
        self.session.headers.update({
            "X-N8N-API-KEY": api_key,
            "Content-Type": "application/json",
            "Accept": "application/json",
        })

    def test_connection(self) -> bool:
        """Test the n8n API connection. Returns True if successful."""
        try:
            resp = self.session.get(f"{self.api_url}/workflows", timeout=10)
            if resp.status_code == 401:
                print(f"\nERROR: Authentication failed (401). Check your n8n API key.")
                return False
            if resp.status_code == 403:
                print(f"\nERROR: Forbidden (403). API key may not have workflow permissions.")
                return False
            if resp.status_code >= 400:
                print(f"\nERROR: n8n API returned {resp.status_code}: {resp.text[:200]}")
                return False
            resp.raise_for_status()
            return True
        except requests.exceptions.ConnectionError:
            print(f"\nERROR: Could not connect to {self.base_url}")
            print("  Check that the URL is correct and n8n is running.")
            return False
        except requests.exceptions.Timeout:
            print(f"\nERROR: Connection to {self.base_url} timed out.")
            return False

    def import_workflow(self, workflow_data: dict) -> dict | None:
        """Import (create) a workflow. Returns the created workflow object or None."""
        try:
            # n8n import endpoint
            resp = self.session.post(
                f"{self.api_url}/workflows",
                json=workflow_data,
                timeout=30,
            )
            if resp.status_code in (200, 201):
                return resp.json()
            else:
                print(f"    ERROR {resp.status_code}: {resp.text[:300]}")
                return None
        except Exception as e:
            print(f"    ERROR: {e}")
            return None

    def activate_workflow(self, workflow_id: str) -> bool:
        """Activate a workflow by ID."""
        try:
            resp = self.session.post(
                f"{self.api_url}/workflows/{workflow_id}/activate",
                timeout=15,
            )
            return resp.status_code in (200, 201)
        except Exception:
            return False

    def set_variables(self, variables: dict) -> bool:
        """Attempt to set n8n environment variables via the API."""
        # n8n cloud supports /variables endpoint (available in n8n >= 1.0)
        all_ok = True
        for key, value in variables.items():
            try:
                # First check if variable exists
                list_resp = self.session.get(f"{self.api_url}/variables", timeout=10)
                existing = {}
                if list_resp.ok:
                    for var in list_resp.json().get("data", []):
                        existing[var.get("key")] = var.get("id")

                if key in existing:
                    # Update existing
                    var_id = existing[key]
                    resp = self.session.patch(
                        f"{self.api_url}/variables/{var_id}",
                        json={"value": str(value)},
                        timeout=10,
                    )
                else:
                    # Create new
                    resp = self.session.post(
                        f"{self.api_url}/variables",
                        json={"key": key, "value": str(value)},
                        timeout=10,
                    )

                if not resp.ok:
                    all_ok = False
            except Exception:
                all_ok = False

        return all_ok


# ---------------------------------------------------------------------------
# Workflow discovery
# ---------------------------------------------------------------------------

WORKFLOW_DISPLAY_NAMES = {
    "automated-customer-support": "Automated Customer Support",
    "invoice-payment-followup": "Invoice & Payment Follow-up",
    "review-velocity-engine": "Review Velocity Engine",
    "lead-capture-whatsapp": "Lead Capture + WhatsApp",
    "social-media-autopilot": "Social Media Autopilot",
    "ai-chatbot-installer": "AI Chatbot Installer",
    "crm-pipeline": "CRM Pipeline",
    "weekly-pl-report": "Weekly P&L Report",
}


def find_workflow_files(kit_dir: Path) -> list[Path]:
    """Return all workflow JSON files sorted by display order."""
    workflows_dir = kit_dir / "kit-1-universal-core" / "workflows"
    if not workflows_dir.exists():
        print(f"\nERROR: Workflows directory not found: {workflows_dir}")
        sys.exit(1)

    order = list(WORKFLOW_DISPLAY_NAMES.keys())
    files = list(workflows_dir.glob("*.json"))

    def sort_key(p: Path) -> int:
        stem = p.stem
        try:
            return order.index(stem)
        except ValueError:
            return 999

    return sorted(files, key=sort_key)


# ---------------------------------------------------------------------------
# Summary printer
# ---------------------------------------------------------------------------

def print_summary(
    n8n_url: str,
    results: list[dict],
    config: dict,
) -> None:
    print("\n" + "=" * 60)
    print("✅ Kit 1 — Universal Business Core deployed to n8n")
    print("=" * 60)

    print(f"\nWorkflows imported ({len(results)}):")
    for r in results:
        if r["success"]:
            url = f"{n8n_url}/workflow/{r['id']}"
            print(f"  ✅ {r['display_name']:<35} → {url}")
        else:
            print(f"  ❌ {r['display_name']:<35} → FAILED ({r.get('error', 'unknown error')})")

    print("\n⚠️  Action required — paste these API keys into n8n:")
    for key, hint in PLACEHOLDER_API_KEYS:
        print(f"  • {key:<35} ({hint})")

    website = config.get("website_url", "https://yourwebsite.com")
    business_name = config.get("business_name", "Your Business")
    print(f"""
Next step: Run the chatbot installer webhook to scrape your website:

  curl -X POST {n8n_url}/webhook/install-chatbot \\
    -H "Content-Type: application/json" \\
    -d '{{"website_url": "{website}", "business_name": "{business_name}"}}'
""")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def build_env_variables(config: dict) -> dict:
    """Build the dict of n8n env vars to set from the business config."""
    return {
        "BUSINESS_NAME": config.get("business_name", ""),
        "BUSINESS_WEBSITE": config.get("website_url", ""),
        "BUSINESS_INDUSTRY": config.get("industry", ""),
        "BUSINESS_CITY": config.get("city", ""),
        "BUSINESS_PHONE": config.get("phone", ""),
        "BUSINESS_EMAIL": config.get("email", ""),
        "OWNER_WHATSAPP": config.get("owner_whatsapp", ""),
        "OWNER_NAME": config.get("owner_name", ""),
        "GOOGLE_REVIEW_LINK": config.get("google_review_link", ""),
        "FACEBOOK_PAGE_ID": config.get("facebook_page_id", ""),
        "INSTAGRAM_ACCOUNT_ID": config.get("instagram_account_id", ""),
        # Placeholders — user must fill these in n8n
        "TWILIO_ACCOUNT_SID": config.get("twilio_account_sid", "FILL_IN_REQUIRED"),
        "TWILIO_AUTH_TOKEN": config.get("twilio_auth_token", "FILL_IN_REQUIRED"),
        "TWILIO_PHONE_NUMBER": config.get("twilio_phone_number", "FILL_IN_REQUIRED"),
        "ANTHROPIC_API_KEY": config.get("anthropic_api_key", "FILL_IN_REQUIRED"),
        "GOOGLE_SHEETS_CREDENTIALS": config.get("google_sheets_credentials", "FILL_IN_REQUIRED"),
        "BUSINESS_CONFIG_SHEET_ID": config.get("business_config_sheet_id", "FILL_IN_REQUIRED"),
        "SERPAPI_KEY": config.get("serpapi_key", "FILL_IN_REQUIRED"),
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Deploy Kit 1 — Universal Business Core to n8n"
    )
    parser.add_argument(
        "--config", "-c",
        help="Path to business config file (JSON, CSV, .env, or plain text)",
    )
    parser.add_argument(
        "--n8n-url",
        default=os.environ.get("N8N_URL", ""),
        help="n8n instance URL (or set N8N_URL env var)",
    )
    parser.add_argument(
        "--n8n-key",
        default=os.environ.get("N8N_API_KEY", ""),
        help="n8n API key (or set N8N_API_KEY env var)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Parse config and list workflows without deploying",
    )
    args = parser.parse_args()

    print("\n🚀 Kit 1 — Universal Business Core Setup")
    print("=" * 60)

    # --- Load config ---
    config = {}
    if args.config:
        print(f"\nReading config from: {args.config}")
        try:
            config = load_config(args.config)
            print(f"  Found {len(config)} fields in config file.")
        except FileNotFoundError:
            print(f"\nERROR: Config file not found: {args.config}")
            sys.exit(1)
        except Exception as e:
            print(f"\nERROR reading config file: {e}")
            sys.exit(1)
    else:
        print("\nNo config file provided. You'll be prompted for business details.")

    # --- Prompt for missing fields ---
    config = prompt_missing_fields(config)

    # --- Get n8n credentials ---
    n8n_url = args.n8n_url.strip().rstrip("/")
    n8n_key = args.n8n_key.strip()

    if not n8n_url:
        n8n_url = input("\n  Enter your n8n instance URL (e.g. https://yourname.app.n8n.cloud): ").strip().rstrip("/")
    if not n8n_key:
        n8n_key = input("  Enter your n8n API key (from Settings → API): ").strip()

    if not n8n_url or not n8n_key:
        print("\nERROR: n8n URL and API key are required.")
        sys.exit(1)

    # --- Find workflow files ---
    script_dir = Path(__file__).parent
    kit_dir = script_dir.parent
    workflow_files = find_workflow_files(kit_dir)

    print(f"\nFound {len(workflow_files)} workflow files:")
    for wf in workflow_files:
        display = WORKFLOW_DISPLAY_NAMES.get(wf.stem, wf.stem)
        print(f"  • {display} ({wf.name})")

    if args.dry_run:
        print("\n[DRY RUN] Skipping deployment. Config parsed successfully.")
        print(f"\nBusiness: {config.get('business_name')}")
        print(f"Website:  {config.get('website_url')}")
        print(f"n8n URL:  {n8n_url}")
        sys.exit(0)

    # --- Connect to n8n ---
    print(f"\nConnecting to n8n at {n8n_url}...")
    client = N8NClient(n8n_url, n8n_key)

    if not client.test_connection():
        sys.exit(1)
    print("  ✅ Connected to n8n successfully.")

    # --- Set environment variables ---
    print("\nSetting n8n environment variables...")
    env_vars = build_env_variables(config)
    ok = client.set_variables(env_vars)
    if ok:
        print(f"  ✅ {len(env_vars)} variables set.")
    else:
        print("  ⚠️  Some variables could not be set via API.")
        print("      You can set them manually in n8n Settings → Variables.")

    # --- Import workflows ---
    print("\nImporting workflows...")
    results = []

    for wf_file in workflow_files:
        display_name = WORKFLOW_DISPLAY_NAMES.get(wf_file.stem, wf_file.stem)
        print(f"  Importing: {display_name}...", end=" ", flush=True)

        try:
            with open(wf_file, "r") as f:
                workflow_data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"FAILED (invalid JSON: {e})")
            results.append({
                "display_name": display_name,
                "success": False,
                "error": f"Invalid JSON: {e}",
            })
            continue

        created = client.import_workflow(workflow_data)

        if created:
            workflow_id = created.get("id", "unknown")

            # Activate the workflow
            activated = client.activate_workflow(workflow_id)
            status = "✅" if activated else "✅ (activation failed — activate manually)"
            print(f"{status} (ID: {workflow_id})")

            results.append({
                "display_name": display_name,
                "success": True,
                "id": workflow_id,
            })
        else:
            print("FAILED")
            results.append({
                "display_name": display_name,
                "success": False,
                "error": "Import returned no data",
            })

    # --- Summary ---
    print_summary(n8n_url, results, config)

    success_count = sum(1 for r in results if r["success"])
    fail_count = len(results) - success_count

    if fail_count > 0:
        print(f"⚠️  {fail_count} workflow(s) failed to import. Check errors above.")
        sys.exit(1)
    else:
        print(f"All {success_count} workflows imported and activated. Setup complete! 🎉")


if __name__ == "__main__":
    main()
