# Kit 7 — City Presence Grid: Setup Guide

**Total setup time:** 2–4 hours (most is automated)
**What you need:** Google account, Twilio account, n8n instance, API keys listed below

---

## What This Kit Does

Kit 7 makes your business appear first — or in the top 3 — for every search across every suburb in your city. It builds a network of Google Business Profiles across the city, locks out page 1 for your brand name, gets you a Google Knowledge Panel, and hunts down competitor traffic.

**End result:** When anyone in your city searches your business name, your product, or your service — you show up. Multiple times. In multiple positions.

---

## Required API Keys / Credentials

Paste these into your n8n Environment Variables before running any workflow.

| Variable | What It's For | Where to Get It |
|----------|--------------|-----------------|
| `GOOGLE_MAPS_API_KEY` | Suburb geocoding, competitor GBP lookup | console.cloud.google.com → APIs → Maps |
| `GBP_ACCOUNT_ID` | Your Google Business Profile account ID | business.google.com → account info |
| `GOOGLE_ADS_CUSTOMER_ID` | Google Ads account number | ads.google.com → account settings |
| `GMC_MERCHANT_ID` | Google Merchant Centre (products only) | merchants.google.com |
| `SERPAPI_KEY` | Brand SERP rank checking | serpapi.com → dashboard |
| `BRIGHTLOCAL_API_KEY` | City-wide grid rank scanning | brightlocal.com → API |
| `SEMRUSH_API_KEY` | Competitor keyword analysis | semrush.com → API |
| `PRWEB_API_KEY` | Press release distribution | prweb.com → account |
| `WIKIDATA_EDIT_TOKEN` | Wikidata entity creation | wikidata.org → create account → get token |
| `OWNER_WHATSAPP` | Your WhatsApp number for alerts | e.g. +61412345678 |
| `CITY_GRID_SHEET_ID` | Google Sheet ID for all data storage | Create a new Google Sheet, copy the ID from the URL |
| `BUSINESS_CONFIG_SHEET_ID` | Business config sheet (can be same as above) | Same sheet, different tab |
| `N8N_WEBHOOK_BASE_URL` | Your n8n instance URL | e.g. https://your-n8n.app.n8n.cloud/webhook |

---

## Google Sheet Setup

Create one Google Sheet named **"[Business Name] — City Grid"** and add these tabs:

| Tab Name | Purpose |
|----------|---------|
| `Business Config` | One row with all business details |
| `Suburb Tiers` | Filled automatically by city-mapper workflow |
| `GBP Profiles` | All created GBP profiles and IDs |
| `Competitors` | List of up to 5 competitors |
| `SERP Audit Log` | Weekly brand SERP scores |
| `Grid Rank History` | Weekly heat map data |
| `Competitor Log` | Daily competitor monitoring data |
| `Knowledge Base` | Business Q&A, services, policies (also used by chatbot) |
| `Support Log` | All customer support tickets |

### Business Config Tab — Required Columns:
`business_name | website_url | industry | city | state | city_centre_suburb | service_radius_km | owner_name | owner_whatsapp | phone | email | founded_year | services | target_keywords | uvp | monthly_ad_budget | business_type (product/service)`

---

## Step-by-Step Setup

### Step 1: Fill Business Config (5 minutes)
Fill out the Business Config tab in your Google Sheet. This is the data source for all workflows.

### Step 2: Run City Mapper (10 minutes)
1. Import `city-mapper.json` into n8n
2. Set your `CITY_GRID_SHEET_ID` in n8n environment variables
3. Trigger the webhook with your business details:
```json
{
  "business_name": "Your Business Name",
  "city": "Sydney",
  "service_radius_km": 30,
  "industry": "plumber",
  "owner_whatsapp": "+61412345678"
}
```
4. Wait for WhatsApp confirmation (2–5 minutes)
5. Check the Suburb Tiers tab — your city is mapped

### Step 3: Run GBP Network Builder (30–60 minutes)
1. Import `gbp-network-builder.json` into n8n
2. Ensure your Google OAuth2 credentials are set up in n8n with `mybusiness.business.manage` scope
3. The city mapper triggers this automatically, OR trigger it manually from the webhook
4. Watch WhatsApp for progress updates as each suburb profile is created
5. **Note:** Google may require phone/postcard verification for new GBP listings. Claude flags these for your action.

### Step 4: Run Knowledge Panel Builder (20 minutes)
1. Import `knowledge-panel-builder.json`
2. Trigger the webhook with your full business profile
3. Find the generated Google Doc with your schema markup
4. Paste the schema code into your website `<head>` (or ask your web developer)
5. Validate at: https://search.google.com/test/rich-results

