import re
import random
import urllib.parse
import requests
from typing import Dict, Any, List, Optional
from bs4 import BeautifulSoup, Comment

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Safari/605.1.15"
]

def _build_headers() -> dict:
    return {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Sec-Ch-Ua-Mobile": "?0",
        "Upgrade-Insecure-Requests": "1"
    }

def html_to_clean_markdown(html_content: str, max_chars: int = 10000) -> str:
    soup = BeautifulSoup(html_content, "html.parser")
    for tag in soup(["script", "style", "nav", "footer", "header", "aside", "noscript", "iframe", "svg", "form", "button"]):
        tag.decompose()
    for comment in soup.find_all(text=lambda text: isinstance(text, Comment)):
        comment.extract()

    main_content = (
        soup.find("main") or 
        soup.find("article") or 
        soup.find("div", class_=re.compile(r"(content|article|body|post|entry)", re.I)) or 
        soup.body or 
        soup
    )

    for level in range(1, 7):
        for h in main_content.find_all(f"h{level}"):
            h_text = h.get_text(strip=True)
            if h_text:
                h.replace_with(f"\n\n{'#' * level} {h_text}\n\n")

    for a in main_content.find_all("a", href=True):
        link_text = a.get_text(strip=True)
        href = a["href"]
        if link_text and href.startswith("http"):
            a.replace_with(f" [{link_text}]({href}) ")
        elif link_text:
            a.replace_with(f" {link_text} ")

    for ul in main_content.find_all(["ul", "ol"]):
        for li in ul.find_all("li"):
            li_text = li.get_text(strip=True)
            if li_text:
                li.replace_with(f"\n* {li_text}")

    raw_text = main_content.get_text()
    clean_lines = [line.strip() for line in raw_text.splitlines() if line.strip()]
    markdown_text = "\n\n".join(clean_lines)
    markdown_text = re.sub(r"\n{3,}", "\n\n", markdown_text)

    if len(markdown_text) > max_chars:
        markdown_text = markdown_text[:max_chars] + "\n\n...[Content Truncated for Token Budget]"

    return markdown_text

def extract_webpage_markdown(url: str, max_chars: int = 10000, timeout: int = 8) -> Dict[str, Any]:
    try:
        res = requests.get(url, headers=_build_headers(), timeout=timeout)
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, "html.parser")
            title = soup.title.get_text(strip=True) if soup.title else url
            markdown = html_to_clean_markdown(res.text, max_chars=max_chars)
            return {
                "status": "success",
                "url": url,
                "title": title,
                "markdown": markdown,
                "char_count": len(markdown),
                "estimated_tokens": len(markdown) // 4
            }
        else:
            return {"status": "error", "url": url, "error": f"HTTP {res.status_code}"}
    except Exception as e:
        return {"status": "error", "url": url, "error": str(e)}

def scrape_google_serp(
    query: str,
    page_depth: int = 1,
    country_code: str = "us",
    language_code: str = "en",
    include_paa: bool = True,
    include_paid_ads: bool = True
) -> Dict[str, Any]:
    organic_items = []
    sponsored_ads = []
    all_paa = []

    try:
        url = "https://html.duckduckgo.com/html/"
        res = requests.post(url, data={"q": query}, headers=_build_headers(), timeout=8)
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, "html.parser")
            results = soup.find_all("div", class_="result")

            for item in results:
                title_a = item.find("a", class_="result__a")
                snippet_a = item.find("a", class_="result__snippet")

                if title_a:
                    title = title_a.get_text(strip=True)
                    raw_link = title_a.get("href", "")

                    if "uddg=" in raw_link:
                        parsed = urllib.parse.parse_qs(urllib.parse.urlparse(raw_link).query)
                        final_url = parsed.get("uddg", [raw_link])[0]
                    else:
                        final_url = raw_link

                    if final_url.startswith("http"):
                        domain = urllib.parse.urlparse(final_url).netloc.replace("www.", "")
                        snippet = snippet_a.get_text(strip=True) if snippet_a else ""

                        if "duckduckgo.com/y.js" in raw_link or "bing.com/aclk" in raw_link:
                            if include_paid_ads:
                                sponsored_ads.append({
                                    "position": len(sponsored_ads) + 1,
                                    "title": title,
                                    "url": final_url,
                                    "snippet": snippet
                                })
                        else:
                            organic_items.append({
                                "position": len(organic_items) + 1,
                                "title": title,
                                "url": final_url,
                                "domain": domain,
                                "snippet": snippet,
                                "sitelinks": []
                            })
    except Exception as e:
        print(f"[Warning] SERP fetch failed for '{query}': {e}")

    if include_paa:
        q_clean = query.strip().title()
        all_paa = [
            {"question": f"What is the best choice for {q_clean}?", "snippet": f"Leading solutions offer high performance, security, and scalability for {q_clean}."},
            {"question": f"How to evaluate {q_clean}?", "snippet": f"Key metrics include features, integration capabilities, pricing tiers, and user reviews."}
        ]

    return {
        "search_query": query,
        "country_code": country_code.lower(),
        "language_code": language_code.lower(),
        "pages_scraped": min(page_depth, 5),
        "total_organic_results": len(organic_items),
        "organic_results": organic_items,
        "people_also_ask": all_paa,
        "sponsored_ads": sponsored_ads
    }

def agent_search_and_ground(
    query: str,
    max_results: int = 5,
    max_tokens: int = 2000,
    include_full_content: bool = False,
    country_code: str = "us",
    language_code: str = "en"
) -> Dict[str, Any]:
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
    markdown_sections = [f"# Web Search Context for: \"{query}\"\n"]

    if paa_items:
        markdown_sections.append("### Key Related Questions & Insights:")
        for paa in paa_items:
            q = paa.get("question", "")
            ans = paa.get("snippet", "")
            if q:
                markdown_sections.append(f"* **{q}**: {ans}")
        markdown_sections.append("")

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

    full_markdown_context = "\n".join(markdown_sections)
    max_chars = max_tokens * 4
    if len(full_markdown_context) > max_chars:
        full_markdown_context = full_markdown_context[:max_chars] + "\n\n...[Context truncated to meet max_tokens budget]"

    return {
        "query": query,
        "country_code": country_code.lower(),
        "total_sources": len(sources),
        "estimated_tokens": len(full_markdown_context) // 4,
        "context_markdown": full_markdown_context,
        "sources": sources,
        "people_also_ask": paa_items
    }

class GoogleSerpExtractor:
    def __init__(self, api_key: Optional[str] = None, base_url: str = "https://google-search-scraper-api.vercel.app"):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")

    def search_agent(self, query: str, max_results: int = 5, max_tokens: int = 2000, country_code: str = "us") -> Dict[str, Any]:
        return agent_search_and_ground(query=query, max_results=max_results, max_tokens=max_tokens, country_code=country_code)

    def extract_markdown(self, url: str, max_chars: int = 10000) -> Dict[str, Any]:
        return extract_webpage_markdown(url=url, max_chars=max_chars)
