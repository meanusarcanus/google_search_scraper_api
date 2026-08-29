# Google SERP & Search Intelligence Extractor API

Lightweight, high-speed Python Micro-SaaS API & Apify Actor for harvesting organic search rankings, sponsored ads, People Also Ask (PAA) questions, and search metrics directly from Google Search Engine Results Pages (SERPs).

## Features
- **Organic Ranking Extraction**: Extracts title, URL, domain, position index, snippet text, and sitelinks.
- **People Also Ask (PAA)**: Automatically parses related question blocks and answer snippets.
- **Sponsored PPC Ads**: Captures sponsored ad headlines, destination URLs, and snippets.
- **Geo-Location & Language Control**: Supports two-letter ISO country (`gl`) and language (`hl`) codes.
- **Dual Deployment Ready**: FastAPI Serverless (Vercel/RapidAPI) + Standalone Apify Actor.

## API Usage

### 1. Health Check
`GET /api/v1/health`

### 2. Search SERP (POST)
`POST /api/v1/search`
```json
{
  "search_queries": [
    "What are the top 5 CRM tools",
    "Best Python web scraping frameworks"
  ],
  "page_depth": 1,
  "country_code": "us",
  "language_code": "en",
  "include_paa": true,
  "include_paid_ads": true
}
```

### 3. Quick Search (GET)
`GET /api/v1/search?q=Best+Python+web+scraping+tools&country_code=us`

## Local Testing
```bash
python3 test_api.py
```