### Step 5: Activate Brand SERP Lock-Out (5 minutes)
1. Import `brand-serp-lockout.json`
2. Activate the cron — runs every Monday at 7am automatically
3. First run: Claude audits your brand SERP and starts creating any missing assets
4. Check WhatsApp Monday morning for your SERP ownership score

### Step 6: Activate Grid Rank Scanner (5 minutes)
1. Import `grid-rank-scanner.json`
2. Activate the cron — runs every Wednesday at 6am automatically
3. First run generates your city heat map and auto-fixes red zones

### Step 7: Activate Competitor Conquest (5 minutes)
1. Fill the `Competitors` tab in your Google Sheet (up to 5 competitors: name, website, GBP place ID)
2. Import `competitor-conquest.json`
3. Activate — runs daily at 5am
4. First run: creates conquest Google Ads campaigns for each competitor's brand name

### Step 8: Product Feed / LSA (10 minutes)
1. Import `product-feed-manager.json`
2. If product business: ensure `GMC_MERCHANT_ID` is set and Google Merchant Centre is connected
3. If service business: check your Google Docs for the LSA setup guide
4. Activate cron — runs daily at 3am

---

## Weekly Routine (automated — nothing to do)

| Day | What Happens Automatically |
|-----|---------------------------|
| Monday 7am | Brand SERP audit → gaps filled → you get a SERP score WhatsApp |
| Wednesday 6am | City grid rank scan → red zones identified → fix posts published |
| Daily 5am | Competitor monitoring → bid adjustments → alerts if something big changes |
| Daily 3am | Product feed / LSA refresh |

---

## Understanding Your Reports

### WhatsApp Brand SERP Report (Monday)
> "You own 8/10 page-1 positions for 'Bondi Plumbing'"
- 10/10 = perfect. Competitor has nowhere to appear.
- Below 7/10 = urgent — blank positions are owned by competitors or directories with bad info

### WhatsApp Grid Rank Report (Wednesday)
> "City coverage score: 67% — 23 green zones, 8 red zones"
- Green = #1–3 rank in that suburb ✅
- Yellow = #4–7 rank ⚠️
- Red = #8+ or not ranking ❌
- Red zones get auto-fix posts published. Takes 4–8 weeks to see movement.

### Competitor Alert
> "XYZ Plumbing just dropped from 4.8 to 4.3 stars — bid increased 30% to capture their leads"
- This is your moment to strike. Act on these alerts.

---

## How Long Until Results?

| Signal | Timeframe |
|--------|-----------|
| New GBP profiles indexed | 1–4 weeks |
| Google Knowledge Panel | 4–12 weeks |
| Suburb page-1 ranking | 6–16 weeks (depends on competition) |
| Review velocity compound effect | 3–6 months |
| Full city domination | 6–12 months |

**Important:** Local SEO is a compounding asset. The longer the system runs, the stronger it gets. Every review, post, and backlink adds to an increasingly hard-to-beat presence.

---

## GBP Policy Compliance

Google's terms allow service area businesses to create one listing per service area. However:
- All listings must represent a real physical presence OR a genuine service area business
- Do not create listings for areas you genuinely do not service
- Each listing must have a unique business description (handled automatically by Claude)
- Listings must have accurate, up-to-date information at all times

The GBP Network Builder creates only service area listings (no physical storefront address listed) — this is Google-compliant for businesses that visit customers rather than customers visiting them (trades, cleaners, gardeners, mobile services).

---

## Troubleshooting

**GBP listing got suspended:**
Google sometimes suspends new listings for verification. This is normal. Check your Google Business Profile dashboard and follow the verification steps. Once verified, the listing reinstates.

**Knowledge Panel not showing after 8 weeks:**
- Ensure schema markup is live on the website (validate at Rich Results Test)
- Check that all sameAs links in the schema point to real, live profiles
- Add more citations (50+ directories is the target)
- Get more press mentions (run the press release workflow)

**Grid rank not improving after 6 weeks:**
- Check that GBP posts are actually publishing (n8n execution logs)
- Ensure review requests are going out after completed jobs (check Support Log)
- The suburb may require a closer GBP profile — consider adding a Tier 2 profile for that area

---

## Support

For setup assistance, n8n node issues, or API configuration: refer to `TROUBLESHOOTING.pdf` in this kit or reach out through the product support channel.
