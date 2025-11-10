# AI-Powered Web Documentation Scraper (MCP Server)

This project implements an **AI-Powered web scraping and documentation assistant**, built as an **MCP (Model Context Protocol)** tool.  
It can **search the web for relevant documentation**, **fetch and clean content using LLMs**, and **serve responses through a FastMCP server**, making it accessible via any compatible MCP client.

## Overview

The **MCP Web Scraper** serves as a bridge between live web documentation and LLM-based understanding.  
It uses:
- **Serper.dev API** for intelligent Google search queries  
- **Async web scraping** via `httpx`  
- **Groq LLMs** for content extraction and summarization  
- **FastMCP** for standard MCP server-client communication  
- **Claude desktop** for deploying MCP server locally
- **Debugging** via  `npx @modelcontextprotocol/inspector`  
---

## FEATURES:

- **Smart Web Search** using the [Serper.dev](https://serper.dev/) API.  
- **Automatic Content Cleaning** via LLM (Groq API).  
- **Dynamic Documentation Querying** for:
  - LangChain  
  - LlamaIndex  
  - OpenAI API  
  - UV Package Manager  
- **FastMCP Server Integration** for easy connection via `stdio`.  
- **LLM-based Summarization** of fetched documentation.

---

## INSTALLATION AND SETUP
### 1. INSTALL DEPENDENCIES:

      uv pip install -r requirements.txt

### 2. Add Environment Variables
Create a .env file in the project root:

      SERPER_API_KEY=your_serper_api_key
      GROQ_API_KEY=your_groq_api_key

You can get:
- Serper API Key → https://serper.dev
- Groq API Key → https://console.groq.com

---

## PROJECT STRUCTURE:

MCP-WebScraper:
```
|
├── mcp_server.py # Runs the MCP server (FastMCP tool)
├── client.py # Connects to the MCP server, queries docs, and summarizes results
├── utils.py # Utility functions (HTML cleaning and LLM API wrapper)
├── .env # Environment variables (API keys)
└── README.md # Project documentation
```
--- 

## HOW IT WORKS: 
### **Step 1: MCP Server (mcp_server.py)**
- Initializes a FastMCP server named "docs".
- Implements the get_docs(query, library) MCP tool:
  - Uses Serper.dev to search for documentation pages.
  - Fetches URLs asynchronously using httpx.
  - Passes HTML content through Groq LLM for cleaning and summarization.
  - Returns cleaned documentation text with source links.
  

### **Step 2: Client (client.py)**
- Connects to the MCP server via stdio.
- Lists available tools and invokes get_docs.
- Uses Groq LLM to summarize fetched documentation for user-friendly answers.

      Example query (default in client.py):
      query = "How to install and use uv library in Python?"
      library = "uv"


### **Step 3: Utils (utils.py)**
- Contains helper functions:
  - clean_html_to_text() → Cleans raw HTML using trafilatura
  - get_response_from_llm() → Sends prompts to Groq API for summarization
 
--- 

## RUNNING THE PROJECT**

**Step 1: Start the MCP Server**
You can start the server using either command:

      uv run mcp_server.py

**Step 2: Run the Client**
In another terminal window:

      uv run client.py

---

## SUPPORTED LIBRARIES:
To add more documentation sources, update docs_urls in mcp_server.py:
```
docs_urls = {
    "langchain": "python.langchain.com/docs",
    "llama-index": "docs.llamaindex.ai/en/stable",
    "openai": "platform.openai.com/docs",
    "uv": "docs.astral.sh/uv"
}
```

## Running the MCP Server on Cloud Desktop
After successful local testing, the MCP server was deployed on a cloud desktop environment for continuous availability and integration.
A JSON configuration file was created under the name claude_desktop_config.json to define the MCP server’s launch command, working directory, and environment variables.
### Create the Configuration File

Create a file named **`mcp_config.json`** (or similar) in your project directory.  
This JSON configuration defines how the Cloud Desktop environment should launch your MCP server, including paths, environment variables, and dependencies.

Below is an example configuration:

```json
{
  "mcpServers": {
    "docs-mcp": {
      "command": "Path to your Python executable",
      "args": [
        "Path to your mcp_server.py file"
      ],
      "cwd": " Path to your working directory",
      "env": {
        "SERPER_API_KEY": "your serper api",
        "GROQ_API_KEY": "your groq api"
      }
    }
  }
}
```
