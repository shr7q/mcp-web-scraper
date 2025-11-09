# Goal is to create an AI-Powered webscraping tool that:
# 1. Searches the web for relevant documentation
# 2. Fetches and cleans the content from the documentation
# 3. Serves as an MCP tool accessible via FastMCP

import json
import os
import httpx
import asyncio
from dotenv import load_dotenv
from utils import clean_html_to_text, get_response_from_llm
from fastmcp import FastMCP

# Load environment variables
load_dotenv()

# Initialize FastMCP
mcp = FastMCP("docs")

# Serper.dev API endpoint which is used for web search
SERPER_URL = "https://google.serper.dev/search"

# Step 1: Search the web using SERPER API
async def search_web(query:str) -> dict | None:
    payload = json.dumps({  "q": query, "num": 2 })
    headers = {
      'X-API-KEY': os.getenv("SERPER_API_KEY"),
      'Content-Type': 'application/json'
    }
    # Send POST request to SERPER API
    async with httpx.AsyncClient() as client:
        response = await client.post(
            SERPER_URL, headers = headers, data=payload, timeout = 30.0
        )
        response.raise_for_status()
        return response.json()

# Step 2: Fetch webpage content and clean it using an LLM
async def fetch_url(url:str):

    # Initialize async HTTP client
    async with httpx.AsyncClient() as client:

        # Perform get request to fetch webpage
        response = await client.get(url, timeout = 30.0)

        # System prompt for LLM to clean HTML content
        system_prompt = (
            """You are a web scraping assistant. 
            Extract the main content from the HTML page, removing any ads, navigation, or irrelevant sections.
             Return only the cleaned text content."""
        )
        # Handle large responses by chunking
        chunk_size = 8000
        text_chunk =[response.text[i:i+chunk_size] for i in range(0, len(response.text), chunk_size)]
        # Process each chunk with the LLM
        cleaned_parts = []
        for chunk in text_chunk:
            cleaned_chunk = get_response_from_llm(
            user_prompt = chunk,
            system_prompt = system_prompt,
            model = "openai/gpt-oss-20b"
            )
            cleaned_parts.append(cleaned_chunk)
        # Combine cleaned parts into a single response
        cleaned_response = "".join(cleaned_parts)
        return cleaned_response


# Step 3: Define supported documentation URLs
docs_urls = {
    "langchain": "python.langchain.com/docs",
    "llama-index": "docs.llamaindex.ai/en/stable",
    "openai": "platform.openai.com/docs",
    "uv": "docs.astral.sh/uv",
}

# Step 4: Define MCP tool to get documentation
@mcp.tool()
async def get_docs(query:str, library:str):
    """
    Search the latest docs for a given query and library.
    Supports langchain, openai, llama-index and uv.

    Args:
        query: The query to search for (e.g. "Publish a package with UV")
        library: The library to search in (e.g. "uv")

    Returns:
        Summarized text from the docs with source links.
    """
    # Validate input library
    if library not in docs_urls:
        raise ValueError(f"Library {library} not supported")

    # Construct site-specific search query
    query = f"site:{docs_urls[library]} {query}"
    results = await search_web(query)

    if len(results["organic"]) == 0:
        return "No results found"

    text_parts = []

    # Loop through search results and fetch content
    for result in results["organic"]:
        link = result.get("link", "")
        raw = await fetch_url(link)

        if raw:
            labeled = f"Source: {link}\n{raw}"
            text_parts.append(labeled)
    return "\n\n".join(text_parts)

# Main function to run the MCP server
def main():
    mcp.run(transport ="stdio")

if __name__ == "__main__":
    main()