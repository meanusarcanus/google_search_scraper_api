# Google SERP & Search Intelligence Extractor (Python SDK)

High-speed, zero rate-limit Python client and library for scraping Google Search Engine Results Pages (SERPs).

## 🚀 Installation
```bash
pip install google-serp-extractor
```

## ⚡ Quick Start
```python
from google_serp_extractor import scrape_google_serp

results = scrape_google_serp("What are the top 5 CRM tools", country_code="us")

print(f"Total Results: {results['total_organic_results']}")
for item in results["organic_results"][:5]:
    print(f"#{item['position']} {item['title']}")
    print(f"  URL: {item['url']}")
```

## 🌐 Cloud API & Apify Actor
* **Apify Store Actor**: [https://apify.com/meanusarcanus/google-serp-ai](https://apify.com/meanusarcanus/google-serp-ai)
* **RapidAPI Hub**: [https://rapidapi.com](https://rapidapi.com)
* **GitHub Repository**: [https://github.com/meanusarcanus/google-serp-extractor](https://github.com/meanusarcanus/google-serp-extractor)
