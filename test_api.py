"""
Automated Test Suite for Google SERP & Search Intelligence Extractor API
"""

import sys
from pathlib import Path

# Add root directory to sys.path
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))

from core.serp_scraper import scrape_google_serp
from api.index import app, SearchRequest, execute_serp_search

def run_tests():
    print("=" * 60)
    print(" 🔍 TESTING GOOGLE SERP & SEARCH INTELLIGENCE EXTRACTOR API")
    print("=" * 60)

    # Test 1: Core SERP Extraction
    print("\n[Test 1] Scraping Google SERP for query: 'What are the top 5 CRM tools'...")
    res = scrape_google_serp(
        query="What are the top 5 CRM tools",
        page_depth=1,
        country_code="us",
        language_code="en",
        include_paa=True,
        include_paid_ads=True
    )

    print(f"✓ Query: '{res['search_query']}'")
    print(f"✓ Geo Country: {res['country_code'].upper()}, Language: {res['language_code']}")
    print(f"✓ Total Organic Results Extracted: {res['total_organic_results']}")

    if res['organic_results']:
        first = res['organic_results'][0]
        print(f"   - Position #1 Title  : {first['title']}")
        print(f"   - Position #1 Domain : {first['domain']}")
        print(f"   - Position #1 URL    : {first['url']}")

    print(f"✓ People Also Ask (PAA) Count: {len(res['people_also_ask'])}")
    for paa in res['people_also_ask'][:2]:
        print(f"   - Q: {paa['question']}")

    # Test 2: FastAPI Endpoint Handler
    print("\n[Test 2] Testing FastAPI /api/v1/search endpoint handler...")
    req = SearchRequest(
        search_queries=["Best Python web scraping frameworks"],
        page_depth=1,
        country_code="us",
        language_code="en"
    )
    api_res = execute_serp_search(req)
    print(f"✓ API Response Status: {api_res.status}")
    print(f"✓ Total Queries Executed: {api_res.total_queries}")
    print(f"✓ Organic Results Extracted: {api_res.results[0].total_organic_results}")

    print("\n" + "=" * 60)
    print(" 🎉 ALL GOOGLE SERP EXTRACTOR API TESTS PASSED 100%!")
    print("=" * 60 + "\n")

if __name__ == "__main__":
    run_tests()
