"""
Universal HTML to LLM-Optimized Markdown Cleaner
Strips boilerplate, navigation, ads, and scripts to generate token-efficient Markdown for LLM RAG pipelines.
"""

import re
import urllib.parse
import requests
from typing import Optional, Dict, Any
from bs4 import BeautifulSoup, Comment

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9"
}

def html_to_clean_markdown(html_content: str, max_chars: int = 10000) -> str:
    """
    Converts raw HTML into clean, token-efficient Markdown text.
    """
    soup = BeautifulSoup(html_content, "html.parser")

    # 1. Strip non-content and junk tags
    for tag in soup(["script", "style", "nav", "footer", "header", "aside", "noscript", "iframe", "svg", "form", "button"]):
        tag.decompose()

    # Remove HTML comments
    for comment in soup.find_all(text=lambda text: isinstance(text, Comment)):
        comment.extract()

    # Target main content container if available
    main_content = (
        soup.find("main") or 
        soup.find("article") or 
        soup.find("div", class_=re.compile(r"(content|article|body|post|entry)", re.I)) or 
        soup.body or 
        soup
    )

    # 2. Transform headers
    for level in range(1, 7):
        for h in main_content.find_all(f"h{level}"):
            h_text = h.get_text(strip=True)
            if h_text:
                h.replace_with(f"\n\n{'#' * level} {h_text}\n\n")

    # 3. Transform links with meaningful anchors
    for a in main_content.find_all("a", href=True):
        link_text = a.get_text(strip=True)
        href = a["href"]
        if link_text and href.startswith("http"):
            a.replace_with(f" [{link_text}]({href}) ")
        elif link_text:
            a.replace_with(f" {link_text} ")

    # 4. Transform lists
    for ul in main_content.find_all(["ul", "ol"]):
        for li in ul.find_all("li"):
            li_text = li.get_text(strip=True)
            if li_text:
                li.replace_with(f"\n* {li_text}")

    # 5. Extract text and clean excess whitespace
    raw_text = main_content.get_text()
    clean_lines = []
    for line in raw_text.splitlines():
        line = line.strip()
        if line:
            clean_lines.append(line)

    markdown_text = "\n\n".join(clean_lines)

    # Collapse multiple blank lines
    markdown_text = re.sub(r"\n{3,}", "\n\n", markdown_text)

    if len(markdown_text) > max_chars:
        markdown_text = markdown_text[:max_chars] + "\n\n...[Content Truncated for Token Budget]"

    return markdown_text

def extract_webpage_markdown(url: str, max_chars: int = 10000, timeout: int = 8) -> Dict[str, Any]:
    """
    Fetches a live URL and returns structured clean Markdown with metadata.
    """
    try:
        res = requests.get(url, headers=HEADERS, timeout=timeout)
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, "html.parser")
            title = soup.title.get_text(strip=True) if soup.title else url
            markdown = html_to_clean_markdown(res.text, max_chars=max_chars)
            
            # Approximate token count (1 token ~= 4 chars)
            estimated_tokens = len(markdown) // 4

            return {
                "status": "success",
                "url": url,
                "title": title,
                "markdown": markdown,
                "char_count": len(markdown),
                "estimated_tokens": estimated_tokens
            }
        else:
            return {
                "status": "error",
                "url": url,
                "error": f"HTTP {res.status_code}"
            }
    except Exception as e:
        return {
            "status": "error",
            "url": url,
            "error": str(e)
        }
