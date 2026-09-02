#!/usr/bin/env python3
"""
Model Context Protocol (MCP) Server for AI Agent Search & Grounding
Provides standardized MCP tools for Claude Desktop, Cursor IDE, and Autonomous AI Agents.
"""

import sys
import json
from pathlib import Path

# Add root directory to sys.path
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))

from core.agent_search import agent_search_and_ground
from core.markdown_cleaner import extract_webpage_markdown

TOOLS = [
    {
        "name": "search_google_agent",
        "description": "Searches Google and returns dense, token-optimized Markdown context with citations specifically formatted for AI LLMs. Use this to ground reasoning and answer questions with up-to-date real-world facts.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query or research topic"
                },
                "max_results": {
                    "type": "integer",
                    "description": "Number of search results to include (default: 5)",
                    "default": 5
                },
                "max_tokens": {
                    "type": "integer",
                    "description": "Maximum token budget for returned markdown (default: 2000)",
                    "default": 2000
                },
                "country_code": {
                    "type": "string",
                    "description": "Two-letter ISO country code for geo-location (e.g. us, ph, uk, ca)",
                    "default": "us"
                }
            },
            "required": ["query"]
        }
    },
    {
        "name": "extract_webpage_markdown",
        "description": "Fetches any live webpage URL, strips navigation/ads/boilerplate, and returns dense, clean Markdown text optimized for LLM RAG pipelines.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "Target webpage URL to scrape and convert to clean Markdown"
                },
                "max_chars": {
                    "type": "integer",
                    "description": "Maximum character limit for output (default: 10000)",
                    "default": 10000
                }
            },
            "required": ["url"]
        }
    }
]

USAGE_FILE = Path.home() / ".mcp_google_serp_usage.json"

def check_mcp_access():
    import os
    key = os.environ.get("RAPIDAPI_KEY") or os.environ.get("SERP_API_KEY")
    if key:
        return True, ""
    count = 0
    if USAGE_FILE.exists():
        try:
            with open(USAGE_FILE) as f:
                count = json.load(f).get("count", 0)
        except Exception:
            pass
    if count >= 10:
        return False, "⚠️ Free trial quota (10 requests) reached for Google SERP AI Grounding MCP server.\nTo unlock unlimited search queries in Claude Desktop & Cursor IDE, please subscribe at: https://rapidapi.com/meanusarcanus/api/microsaas-agent-suite and add 'RAPIDAPI_KEY': 'your_key' to your MCP environment configuration."
    count += 1
    try:
        with open(USAGE_FILE, "w") as f:
            json.dump({"count": count}, f)
    except Exception:
        pass
    return True, ""

def handle_mcp_message(message: dict) -> dict:
    method = message.get("method")
    msg_id = message.get("id")

    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {
                "tools": TOOLS
            }
        }
    elif method == "tools/call":
        allowed, err_msg = check_mcp_access()
        if not allowed:
            return {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "content": [{"type": "text", "text": err_msg}]
                }
            }

        params = message.get("params", {})
        tool_name = params.get("name")
        args = params.get("arguments", {})

        if tool_name == "search_google_agent":
            query = args.get("query", "")
            max_results = args.get("max_results", 5)
            max_tokens = args.get("max_tokens", 2000)
            country_code = args.get("country_code", "us")

            result = agent_search_and_ground(
                query=query,
                max_results=max_results,
                max_tokens=max_tokens,
                country_code=country_code
            )

            return {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": result.get("context_markdown", "")
                        }
                    ]
                }
            }

        elif tool_name == "extract_webpage_markdown":
            url = args.get("url", "")
            max_chars = args.get("max_chars", 10000)

            result = extract_webpage_markdown(url=url, max_chars=max_chars)
            return {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": result.get("markdown", "")
                        }
                    ]
                }
            }
        else:
            return {
                "jsonrpc": "2.0",
                "id": msg_id,
                "error": {
                    "code": -32601,
                    "message": f"Unknown tool: {tool_name}"
                }
            }

    elif method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {}
                },
                "serverInfo": {
                    "name": "google-agent-search-mcp",
                    "version": "1.0.0"
                }
            }
        }
    else:
        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {}
        }

def run_stdio_server():
    """Runs the MCP server reading JSON-RPC from stdin and writing to stdout."""
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            res = handle_mcp_message(req)
            sys.stdout.write(json.dumps(res) + "\n")
            sys.stdout.flush()
        except Exception as e:
            err_res = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {"code": -32700, "message": str(e)}
            }
            sys.stdout.write(json.dumps(err_res) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    run_stdio_server()
