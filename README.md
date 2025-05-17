# MCP-Based Local File Agent

A local file management agent built with LangChain, LangGraph, and Model Context Protocol (MCP) that can perform operations on your local PC like creating folders, organizing files, and locating content.

## Features

- Create, copy, move, and delete files and folders
- List contents of directories
- Locate files by pattern matching
- Get file/directory information
- Organize files by extension
- Natural language interface using GPT models
- **NEW**: Smart path resolution for system locations (Desktop, Documents, etc.)

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

### File Agent

Run the file agent:

```
python file_agent.py
```

The agent will automatically detect system paths like Desktop, Documents, Downloads, etc.

## System Path Shortcuts

The agent now supports system path shortcuts that map to actual locations on your computer:

- `desktop` → Your Desktop folder
- `documents` → Your Documents folder
- `downloads` → Your Downloads folder
- `pictures` → Your Pictures folder
- `music` → Your Music folder
- `videos` → Your Videos folder
- `home` → Your user home directory

For Windows users with OneDrive, the agent automatically detects and uses the OneDrive locations.

You can reference these locations in natural language:
- "Create a folder on my desktop called Projects"
- "List all files in my documents folder"
- "Move report.docx from desktop to documents/Work"

## Example Commands

Once the agent is running, you can ask it to perform various file operations:

- "Create a new folder called 'Projects' on my desktop"
- "List all files in my documents folder"
- "Find all Python files in my downloads folder"
- "Move resume.pdf from desktop to documents/Job Applications"
- "Organize files in my downloads folder by extension"
- "Show me the available system locations"

## How It Works

1. The `file_server.py` creates an MCP server with file operation tools
2. The agent connects to this server using the langchain-mcp-adapters library
3. When you reference a system location (like "desktop"), the path resolver converts it to the actual system path
4. User requests are processed by a GPT model that decides which tools to use
5. The agent executes the chosen tools and returns the results

## Implementation Details

The smart path resolution works by:
1. Detecting common locations in path strings ("desktop/folder" → "C:/Users/username/Desktop/folder")
2. Automatically handling OneDrive redirection on Windows systems
3. Maintaining backward compatibility with absolute and relative paths

## Customization

You can modify `file_server.py` to add more file operation tools or customize the path resolution logic as needed. 