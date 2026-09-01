# 🤖 Google SERP & AI Agent Grounding — Model Context Protocol (MCP) Server

[![MCP Protocol](https://img.shields.io/badge/MCP-Model_Context_Protocol-blue.svg)](https://modelcontextprotocol.io/)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Glama](https://img.shields.io/badge/Glama-MCP_Server-purple.svg)](https://glama.ai/mcp/servers)

A high-performance **Model Context Protocol (MCP) Server** and live Google search grounding engine for **Claude Desktop, Cursor IDE, LangChain, and Autonomous AI Agents**.

<p align="center">
  <img src="https://raw.githubusercontent.com/meanusarcanus/google-serp-extractor/master/assets/logo.jpg" alt="Google SERP MCP Server Logo" width="180" style="border-radius: 24px;" />
</p>

---

## ⚡ Overview

This repository provides a standardized **Model Context Protocol (MCP)** server (`mcp_server.py`) that equips LLMs and autonomous agents with real-time web search and webpage content extraction without hallucination.

* 🛡️ **Zero 429 Rate-Limit Blocks**: Automatic anti-blocking engine with multi-engine fallback.
* 🤖 **LLM-Optimized Grounding**: Returns token-budgeted Markdown context with structured citations (`[1]`, `[2]`).
* 📄 **Universal Markdown Extractor**: Strips navigation, ads, and scripts from any URL to produce dense Markdown for RAG context windows.
* 🔌 **Zero-Config MCP Integration**: Plug-and-play with Claude Desktop, Cursor, and Antigravity.

---

## 🛠️ MCP Tools & Capabilities

The server exposes the following Model Context Protocol (MCP) tools:

| Tool Name | Parameters | Description |
| :--- | :--- | :--- |
| **`search_google_agent`** | `query` *(string)*, `max_results` *(int)*, `max_tokens` *(int)*, `country_code` *(string)* | Searches Google and returns token-optimized Markdown context with structured citations (`[1]`, `[2]`) specifically formatted for LLM system prompts and RAG grounding. |
| **`extract_webpage_markdown`** | `url` *(string)*, `max_chars` *(int)* | Fetches any live URL, strips boilerplate/ads/navbars, and converts the page into clean Markdown text for LLM ingestion. |

---

## 🔌 Quickstart: Connect to Claude Desktop & Cursor

### 1. Claude Desktop Configuration
Add this server to your `claude_desktop_config.json`:

* **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
* **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
* **Linux**: `~/.config/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "google-serp-agent": {
      "command": "python3",
      "args": [
        "/path/to/google-serp-extractor/mcp_server.py"
      ]
    }
  }
}
```

### 2. Cursor IDE Configuration (`.cursor/mcp.json`)
```json
{
  "mcpServers": {
    "google-serp-agent": {
      "command": "python3",
      "args": ["/path/to/google-serp-extractor/mcp_server.py"]
    }
  }
}
```

---

## 📦 Python SDK & LangChain Tool Usage

You can also use this library directly inside Python scripts and LangChain agents:

```bash
pip install google-serp-extractor
```

```python
from google_serp_extractor import agent_search_and_ground, extract_webpage_markdown

# 1. Ground your LLM with real-time web search facts
result = agent_search_and_ground(
    query="Latest breakthroughs in Quantum Computing 2026",
    max_results=3,
    max_tokens=1500
)

# Feed context directly into your LLM prompt
print(result["context_markdown"])

# 2. Extract clean Markdown from any live URL
page_md = extract_webpage_markdown("https://en.wikipedia.org/wiki/Artificial_intelligence")
print(page_md["markdown"][:500])
```

---

## 🌐 Serverless REST API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/api/v1/agent/search` | AI Agent search with token budgeting and citation formatting (Tavily/Exa alternative). |
| `POST` | `/api/v1/agent/extract` | Universal URL-to-Markdown extractor for RAG pipelines. |
| `POST` | `/api/v1/search` | Raw Google SERP batch search with organic rankings, PAA, and ads. |
| `GET` | `/api/v1/health` | Service health status and supported agent capabilities. |

---

## 📄 License
MIT License. Created by Meanus Arcanus.
