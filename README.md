# MCP-Based Local File Agent

A local file management agent built with LangChain, LangGraph, and Model Context Protocol (MCP) that can perform operations on your local PC like creating folders, organizing files, and locating content.

## Features

- Create, copy, move, and delete files and folders
- List contents of directories
- Locate files by pattern matching
- Get file/directory information
- Organize files by extension
- Natural language interface using GPT models

## Setup

1. Clone this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Set up your OpenAI API key:
   - Copy `env.example` to `.env`
   - Replace `your_openai_api_key_here` with your actual OpenAI API key

## Usage

### Basic File Agent (stdio transport)

Run the basic file agent that uses stdio transport:

```
python file_agent.py
```

### Advanced File Agent (with LangGraph StateGraph)

Run the advanced agent with better workflow handling:

```
python advanced_file_agent.py
```

### HTTP Server and Client (recommended for production)

1. First, start the HTTP server:
   ```
   python file_server_http.py --port 3000
   ```

2. Then, in a separate terminal, start the client:
   ```
   python http_file_agent.py --port 3000
   ```

The HTTP version is more robust for production use and allows the server to run independently from the client.

## Example Commands

Once the agent is running, you can ask it to perform various file operations:

- "Create a new folder called 'Documents' in the current directory"
- "List all files in the current directory"
- "Find all Python files in the project"
- "Move file.txt from Downloads to Documents"
- "Organize files in the Downloads folder by extension"
- "What's my current directory?"

## How It Works

1. The `file_server.py` or `file_server_http.py` creates an MCP server with file operation tools
2. The agent connects to this server using the langchain-mcp-adapters library
3. User requests are processed by a GPT model that decides which tools to use
4. The agent executes the chosen tools and returns the results

## Transport Options

This project demonstrates two MCP transport options:

1. **stdio**: Simple transport where the client spawns the server process directly
2. **streamable-http**: HTTP-based transport where the server runs independently

The HTTP option is recommended for production as it's more stable and allows the server to run independently of the client.

## Customization

You can modify `file_server.py` or `file_server_http.py` to add more file operation tools as needed. 