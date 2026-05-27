# Business Automation Kits — Full Product Build

7 packaged AI automation kits for small-medium businesses. Each kit is a "set it and go" system built on n8n + Claude AI. Buyers sign in once, everything runs automatically.

---

## The Kits

| # | Kit | Target | Highlights |
|---|-----|--------|-----------|
| 1 | **Universal Business Core** ⭐ | Any small business | Invoicing, payroll, CRM, support, reporting |
| 2 | **Trades Powerhouse** ⭐ | Plumbers, electricians, builders | AI quote engine + WhatsApp loop (flagship demo) |
| 3 | **Real Estate Power Kit** | Agents & property managers | Listing AI, buyer matching, vendor reports |
| 4 | **Health & Wellness Clinic** | Physio, GP, beauty | Booking, billing, patient recall |
| 5 | **Marketing Agency OS** | Agencies, freelancers | Content pipelines, client reporting |
| 6 | **Domination Premium** 💎 | Any — upsell | GBP domination, citations, review velocity |
| 7 | **City Presence Grid** 🏙️ | Any — ultra-premium | Own every search in the city |

---

## Universal Features (every kit)

Every kit ships with all of these:

- **Automated Customer Support** — 3-tier AI support (auto-resolve 70%+ of messages, draft+approve tier, instant escalation). Covers: Gmail, WhatsApp, Facebook Messenger, Instagram DMs, SMS, chatbot, GBP Q&A.
- **AI Chatbot Installer** — scrapes the business website, builds a knowledge base, deploys a live chatbot with lead capture + AI quoting
- **Invoice + payment follow-up**
- **Review velocity engine**
- **Weekly P&L + wrap sheet reports**
- **Lead capture + WhatsApp alerts**
- **Social media autopilot**
- 20+ more universal automations

---

## Kit 7 — City Presence Grid (Premium)

**Goal:** The business appears first across the entire city for any search — their name, their product, their service.

### What it builds:

1. **Multi-Location GBP Network** — a hub-and-spoke network of Google Business Profile listings across every Tier 1 suburb in the city, each with unique Claude-written content
2. **Brand SERP Lock-Out** — owns all 10 positions on page 1 for brand name searches (website, YouTube, LinkedIn, Facebook, Instagram, press, directory)
3. **Google Knowledge Panel** — entity schema + Wikidata submission triggers the Google Knowledge Panel card
4. **City Grid Rank Scanner** — weekly heat map of GBP rank across every suburb, auto-fixes red zones
5. **Competitor Conquest** — bids on competitor brand names in Google Ads, monitors their ratings daily
6. **Product/Service Feed** — Google Shopping feed (products) or Local Service Ads setup (services)
7. **Weekly Auto-Posting** — unique, suburb-specific GBP posts to every profile every week

### Kit 7 Workflows

| File | What it does |
|------|-------------|
| `city-mapper.json` | Maps all suburbs within radius into Tier 1/2/3 priority |
| `gbp-network-builder.json` | Builds the suburb GBP profile network |
| `brand-serp-lockout.json` | Weekly brand SERP audit + gap filling |
| `knowledge-panel-builder.json` | Entity schema + Wikidata + Crunchbase |
| `grid-rank-scanner.json` | City-wide rank heat map + auto red zone fixes |
| `competitor-conquest.json` | Daily competitor monitoring + conquest ads |
| `product-feed-manager.json` | Google Shopping / Local Service Ads |
| `weekly-gbp-auto-poster.json` | Rotating weekly posts to all suburb profiles |

### Kit 7 Integrations

Google Maps API, Google Business Profile API, Google Ads API, Google Merchant Centre, Google Search Console, BrightLocal (grid rank), Semrush (competitor keywords), SerpAPI (SERP checks), Wikidata API, Crunchbase API, PRWeb (press release), Twilio WhatsApp, n8n

---

## Universal — Automated Customer Support

All-channels support workflow: `kit-1-universal-core/workflows/automated-customer-support.json`

**3-Tier System:**
- **Tier 1 Auto:** Claude resolves directly (FAQs, bookings, pricing) — 70%+ of tickets
- **Tier 2 Assisted:** Claude drafts reply → owner one-tap WhatsApp approve
- **Tier 3 Escalate:** Legal/refund/media → instant owner alert + auto holding message

**Channels covered:** Gmail, WhatsApp Business, Facebook Messenger, Instagram DMs, SMS, chatbot, Google Business Profile Q&A

---

## Folder Structure

```
business-automation-kits/
├── kit-1-universal-core/
│   └── workflows/
│       └── automated-customer-support.json   ← UNIVERSAL — in all kits
├── kit-2-trades-powerhouse/
├── kit-3-real-estate/
├── kit-4-health-wellness/
├── kit-5-marketing-agency/
├── kit-6-domination-premium/
├── kit-7-city-presence-grid/
│   ├── workflows/             ← 8 n8n workflow JSON files
│   ├── prompts/               ← 5 Claude system prompt files
│   ├── templates/             ← Schema, audit sheet, product feed
│   └── setup/                 ← Setup guide
└── sales-bundle/
```

---

## Quick Start

1. Set up n8n (cloud or self-hosted)
2. Copy env variables from the kit's setup guide into n8n
3. Import workflow JSON files into n8n
4. Fill the Google Sheet config tab
5. Trigger the first workflow via webhook

See `kit-7-city-presence-grid/setup/KIT7-SETUP-GUIDE.md` for Kit 7 detailed instructions.
