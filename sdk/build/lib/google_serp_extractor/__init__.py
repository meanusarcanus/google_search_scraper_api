"""
Google SERP & Search Intelligence Extractor SDK
Official Python client & CLI for extracting Google search rankings, sponsored ads, and People Also Ask queries.
"""

from .client import GoogleSerpExtractor, scrape_google_serp

__version__ = "1.0.0"
__all__ = ["GoogleSerpExtractor", "scrape_google_serp"]
