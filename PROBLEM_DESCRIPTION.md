# GNews MCP Server — Learner Assignment
MCP (Model Context Protocol) Track | Total Marks: 100 | Duration: 3 Hours

> Confidential — Ultron Internal Training Material

---

## 1. Assignment Overview

In this assignment, you will build a GNews MCP Server that integrates with the GNews API to fetch real-time news headlines and search articles. You will implement MCP tools using Python, test them via MCP Inspector, and demonstrate working news retrieval.

By the end of this assignment, you will be able to:
- Understand the MCP (Model Context Protocol) architecture
- Build and register tools on an MCP server using FastMCP
- Integrate third-party REST APIs (GNews) into MCP tools
- Test MCP tools using the MCP Inspector
- Handle API keys securely using environment variables

---

## 2. Prerequisites

Before starting, ensure you have the following installed and configured:
- Python 3.10 or higher
- Node.js v18 or higher (for MCP Inspector)
- A free GNews API key — register at https://gnews.io
- A code editor (VS Code recommended)
- Basic understanding of Python async/await

---

## 3. Project Structure

```
gnews_mcp/
├── app/
│   ├── __init__.py
│   └── server.py          ← Main MCP server file
├── pyproject.toml         ← Dependencies
├── .env                   ← API key (do NOT commit to git)
└── README.md
```


---

## 4. Setup Instructions

### Step 1 — Create virtual environment
1. Open a terminal and navigate to your project folder
2. Run:
   ```bash
   python -m venv .venv
   ```
3. Activate it:
   - Windows:
     ```bash
     .venv\Scripts\activate
     ```
   - Mac/Linux:
     ```bash
     source .venv/bin/activate
     ```

### Step 2 — Install dependencies
```bash
pip install "mcp[cli]" httpx python-dotenv
```

### Step 3 — Configure API key
Create a `.env` file in the project root and add:
```bash
GNEWS_API_KEY="your_api_key_here"
```

### Step 4 — Run the MCP Inspector
```bash
npx @modelcontextprotocol/inspector python app/server.py
```
Open http://localhost:6274 in your browser to test your tools.


---

## 5. Tools to Implement

| Tool Name           | Parameters                                        | Description                                |
|---------------------|----------------------------------------------------|--------------------------------------------|
| `get_top_headlines` | `category`, `country`, `language`, `max_results`  | Fetch top headlines by category and region |
| `search_news`       | `query`, `language`, `max_results`, `sort_by`     | Search articles by keyword or phrase       |
| `get_news_by_topic` | `topic`, `language`, `max_results`                | Get news for a specific topic              |

All tools must:
- Load the API key from environment variables using `python-dotenv`
- Return a formatted string with article title, source, date, URL, and summary
- Handle errors gracefully (missing API key, API failures, no results)
- Use Python type hints for all parameters


---

## 6. Assignment Tasks

### Summary

| Task | Description                                                     | Marks | Difficulty |
|-----:|-----------------------------------------------------------------|------:|:----------:|
| 1    | Set up the GNews MCP server and connect to MCP Inspector        | 10    | Easy       |
| 2    | Implement `get_top_headlines` and test with 3 categories        | 20    | Easy       |
| 3    | Implement `search_news` with keyword filtering                  | 20    | Medium     |
| 4    | Implement `get_news_by_topic` with at least 3 topics            | 20    | Medium     |
| 5    | Add new tool: `get_news_by_date_range` with `from/to` params    | 30    | Hard       |

### Task 1 — Setup (10 marks)
- Create the project structure as shown in Section 3
- Install all required dependencies
- Create `.env` with your GNews API key
- Run the MCP Inspector and show a screenshot of it connecting successfully

### Task 2 — `get_top_headlines` (20 marks)
- Implement the `get_top_headlines` tool in `app/server.py`
- Test with the following categories: `technology`, `sports`, `business`
- Output must include: title, source, published date, URL, and description
- Take screenshots of each test from MCP Inspector

### Task 3 — `search_news` (20 marks)
- Implement the `search_news` tool
- Test with at least 3 different search keywords
- Demonstrate `sort_by` working with both `publishedAt` and `relevance`
- Include screenshots in your submission

### Task 4 — `get_news_by_topic` (20 marks)
- Implement the `get_news_by_topic` tool
- Test with at least 3 topics: `breaking-news`, `science`, `health`
- Show that unsupported topics return a meaningful error message

### Task 5 — New Tool: `get_news_by_date_range` (30 marks)
Build a new tool not in the starter code:
- Tool name: `get_news_by_date_range`
- Parameters: `query` (str), `from_date` (str, format `YYYY-MM-DD`), `to_date` (str, format `YYYY-MM-DD`), `max_results` (int)
- Use the GNews search endpoint with `from` and `to` query parameters
- Validate that `from_date` is before `to_date` — return an error if not
- Return formatted results or a clear message if no articles found

Hint: GNews API supports date filtering via:
```python
params = { 'q': query, 'from': from_date, 'to': to_date, ... }
```


---

## 7. Submission Guidelines

Submit the following as a ZIP file named `GNews_MCP_<YourName>.zip`:
- Complete source code (`app/server.py` and supporting files)
- A short README explaining how to run your server
- Do NOT include your `.env` file or API key in the submission

Submission deadline and upload instructions will be shared by your instructor.

---

## 8. Evaluation Criteria

| Criteria                                          | Weight | Notes                         |
|---------------------------------------------------|------:|-------------------------------|
| Correctness — tools return expected output        | 50%   | Verified via screenshots      |
| Code quality — clean, readable, well-commented    | 20%   | PEP8 compliance               |
| Error handling — graceful failures                | 15%   | Missing key, bad input        |
| Documentation — README and inline comments        | 15%   |                               |


---

## 9. Tips & Resources

- GNews API Docs: https://gnews.io/docs/v4
- FastMCP Docs: https://github.com/jlowin/fastmcp
- MCP Inspector: `npx @modelcontextprotocol/inspector`
- Use `async def` for all tool functions since `httpx` is async
- Test edge cases: invalid country codes, empty results, long queries

Important: Never hardcode your API key in source code. Always use environment variables. Submissions found with hardcoded API keys will be penalised.

---