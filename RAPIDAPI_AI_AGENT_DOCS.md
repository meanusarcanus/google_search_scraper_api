# 📚 Google SERP & AI Agent Search Intelligence API — Developer Documentation

Welcome to the **Google SERP & AI Agent Search Intelligence API**. This API is engineered as a high-speed, cost-efficient alternative to **Tavily, Exa, and Serper**, delivering live Google search rankings, People Also Ask (PAA) queries, and token-optimized Markdown context for AI LLMs and autonomous agents.

---

## ⚡ 1. Quickstart & Authentication

All requests to the RapidAPI endpoint require authentication headers:

```http
x-rapidapi-key: YOUR_RAPIDAPI_KEY
x-rapidapi-host: google-serp-search-intelligence-extractor-pro.p.rapidapi.com
Content-Type: application/json
```

---

## 🤖 2. Endpoint 1: AI Agent Search & Grounding (`POST /api/v1/agent/search`)

Use this endpoint to provide live web search facts directly to LLMs (OpenAI, Anthropic, Gemini, Llama) without hallucination.

### Request Body:
```json
{
  "query": "Latest breakthroughs in Quantum Computing 2026",
  "max_results": 5,
  "max_tokens": 2000,
  "country_code": "us",
  "language_code": "en",
  "include_full_content": false
}
```

### Key Parameters:
* `query` *(string, required)*: The search term or research question.
* `max_results` *(int, optional, default: 5)*: Top results to include (1–10).
* `max_tokens` *(int, optional, default: 2000)*: Enforces strict token limits for prompt safety.
* `include_full_content` *(bool, optional, default: false)*: When `true`, scrapes the full page content as clean Markdown.
* `country_code` *(string, optional, default: "us")*: Two-letter ISO country code (`us`, `uk`, `ph`, `ca`, `de`, `fr`).

### Response Output:
```json
{
  "query": "Latest breakthroughs in Quantum Computing 2026",
  "country_code": "us",
  "total_sources": 3,
  "estimated_tokens": 405,
  "context_markdown": "# Web Search Context for: \"Latest breakthroughs in Quantum Computing 2026\"\n\n### Key Related Questions & Insights:\n* **What are the top quantum breakthroughs?**: Advanced topological qubits...\n\n### Search Sources & Findings:\n**[1] Quantum Tech Report 2026**\n*Source:* [nature.com](https://nature.com/...)\nBreakthroughs in error-corrected qubits demonstrated...\n",
  "sources": [
    {
      "citation_index": 1,
      "title": "Quantum Tech Report 2026",
      "url": "https://nature.com/...",
      "domain": "nature.com",
      "snippet": "Breakthroughs in error-corrected qubits demonstrated..."
    }
  ]
}
```

---

## 📄 3. Endpoint 2: URL to LLM-Markdown Extractor (`POST /api/v1/agent/extract`)

Extract clean, token-dense Markdown text from any live webpage for RAG vector databases. Automatically strips ads, scripts, navbars, and cookie popups.

### Request Body:
```json
{
  "url": "https://en.wikipedia.org/wiki/Artificial_intelligence",
  "max_chars": 10000
}
```

### Response Output:
```json
{
  "status": "success",
  "url": "https://en.wikipedia.org/wiki/Artificial_intelligence",
  "title": "Artificial intelligence - Wikipedia",
  "markdown": "# Artificial intelligence\n\nArtificial intelligence (AI) is the intelligence of machines...\n\n* Machine Learning\n* Deep Learning",
  "char_count": 8420,
  "estimated_tokens": 2105
}
```

---

## 🔍 4. Endpoint 3: Google SERP Batch Search (`POST /api/v1/search`)

Scrape raw organic rankings, People Also Ask (PAA) questions, and sponsored PPC ads for multiple keywords at once.

### Request Body:
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

---

## 💻 5. Code Examples

### Python (Requests)
```python
import requests

url = "https://google-serp-search-intelligence-extractor-pro.p.rapidapi.com/api/v1/agent/search"

payload = {
    "query": "Best AI agent frameworks 2026",
    "max_results": 5,
    "max_tokens": 2000
}

headers = {
    "x-rapidapi-key": "YOUR_RAPIDAPI_KEY",
    "x-rapidapi-host": "google-serp-search-intelligence-extractor-pro.p.rapidapi.com",
    "Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)
data = response.json()

# Feed context directly to your LLM prompt
llm_context = data["context_markdown"]
print(llm_context)
```

### Node.js / JavaScript (Fetch)
```javascript
const url = 'https://google-serp-search-intelligence-extractor-pro.p.rapidapi.com/api/v1/agent/search';

const options = {
  method: 'POST',
  headers: {
    'x-rapidapi-key': 'YOUR_RAPIDAPI_KEY',
    'x-rapidapi-host': 'google-serp-search-intelligence-extractor-pro.p.rapidapi.com',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    query: 'Best AI agent frameworks 2026',
    max_results: 5
  })
};

fetch(url, options)
  .then(res => res.json())
  .then(data => console.log(data.context_markdown))
  .catch(err => console.error(err));
```

### cURL
```bash
curl --request POST \
	--url https://google-serp-search-intelligence-extractor-pro.p.rapidapi.com/api/v1/agent/search \
	--header 'Content-Type: application/json' \
	--header 'x-rapidapi-host: google-serp-search-intelligence-extractor-pro.p.rapidapi.com' \
	--header 'x-rapidapi-key: YOUR_RAPIDAPI_KEY' \
	--data '{
    "query": "Best AI agent frameworks in 2026",
    "max_results": 5
}'
```

---

## 🤖 6. LangChain & AI Agent Integration

Integrate directly into a LangChain or CrewAI Agent executor:

```python
from langchain.agents import initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI
from langchain.tools import tool
import requests

@tool
def google_agent_search(query: str) -> str:
    """Searches the live web and returns clean Markdown facts with citations."""
    res = requests.post(
        "https://google-serp-search-intelligence-extractor-pro.p.rapidapi.com/api/v1/agent/search",
        json={"query": query, "max_results": 3},
        headers={
            "x-rapidapi-key": "YOUR_RAPIDAPI_KEY",
            "x-rapidapi-host": "google-serp-search-intelligence-extractor-pro.p.rapidapi.com"
        }
    )
    return res.json().get("context_markdown", "No results found.")

llm = ChatOpenAI(temperature=0)
agent = initialize_agent([google_agent_search], llm, agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION)
agent.run("What are the most recent updates on AI agents in 2026?")
```
