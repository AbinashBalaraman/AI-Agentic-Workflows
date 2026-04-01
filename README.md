# AI-Agentic-Workflows

A comprehensive suite of autonomous AI agents built using LangChain, designed to interact with external APIs, execute multi-tool sequencing, and orchestrate complex autonomous tasks.

## Overview

This repository demonstrates the practical application of Large Language Models (LLMs) via the LangChain framework. The included agents are designed to execute complex, multi-step operations autonomously by securely interacting with third-party systems such as Google Calendar, the Anthropic Claude API, and other integrated endpoints. The core objective of these implementations is to move beyond simple LLM chattiness toward deterministic, action-oriented agentic workflows.

## Core Implementations

This workspace is divided into specific agent modules, each demonstrating distinct autonomous behaviors and API integrations.

*   `Langchain_google_calender/` and `Calendar_event/`
    *   **Functionality:** Interfaces securely with the Google Calendar API.
    *   **Capabilities:** Allows an LLM agent to fetch upcoming events, clear schedules, and dynamically book new appointments based on natural language prompts.
*   `ClaudeClient/`
    *   **Functionality:** A wrapper designed for seamless interaction with the Anthropic Claude API.
    *   **Capabilities:** Provides an environment for integrating Claude's reasoning capabilities into broader autonomous scripts.
*   `multi_tool_agent/`
    *   **Functionality:** An advanced LangChain agent configured with a dynamic tool-routing system.
    *   **Capabilities:** Demonstrates the LLM's ability to evaluate a complex prompt, select the appropriate external tools from a provided list, and execute those tools in sequence to reach a verified conclusion.

## Technology Stack

*   **Language:** Python 3.10+
*   **Orchestration:** LangChain
*   **LLM Providers:** Anthropic (Claude REST API), Google (Gemini / Vertex AI implementations depending on module)
*   **External APIs:** Google Calendar API (OAuth 2.0 / Service Accounts)
*   **Libraries:** `google-api-python-client`, `anthropic`, `python-dotenv`

## Prerequisites

To run these modules locally, ensure you have the following configured in your environment:

1.  Python 3.10 or higher installed.
2.  A valid Anthropic API Key (`ANTHROPIC_API_KEY`).
3.  Active Google Cloud Platform (GCP) Credentials (`credentials.json` / `token.json` generated via GCP service accounts or OAuth tokens) with access to the Calendar API.

## Setup and Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/AbinashBalaraman/AI-Agentic-Workflows.git
    cd AI-Agentic-Workflows
    ```

2.  Initialize and activate a virtual environment (recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
    *(Note: If a global `requirements.txt` is not provided, refer to the individual module directories for specific dependencies).*

4.  Environment Configuration:
    Create a `.env` file in the root of the targeted module and populate it with your required keys:
    ```env
    ANTHROPIC_API_KEY="your_anthropic_key_here"
    GOOGLE_APPLICATION_CREDENTIALS="path/to/your/gcp/credentials.json"
    ```

## Usage

Navigate to the respective module directory to execute the agent scripts. For example, to run the multi-tool agent:

```bash
cd multi_tool_agent
python main.py
```

## Contributing

This repository serves as a portfolio showcase of autonomous agent engineering. While it is not actively seeking open-source contributions, you may open an issue if you encounter configuration bugs or security discrepancies.

## License

Standard MIT License applies.
