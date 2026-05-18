# from __future__ import annotations

import os
# import asyncio
from typing import Any, Dict, List, Optional, Tuple
from datetime import datetime

import httpx
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

# Load environment variables from .env (if present)
load_dotenv()

API_BASE = "https://gnews.io/api/v4"
API_KEY_ENV = "GNEWS_API_KEY"

# Create the MCP app
app = FastMCP("gnews-mcp-server")


def _require_api_key() -> str:
    api_key = os.getenv(API_KEY_ENV, "").strip()
    if not api_key:
        raise RuntimeError(
            f"Missing API key. Set {API_KEY_ENV} in your environment (e.g., .env)."
        )
    return api_key


def _validate_max_results(max_results: int) -> int:
    # GNews max is documented up to 100, default 10. Clamp to [1,100].
    if max_results < 1:
        return 1
    if max_results > 100:
        return 100
    return max_results


def _format_articles(articles: List[Dict[str, Any]]) -> str:
    if not articles:
        return "No articles found."
    lines: List[str] = []
    for i, a in enumerate(articles, start=1):
        title = a.get("title") or "Untitled"
        url = a.get("url") or ""
        published_at = a.get("publishedAt") or ""
        # GNews returns ISO strings; show date and time in UTC
        try:
            dt = datetime.fromisoformat(published_at.replace("Z", "+00:00"))
            published_fmt = dt.strftime("%Y-%m-%d %H:%M UTC")
        except Exception:
            published_fmt = published_at or "Unknown"
        source = (a.get("source") or {}).get("name") or "Unknown"
        description = a.get("description") or ""
        lines.append(
            f"{i}. {title}\n"
            f"   Source: {source}\n"
            f"   Published: {published_fmt}\n"
            f"   URL: {url}\n"
            f"   Summary: {description}\n"
        )
    return "\n".join(lines)


async def _get_json(path: str, params: Dict[str, Any]) -> Dict[str, Any]:
    # Add API key to params
    params = {**params, "apikey": _require_api_key()}
    url = f"{API_BASE.rstrip('/')}/{path.lstrip('/')}"
    async with httpx.AsyncClient(timeout=20.0) as client:
        resp = await client.get(url, params=params)
        resp.raise_for_status()
        return resp.json()


def _error_message(prefix: str, err: Exception) -> str:
    return f"{prefix}: {err}"


@app.tool()
async def get_top_headlines(
    category: str,
    max_results: int,
    country: Optional[str] = None,
    language: Optional[str] = None,
) -> str:
    """
    Fetch top headlines by category and region.

    Parameters:
    - category: Category string (e.g., technology, sports, business)
    - country: Optional 2-letter country code (e.g., 'us', 'gb')
    - language: Optional 2-letter language code (e.g., 'en')
    - max_results: Maximum number of results to return (1-100)

    Returns:
    - A formatted string with title, source, date, URL, and summary.
    """
    try:
        max_results = _validate_max_results(max_results)
        params: Dict[str, Any] = {
            "category": category,
            "max": max_results,
        }
        if country:
            params["country"] = country
        if language:
            params["lang"] = language

        data = await _get_json("top-headlines", params)
        articles = data.get("articles", [])
        if not articles:
            return "No articles found for the given filters."
        return _format_articles(articles)
    except httpx.HTTPStatusError as e:
        return _error_message("GNews API error (top-headlines)", e)
    except Exception as e:
        return _error_message("Failed to fetch top headlines", e)


@app.tool()
async def search_news(
    query: str,
    max_results: int,
    sort_by: str,
    language: Optional[str] = None,
) -> str:
    """
    Search articles by keyword or phrase.

    Parameters:
    - query: Search string
    - language: Optional 2-letter language code (e.g., 'en')
    - max_results: Maximum number of results to return (1-100)
    - sort_by: 'publishedAt' or 'relevance'

    Returns:
    - A formatted string with title, source, date, URL, and summary.
    """
    try:
        max_results = _validate_max_results(max_results)
        sort_by = (sort_by or "publishedAt").strip()
        if sort_by not in {"publishedAt", "relevance"}:
            return "Invalid sort_by. Use 'publishedAt' or 'relevance'."

        params: Dict[str, Any] = {
            "q": query,
            "max": max_results,
            "sortby": sort_by,
        }
        if language:
            params["lang"] = language

        data = await _get_json("search", params)
        articles = data.get("articles", [])
        if not articles:
            return "No articles found for the given query."
        return _format_articles(articles)
    except httpx.HTTPStatusError as e:
        return _error_message("GNews API error (search)", e)
    except Exception as e:
        return _error_message("Failed to search news", e)


SUPPORTED_TOPICS = {
    "breaking-news",
    "world",
    "nation",
    "business",
    "technology",
    "entertainment",
    "sports",
    "science",
    "health",
}


@app.tool()
async def get_news_by_topic(
    topic: str,
    max_results: int,
    language: Optional[str] = None,
) -> str:
    """
    Get news for a specific topic.

    Parameters:
    - topic: One of: breaking-news, world, nation, business, technology, entertainment,
             sports, science, health
    - language: Optional 2-letter language code (e.g., 'en')
    - max_results: Maximum number of results to return (1-100)

    Returns:
    - A formatted string with title, source, date, URL, and summary.
    """
    try:
        max_results = _validate_max_results(max_results)
        topic_norm = (topic or "").strip().lower()
        if topic_norm not in SUPPORTED_TOPICS:
            topics = ", ".join(sorted(SUPPORTED_TOPICS))
            return f"Unsupported topic '{topic}'. Supported topics: {topics}."
        params: Dict[str, Any] = {
            "topic": topic_norm,
            "max": max_results,
        }
        if language:
            params["lang"] = language

        data = await _get_json("top-headlines", params)
        articles = data.get("articles", [])
        if not articles:
            return "No articles found for the given topic."
        return _format_articles(articles)
    except httpx.HTTPStatusError as e:
        return _error_message("GNews API error (topic)", e)
    except Exception as e:
        return _error_message("Failed to fetch topic news", e)


@app.tool()
async def get_news_by_date_range(
    query: str,
    from_date: str,
    to_date: str,
    max_results: int,
) -> str:
    """
    Search news within a date range.

    Parameters:
    - query: Search string
    - from_date: Start date (YYYY-MM-DD)
    - to_date: End date (YYYY-MM-DD)
    - max_results: Maximum number of results to return (1-100)

    Returns:
    - A formatted string with title, source, date, URL, and summary, or a clear message if none found.
    """
    try:
        # Validate dates
        try:
            start = datetime.strptime(from_date, "%Y-%m-%d")
            end = datetime.strptime(to_date, "%Y-%m-%d")
        except ValueError:
            return "Invalid date format. Use YYYY-MM-DD."
        if start > end:
            return "from_date must be earlier than or equal to to_date."

        max_results = _validate_max_results(max_results)

        params: Dict[str, Any] = {
            "q": query,
            "from": from_date,
            "to": to_date,
            "max": max_results,
            "sortby": "publishedAt",
        }

        data = await _get_json("search", params)
        articles = data.get("articles", [])
        if not articles:
            return "No articles found for the given date range."
        return _format_articles(articles)
    except httpx.HTTPStatusError as e:
        return _error_message("GNews API error (date range)", e)
    except Exception as e:
        return _error_message("Failed to fetch news by date range", e)


if __name__ == "__main__":
    # Run the MCP server
    app.run()
