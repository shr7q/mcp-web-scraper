# Goal: Connect to MCP Server

import asyncio
from mcp.client.session import ClientSession
from mcp.client.stdio import stdio_client
from mcp import ClientSession, StdioServerParameters
import os
from dotenv import load_dotenv
from utils import get_response_from_llm


# Load environment variables from .env file
load_dotenv()

# Define server parameters to connect to the MCP server
server_params = StdioServerParameters(
    command="uv",                           # Use 'uv' to run the server
    args=["run", "mcp_server.py"],          #  Arguments to run the server script
    env=None,
    )


# Main async function to interact with the MCP server
async def main():
    """
       Launches an MCP client session that connects to the MCP server,
       lists available tools, queries documentation using 'get_docs',
       and generates a concise answer using an LLM.
       """

    async with stdio_client(server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()

            # Retrieve and display available tools from the MCP server
            tools_response = await session.list_tools()
            print("Available tools:", [t.name for t in tools_response.tools])

            # Define the user query and target documentation source
            query = "How to install and use uv library in Python?"
            library = "uv"

            res = await session.call_tool("get_docs", arguments = {"query":query, "library":library})

            # Prepare the prompt for the LLM using the retrieved documentation
            context = res.content
            user_prompt = f"Query: {query}, Context: {context}"

            # System prompt for the LLM to generate a final answer
            SYSTEM_PROMPT = """
            You are a helpful documentation assistant. Use the provided context primarily, 
            but if something is general or obvious (e.g., standard Python or LangChain usage), 
            you may infer based on your general knowledge. 
            Always cite sources from the context when available.
            """
            # Send the prompt to the LLM and get the final answer
            answer = get_response_from_llm(
                user_prompt = user_prompt,
                system_prompt= SYSTEM_PROMPT,
                model = "openai/gpt-oss-20b"
            )
            # Display the final answer
            print("Final Answer:", answer)

if __name__ == "__main__":
    asyncio.run(main())