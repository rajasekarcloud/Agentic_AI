"""Simple news MCP server backed by the GNews API (https://gnews.io).

Tools:
  - search_news:        search articles by keyword
  - get_top_headlines:  top headlines by category / country

Requires the GNEWS_API_KEY environment variable.
"""
import os
import sys
from dotenv import load_dotenv
import httpx2

try:  # mcp 2.x
    from mcp.server.mcpserver import MCPServer as FastMCP
except ImportError:  # mcp 1.x
    from mcp.server.fastmcp import FastMCP

load_dotenv()
GNEWS_BASE_URL = "https://gnews.io/api/v4"
CATEGORIES = {
    "general", "world", "nation", "business", "technology",
    "entertainment", "sports", "science", "health",
}

mcp = FastMCP("gnews")


async def _fetch(endpoint: str, params: dict) -> str:
    """Call the GNews API and return a readable text summary of the articles."""
    api_key = os.getenv("GNEWS_API_KEY")
    if not api_key:
        return "Error: GNEWS_API_KEY environment variable is not set."

    params = {k: v for k, v in params.items() if v is not None}
    params["apikey"] = api_key

    try:
        async with httpx2.AsyncClient(timeout=15.0) as client:
            resp = await client.get(f"{GNEWS_BASE_URL}/{endpoint}", params=params)
            resp.raise_for_status()
            data = resp.json()
    except httpx2.HTTPStatusError as e:
        # Do not echo the URL: it contains the API key.
        return f"GNews API error: HTTP {e.response.status_code}"
    except httpx2.HTTPError as e:
        return f"Network error contacting GNews: {type(e).__name__}"

    articles = data.get("articles", [])
    if not articles:
        return "No articles found."

    lines = []
    for i, a in enumerate(articles, 1):
        source = (a.get("source") or {}).get("name", "Unknown source")
        lines.append(
            f"{i}. {a.get('title', 'No title')}\n"
            f"   Source: {source} | Published: {a.get('publishedAt', 'n/a')}\n"
            f"   {a.get('description', '')}\n"
            f"   {a.get('url', '')}"
        )
    return "\n\n".join(lines)


@mcp.tool()
async def search_news(
    query: str,
    max_results: int = 5,
    lang: str = "en",
    country: str | None = None,
) -> str:
    """Search recent news articles by keyword.

    Args:
        query: Search keywords (e.g. "AWS outage", "electric vehicles").
        max_results: Number of articles to return (1-10).
        lang: Two-letter language code (e.g. "en", "es", "de").
        country: Optional two-letter country code (e.g. "us", "in", "gb").
    """
    return await _fetch(
        "search",
        {
            "q": query,
            "max": max(1, min(max_results, 10)),
            "lang": lang,
            "country": country,
        },
    )


@mcp.tool()
async def get_top_headlines(
    category: str = "general",
    max_results: int = 5,
    lang: str = "en",
    country: str = "us",
) -> str:
    """Get top news headlines.

    Args:
        category: One of general, world, nation, business, technology,
            entertainment, sports, science, health.
        max_results: Number of articles to return (1-10).
        lang: Two-letter language code (e.g. "en").
        country: Two-letter country code (e.g. "us", "in", "gb").
    """
    if category not in CATEGORIES:
        return f"Invalid category '{category}'. Choose from: {', '.join(sorted(CATEGORIES))}"
    return await _fetch(
        "top-headlines",
        {
            "category": category,
            "max": max(1, min(max_results, 10)),
            "lang": lang,
            "country": country,
        },
    )


if __name__ == "__main__":
    # stdio transport: never print to stdout, it would corrupt the protocol.
    print("Starting GNews MCP server (stdio)...", file=sys.stderr)
    mcp.run(transport="stdio")
