"""
AI Agent Search & Grounding Engine (Tavily & Exa Alternative)
Transforms raw SERP results into dense, hallucination-resistant Markdown context with citations for LLM agents.
"""

from typing import Dict, Any, List, Optional
from core.serp_scraper import scrape_google_serp
from core.markdown_cleaner import extract_webpage_markdown

def agent_search_and_ground(
    query: str,
    max_results: int = 5,
    max_tokens: int = 2000,
    include_full_content: bool = False,
    country_code: str = "us",
    language_code: str = "en"
) -> Dict[str, Any]:
    """
    Executes live web search and formats results into token-optimized Markdown context for AI LLMs.
    """
    serp_data = scrape_google_serp(
        query=query,
        page_depth=1,
        country_code=country_code,
        language_code=language_code,
        include_paa=True,
        include_paid_ads=False
    )

    organic_results = serp_data.get("organic_results", [])[:max_results]
    paa_items = serp_data.get("people_also_ask", [])[:3]

    sources = []
    markdown_sections = []

    markdown_sections.append(f"# Web Search Context for: \"{query}\"\n")

    # 1. Add People Also Ask context if present
    if paa_items:
        markdown_sections.append("### Key Related Questions & Insights:")
        for paa in paa_items:
            q = paa.get("question", "")
            ans = paa.get("snippet", "")
            if q:
                markdown_sections.append(f"* **{q}**: {ans}")
        markdown_sections.append("")

    # 2. Process organic search results
    markdown_sections.append("### Search Sources & Findings:")
    for idx, item in enumerate(organic_results, start=1):
        title = item.get("title", "Untitled")
        url = item.get("url", "")
        domain = item.get("domain", "")
        snippet = item.get("snippet", "")

        source_entry = {
            "citation_index": idx,
            "title": title,
            "url": url,
            "domain": domain,
            "snippet": snippet
        }

        page_content = snippet
        if include_full_content and url:
            extracted = extract_webpage_markdown(url, max_chars=2500)
            if extracted.get("status") == "success":
                page_content = extracted.get("markdown", snippet)
                source_entry["full_markdown"] = page_content

        sources.append(source_entry)

        markdown_sections.append(
            f"**[{idx}] {title}**  \n"
            f"*Source:* [{domain}]({url})  \n"
            f"{page_content}\n"
        )

    # 3. Assemble full context string
    full_markdown_context = "\n".join(markdown_sections)

    # 4. Token budgeting (1 token ~= 4 chars)
    max_chars = max_tokens * 4
    if len(full_markdown_context) > max_chars:
        full_markdown_context = full_markdown_context[:max_chars] + "\n\n...[Context truncated to meet max_tokens budget]"

    estimated_total_tokens = len(full_markdown_context) // 4

    return {
        "query": query,
        "country_code": country_code.lower(),
        "total_sources": len(sources),
        "estimated_tokens": estimated_total_tokens,
        "context_markdown": full_markdown_context,
        "sources": sources,
        "people_also_ask": paa_items
    }
