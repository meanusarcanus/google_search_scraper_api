import sys
import asyncio
from pathlib import Path
from apify import Actor

# Add parent directory to sys.path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

from core.serp_scraper import scrape_google_serp

async def main():
    async with Actor:
        actor_input = await Actor.get_input() or {}
        
        search_queries = actor_input.get("search_queries", ["Best Python web scraping tools"])
        if isinstance(search_queries, str):
            search_queries = [q.strip() for q in search_queries.split("\n") if q.strip()]

        page_depth = actor_input.get("page_depth", 1)
        country_code = actor_input.get("country_code", "us")
        language_code = actor_input.get("language_code", "en")
        include_paa = actor_input.get("include_paa", True)
        include_paid_ads = actor_input.get("include_paid_ads", True)

        Actor.log.info(f"Starting Google SERP Extraction for {len(search_queries)} queries (Geo: {country_code.upper()}, Lang: {language_code})...")

        for query in search_queries:
            Actor.log.info(f"Querying Google SERP: '{query}'...")
            serp_data = scrape_google_serp(
                query=query,
                page_depth=page_depth,
                country_code=country_code,
                language_code=language_code,
                include_paa=include_paa,
                include_paid_ads=include_paid_ads
            )
            await Actor.push_data(serp_data)

        Actor.log.info("✓ Google SERP Extraction completed successfully!")

if __name__ == "__main__":
    asyncio.run(main())
