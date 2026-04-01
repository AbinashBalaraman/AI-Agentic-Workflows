# AI-Agentic-Workflows

A collection of autonomous AI agent systems built using Google ADK, LangChain, and LangGraph. Each module demonstrates a distinct pattern of multi-agent orchestration, tool integration, or external API automation across productivity, financial data, and database management domains.

## Overview

This repository moves beyond basic LLM chat interfaces toward production-grade agentic systems. Projects here implement agent-to-agent delegation, live tool calling against external APIs (Microsoft 365, Yahoo Finance, Google Finance, Redis, MongoDB), and multi-model orchestration across Gemini 2.0 Flash and GPT-4o. The common engineering thread is that every module requires the LLM to plan, validate, and execute multi-step operations autonomously without hardcoded logic paths.

## Modules

### `multi_tool_agent/`

This directory contains two generations of multi-tool agent implementations, both built on Google's Agent Development Kit (ADK).

**`multi_tool_agent/agent.py`** — A minimal ADK starter agent using `gemini-2.0-flash` with `get_weather` and `get_current_time` tools. Demonstrates the core ADK `Agent` class and tool registration pattern.

**`multi_tool_agent/ADK_Multi_Agent/`** — The flagship production implementation. A hierarchical multi-agent orchestration system where a central `MasterAgent` delegates tasks to three specialized sub-agents in real time.

*   **MasterAgent** (`gemini-2.0-flash`): The central coordinator. Receives the user request, determines which sub-agent(s) are needed, confirms the operation plan, and provides detailed step-by-step reporting throughout execution.
*   **Redis\_agent** (`gpt-4o`): A database management agent that connects to both Redis (hosted on AWS EC2 via Redis Cloud) and a local MongoDB instance through the Model Context Protocol. Handles SET, GET, and DEL operations on Redis keys alongside full MongoDB CRUD. Enforces strict data validation before any database write.
*   **calander\_Agent** (`gemini-2.0-flash`): A Microsoft 365 automation agent. Wraps the full `O365Toolkit` via LangChain and exposes calendar blocking, event search, mail search, draft creation, event invitations, and outbound message sending. Handles IST-to-UTC timezone conversion automatically. Authenticated via a persistent O365 OAuth2 token file.
*   **yfinance\_agent** (`gpt-4o`): A financial data retrieval agent. Exposes `fetch_stock_attribute` and `search_stock` as tools, allowing the LLM to query any `yfinance.Ticker` attribute by name — including `financials`, `recommendations`, `earnings_dates`, `options`, `news`, and more.

### `YahooFinance_LLM_Agents/`

A standalone LangGraph ReAct agent for interactive stock market research. Uses `gpt-4.1-mini` via OpenAI as the reasoning model and exposes 20+ discrete `yfinance` tool functions covering every major ticker attribute: balance sheets, cashflow statements, quarterly financials, analyst price targets, institutional holders, ISIN, options, and live news. Maintains a persistent `chat_history` list across turns for conversational continuity. Includes a `test_yfinance.py` for validating individual tool outputs.

### `GoogleFinance/`

A LangGraph ReAct agent using `gemini-2.0-flash` as the reasoning model. Integrates `GoogleFinanceQueryRun` (via SerpAPI) and `google-scholar` tools from the LangChain community toolkit to perform comparative stock analysis against Google Finance data. Demonstrates how to wrap community tools into a ReAct agent with streaming output.

### `Langchain_google_calender/`

A standalone, conversational LangGraph ReAct agent for Microsoft 365 calendar operations. Uses `gemini-2.5-flash` as the reasoning model with the full `O365Toolkit`. Maintains a running `conversation_history` list to support follow-up queries and corrections within a session. Manages IST-to-UTC time offsetting in the system prompt. This module is the standalone prototype from which the ADK `calander_Agent` was later derived.

### `ClaudeClient/`

A FastMCP server (stdio transport) exposing MongoDB CRUD operations and Tavily web search as MCP tools. Uses `pymongo` to connect to a local MongoDB instance (`car` database, `car_data` collection). Tools include `collection_operations` (supporting `find`, `insert`, `update`, `delete`, `count`, `distinct`), `tavily` (Tavily REST API search), and a resource endpoint exposing application runtime status. This server is the MCP backend consumed by the `Redis_agent` in `ADK_Multi_Agent`.

## Technology Stack

*   **Language:** Python 3.10+
*   **Agent Frameworks:** Google ADK (`google-adk`), LangGraph, LangChain
*   **LLM Providers:** Google Gemini 2.0 Flash / 2.5 Flash, OpenAI GPT-4o / GPT-4.1-mini
*   **External APIs:** Microsoft 365 (O365 OAuth2), Yahoo Finance (`yfinance`), Google Finance (SerpAPI), Tavily Search
*   **Databases:** MongoDB (`pymongo`, local), Redis (Redis Cloud on AWS EC2)
*   **Protocols:** Model Context Protocol (FastMCP, stdio transport)
*   **Libraries:** `langchain-community`, `langgraph`, `O365`, `python-dotenv`, `google-genai`, `mcp`

## Prerequisites

1.  Python 3.10 or higher.
2.  A `.env` file in each module root containing the relevant keys:
    ```env
    GOOGLE_API_KEY="..."
    OPENAI_API_KEY="..."
    SERP_API_KEY="..."
    ANTHROPIC_API_KEY="..."
    ```
3.  A valid Microsoft 365 account with an `o365_token.txt` OAuth token generated via `account.authenticate()` on first run.
4.  A running local MongoDB instance (for `ClaudeClient` and `MongodbMCP` interactions).
5.  Redis Cloud credentials configured in the `ADK_Multi_Agent/Redis/agent.py` environment block.

## Setup and Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/AbinashBalaraman/AI-Agentic-Workflows.git
    cd AI-Agentic-Workflows
    ```

2.  Initialize a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  Install dependencies for the target module (each module has its own `pyproject.toml` or `requirements.txt`):
    ```bash
    pip install -r multi_tool_agent/requirement.txt
    ```

4.  Configure environment variables in a `.env` file at the module root.

## Usage

To run the ADK multi-agent system:

```bash
cd multi_tool_agent
adk web
```

To run the standalone Yahoo Finance LangGraph agent:

```bash
cd YahooFinance_LLM_Agents
python main.py
```

To run the Microsoft 365 calendar agent directly:

```bash
cd Langchain_google_calender
python main.py
```

## Security

All credential files (`credentials.json`, `token.json`, `o365_token.txt`) and environment variable files (`.env`) are excluded from version control via `.gitignore`. Never commit OAuth tokens or API keys to the repository.

## License

Standard MIT License applies.
