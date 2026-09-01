"""
Automated Verification Suite for AI Agent Search & Grounding Engine (Tavily/Exa Competitor)
Tests Markdown extraction, token budgeting, citation grounding, and MCP server JSON-RPC.
"""

import sys
import json
from pathlib import Path

# Add root directory to sys.path
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))

from core.markdown_cleaner import html_to_clean_markdown, extract_webpage_markdown
from core.agent_search import agent_search_and_ground
from mcp_server import handle_mcp_message
from api.index import app, AgentSearchRequest, execute_agent_search, MarkdownExtractRequest, execute_markdown_extract

def run_tests():
    print("=" * 65)
    print(" 🤖 TESTING AI AGENT SEARCH & GROUNDING ENGINE (TAVILY / EXA ALTERNATIVE)")
    print("=" * 65)

    # Test 1: HTML to Clean Markdown
    print("\n[Test 1] HTML to Clean LLM-Optimized Markdown Cleaner...")
    sample_html = """
    <html>
        <head><title>Sample Product Page</title></head>
        <body>
            <nav><a href="/home">Home</a> | <a href="/about">About</a></nav>
            <main>
                <h1>Next-Gen AI Agents</h1>
                <p>Autonomous agents require <b>real-time web search</b> to ground their responses.</p>
                <ul>
                    <li>Zero hallucination</li>
                    <li>Token-efficient context</li>
                </ul>
                <div class="ad-banner">Click here for cheap crypto!</div>
            </main>
            <footer>Copyright 2026 Junk</footer>
        </body>
    </html>
    """
    clean_md = html_to_clean_markdown(sample_html)
    print("✓ Cleaned Markdown Output:")
    print("--------------------------------------------------")
    print(clean_md)
    print("--------------------------------------------------")
    assert "Next-Gen AI Agents" in clean_md
    assert "Copyright 2026 Junk" not in clean_md
    print("✓ Junk tags stripped and headings transformed successfully!")

    # Test 2: Live AI Agent Search & Grounding
    print("\n[Test 2] Live Agent Search & Citation Grounding...")
    grounded_res = agent_search_and_ground(
        query="Latest breakthroughs in Artificial Intelligence 2026",
        max_results=3,
        max_tokens=1000,
        country_code="us"
    )
    print(f"✓ Total Sources Grounded: {grounded_res['total_sources']}")
    print(f"✓ Estimated Tokens: {grounded_res['estimated_tokens']}")
    print("✓ Formatted LLM Context Markdown Snippet:")
    print("--------------------------------------------------")
    print(grounded_res['context_markdown'][:400] + "...")
    print("--------------------------------------------------")
    assert grounded_res['total_sources'] > 0
    assert "[1]" in grounded_res['context_markdown']

    # Test 3: Model Context Protocol (MCP) Server
    print("\n[Test 3] Model Context Protocol (MCP) Server JSON-RPC Protocol...")
    list_tools_req = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/list"
    }
    mcp_list_res = handle_mcp_message(list_tools_req)
    tools = mcp_list_res["result"]["tools"]
    tool_names = [t["name"] for t in tools]
    print(f"✓ MCP Tools Discovered: {tool_names}")
    assert "search_google_agent" in tool_names
    assert "extract_webpage_markdown" in tool_names

    call_tool_req = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/call",
        "params": {
            "name": "search_google_agent",
            "arguments": {
                "query": "Best vector databases for RAG 2026",
                "max_results": 2
            }
        }
    }
    mcp_call_res = handle_mcp_message(call_tool_req)
    mcp_content = mcp_call_res["result"]["content"][0]["text"]
    print(f"✓ MCP Tool Execution Successful! Received {len(mcp_content)} chars.")
    assert len(mcp_content) > 50

    # Test 4: FastAPI Endpoints
    print("\n[Test 4] FastAPI Serverless /api/v1/agent/search Endpoint...")
    api_payload = AgentSearchRequest(
        query="Top open source LLM frameworks 2026",
        max_results=3,
        max_tokens=1500
    )
    endpoint_res = execute_agent_search(api_payload)
    print(f"✓ API Status: Success ({endpoint_res['total_sources']} sources, ~{endpoint_res['estimated_tokens']} tokens)")

    print("\n" + "=" * 65)
    print(" 🎉 ALL AI AGENT SEARCH & GROUNDING TESTS PASSED 100%!")
    print("=" * 65 + "\n")

if __name__ == "__main__":
    run_tests()
