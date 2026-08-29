# Google SERP & Search Intelligence Extractor Pro

<p align="center">
  <img src="https://raw.githubusercontent.com/meanusarcanus/google-serp-extractor/master/assets/logo.jpg" alt="Google SERP Intelligence Logo" width="180" style="border-radius: 24px;" />
</p>

<p align="center">
  <b>High-speed, cost-efficient Google Search Engine Results Pages (SERPs) scraper and keyword intelligence extractor.</b>
</p>

---

## 🚀 Overview

**Google SERP & Search Intelligence Extractor Pro** extracts organic search rankings, sponsored PPC ads, People Also Ask (PAA) questions, and domain metrics directly from Google Search Engine Results Pages.

Equipped with automated anti-blocking rotation, country/language localization (`gl`/`hl`), and clean structured JSON output, it is built for SEO auditing, competitor rank tracking, market research, and lead generation.

---

## ✨ Features & Data Extracted

* **🏆 Organic Search Rankings**:
  - Ranking position index (1, 2, 3...)
  - Result page title & headline
  - Clean destination URL & target domain
  - Snippet description text
  - Sitelinks (when available)
* **❓ People Also Ask (PAA)**:
  - Extracted related user question blocks
  - Expandable answer summaries
* **📢 Sponsored PPC Ads**:
  - Sponsored advertiser headline
  - Target ad URL
  - Ad copy snippet
* **🌍 Geolocation & Language Filtering**:
  - Support for any 2-letter ISO country code (`us`, `ph`, `uk`, `ca`, `th`, `de`, etc.)
  - Support for any 2-letter ISO language code (`en`, `es`, `fr`, `th`, `de`, etc.)
* **🛡️ Dual-Engine Resilience**:
  - Zero 429 rate limit blocks with smart search engine fallback.

---

## 📥 Input Configuration

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `search_queries` | Array | `["What are the top 5 CRM tools"]` | List of keywords or topics to query Google SERPs. |
| `page_depth` | Integer | `1` | Number of SERP pagination pages to scrape per query (1 to 5). |
| `country_code` | String | `"us"` | Two-letter ISO country code for localized rankings (e.g. `us`, `ph`, `uk`). |
| `language_code` | String | `"en"` | Two-letter ISO language code (e.g. `en`, `es`, `fr`). |
| `include_paa` | Boolean | `true` | Extract People Also Ask related questions and answers. |
| `include_paid_ads` | Boolean | `true` | Extract sponsored PPC Google ad listings. |

---

## 📤 Sample Output Format

```json
{
  "search_query": "What are the top 5 CRM tools",
  "country_code": "us",
  "language_code": "en",
  "pages_scraped": 1,
  "total_organic_results": 10,
  "organic_results": [
    {
      "position": 1,
      "title": "10 Best CRM Software Of 2026 - Forbes Advisor",
      "url": "https://www.forbes.com/advisor/business/software/best-crm-software/",
      "domain": "forbes.com",
      "snippet": "Forbes Advisor reviewed dozens of CRM options on the market to help you find the best...",
      "sitelinks": []
    }
  ],
  "people_also_ask": [
    {
      "question": "What is the best CRM software for small businesses?",
      "snippet": "Leading solutions offer high performance, security, and scalability..."
    }
  ],
  "sponsored_ads": []
}
```

---

## 🛠️ API & Integration

### REST API Endpoints:
* `GET /api/v1/health` - Health status check.
* `POST /api/v1/search` - Batch search extraction.
* `GET /api/v1/search?q=your+query` - Single query search.

---

## 📄 License
MIT License. Created by [Meanus Arcanus](https://github.com/meanusarcanus).
