"""
Drop-in Agent Tools for LangChain, CrewAI, AutoGen, and LlamaIndex
Allows developers to add AI Google Search & Grounding to any agent framework in 2 lines of code.
"""

from typing import Optional, Dict, Any
from core.agent_search import agent_search_and_ground
from core.markdown_cleaner import extract_webpage_markdown

def google_agent_search_tool(query: str, max_results: int = 5, country_code: str = "us") -> str:
    """
    Standard callable tool for CrewAI, AutoGen, and LangChain Agent executors.
    Returns token-optimized Markdown context with citations.
    """
    data = agent_search_and_ground(query=query, max_results=max_results, country_code=country_code)
    return data.get("context_markdown", "No relevant search results found.")

def url_to_markdown_tool(url: str, max_chars: int = 8000) -> str:
    """
    Standard callable tool for web content extraction and RAG ingestion.
    """
    data = extract_webpage_markdown(url=url, max_chars=max_chars)
    return data.get("markdown", "Failed to extract webpage content.")

# Optional LangChain BaseTool support if langchain is installed
try:
    from langchain.tools import BaseTool
    from pydantic import Field

    class LangChainGoogleAgentSearch(BaseTool):
        name: str = "google_agent_search"
        description: str = "Searches Google and returns clean, token-efficient Markdown context with citations for answering questions and verifying facts."

        def _run(self, query: str) -> str:
            return google_agent_search_tool(query)

        async def _arun(self, query: str) -> str:
            return self._run(query)

    class LangChainWebMarkdownExtractor(BaseTool):
        name: str = "extract_webpage_markdown"
        description: str = "Fetches any URL and extracts clean, ad-free Markdown text for RAG pipelines."

        def _run(self, url: str) -> str:
            return url_to_markdown_tool(url)

        async def _arun(self, url: str) -> str:
            return self._run(url)

except ImportError:
    pass
