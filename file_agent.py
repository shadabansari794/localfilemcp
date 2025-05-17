import os
import asyncio
from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI

# Load environment variables
load_dotenv()

# Make sure you have set OPENAI_API_KEY in your environment or .env file
if not os.getenv("OPENAI_API_KEY"):
    print("WARNING: OPENAI_API_KEY environment variable not set. You should set it in .env file or environment.")
    print("Continuing anyway for testing purposes...")

async def main():
    print("Initializing MCP client...")
    # Initialize the MCP client to connect to our file server
    try:
        client = MultiServerMCPClient(
            {
                "filesystem": {
                    "command": "python",
                    "args": ["file_server.py"],
                    "transport": "stdio",
                }
            }
        )
        
        print("Getting tools from MCP server...")
        # Get all tools from the MCP server
        tools = await client.get_tools()
        print(f"Found {len(tools)} tools: {[tool.name for tool in tools]}")
        
        # Use a dummy key for testing if not provided
        api_key = os.getenv("OPENAI_API_KEY", "dummy_key_for_testing")
        
        print("Initializing LLM...")
        # Initialize the LLM
        llm = ChatOpenAI(
            api_key=api_key,
            model="gpt-4o",  # or another model you prefer
            temperature=0,
        )
        
        print("Creating agent...")
        # Create the agent using LangGraph's create_react_agent
        agent = create_react_agent(llm, tools)
        
        print("\nFile Agent initialized! You can now ask about file operations.")
        print("You can use shortcuts like 'desktop', 'documents', etc. to refer to system locations.")
        print("For example: 'create a folder on my desktop called test' or 'list files in my documents folder'")
        print("Type 'exit' to quit.")
        
        while True:
            # Get user input
            user_input = input("\nYou: ")
            
            if user_input.lower() == 'exit':
                print("Exiting the file agent.")
                break
            
            try:
                # Use the agent to respond to the user's request
                print("Sending request to agent...")
                response = await agent.ainvoke({"messages": [{"role": "user", "content": user_input}]})
                
                # Print the agent's response
                print("\nFile Agent:", response["messages"][-1].content)
                
            except Exception as e:
                print(f"Error: {str(e)}")
                import traceback
                traceback.print_exc()
    
    except Exception as e:
        print(f"Initialization error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main()) 