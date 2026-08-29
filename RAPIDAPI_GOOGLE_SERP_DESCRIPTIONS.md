# 📝 RapidAPI Short & Long Descriptions for Google SERP Extractor Pro

Below are the pre-written **Short Description** and **Long Description** formatted specifically for your RapidAPI Hub listing.

---

## 📌 1. Short Description (Tagline / Summary - Under 250 Chars)

```text
Extract Google organic rankings, sponsored ads, and People Also Ask (PAA) questions with country/language geolocation targeting in structured JSON.
```

---

## 📜 2. Long Description (Full RapidAPI Overview Markdown)

```markdown
# 🔍 Google SERP & Search Intelligence Extractor Pro

High-speed, developer-friendly Google Search Engine Results Pages (SERPs) API for extracting organic search rankings, sponsored PPC ads, People Also Ask (PAA) questions, and domain metrics with zero 429 rate limit blocks.

---

## 🚀 Key Features & Extracted Data Fields

* **🏆 Organic Search Rankings**: Position index (1, 2, 3...), headline title, destination URL, domain (`forbes.com`, `pcmag.com`), and snippet text.
* **❓ People Also Ask (PAA)**: Related search questions and answers.
* **📢 Sponsored PPC Ads**: Google search ad headlines, destination links, and ad snippets.
* **🌍 Geolocation & Language Filtering**: Supports any 2-letter ISO country code (`us`, `ph`, `uk`, `ca`, `th`, `de`) and language code (`en`, `es`, `fr`, `th`).
* **🛡️ Zero Rate-Limit Blocks**: Automated anti-blocking rotation for 100% reliable uptime.

---

## 🛠️ Example Use Cases

1. **Automated SEO Rank Tracking**: Monitor keyword rankings across countries without maintaining browser farms.
2. **Competitor SERP Analysis**: Analyze who ranks on page #1 for target industry keywords.
3. **PPC Ad Monitoring**: Track competitor sponsored ads and search copy.
4. **AI & LLM Grounding**: Feed real-time Google search results into AI models and autonomous agents.

---

## 📥 Sample Request Payload (POST /api/v1/search)

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

## 📤 Sample Response Payload

```json
{
  "status": "success",
  "total_queries": 1,
  "results": [
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
  ]
}
```
```
