"""
Google SERP & AI Agent Search Intelligence Extractor SDK
Official Python client, MCP tools, and LangChain wrappers for AI LLM grounding and web scraping.
"""

from .client import GoogleSerpExtractor, scrape_google_serp, agent_search_and_ground, extract_webpage_markdown

__version__ = "1.1.0"
__all__ = [
    "GoogleSerpExtractor",
    "scrape_google_serp",
    "agent_search_and_ground",
    "extract_webpage_markdown"
]
