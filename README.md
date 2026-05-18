# GNews MCP Server

MCP Track assignment implementation exposing tools for GNews:
- get_top_headlines
- search_news
- get_news_by_topic
- get_news_by_date_range

## Prerequisites
- Python 3.10+
- Node.js v18+
- GNews API key (https://gnews.io) — store in .env

## Setup
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install "mcp[cli]" httpx python-dotenv fastmcp
```

Alternatively, using pyproject:
```bash
pip install -e .
```

## Configure API key
Create `.env` in the project root:
```
GNEWS_API_KEY=your_api_key_here
```

## Run with MCP Inspector
From project root:
```bash
npx @modelcontextprotocol/inspector python app/server.py
```
Open http://localhost:6274 to test tools.

## Tools
- get_top_headlines(category, country, language, max_results)
- search_news(query, language, max_results, sort_by)  # sort_by: publishedAt|relevance
- get_news_by_topic(topic, language, max_results)     # validates topic
- get_news_by_date_range(query, from_date, to_date, max_results)  # YYYY-MM-DD

All return formatted strings with: title, source, published date, URL, and summary.

## Notes
- Do not commit your .env or API key.
- Handles: missing key, API failures, no results, invalid inputs.
- Uses async httpx, FastMCP, python-dotenv.
