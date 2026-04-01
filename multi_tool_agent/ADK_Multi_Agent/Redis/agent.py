import os
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters
from dotenv import load_dotenv
load_dotenv()

Redis=MCPToolset(
        connection_params=StdioServerParameters(
        command=os.getenv("UV_PATH", "uv"),
        args= [
       "--directory",
        os.getenv("REDIS_MCP_DIR", "path/to/mcp-redis"),
        "run",
        "src/main.py"
        
      ],env= {
        "REDIS_HOST": os.getenv("REDIS_HOST", ""),
        "REDIS_PORT": os.getenv("REDIS_PORT", ""),
        "REDIS_USERNAME": os.getenv("REDIS_USERNAME", "default"),
        "REDIS_PWD": os.getenv("REDIS_PWD", "")
      }))
Mongo=MCPToolset(
    connection_params=StdioServerParameters(
      command= "python",
      args=[
        os.getenv("MONGO_MCP_PATH", "path/to/ClaudeClient/main.py")
      ]
    
        
    )
)

root_agent= Agent(name="Redis_agent",model=LiteLlm("openai/gpt-4o"),
instruction="""
-dont directly call tools, first analyse the instruction or data and decide how and which tool to call and complete task without error
-if the given data is in wrond datatype or format convert it to right format if you can't convert the data or invalid data is given tell the user about correct format to be given.
ROLE: Database Management Agent - Handle Redis and MongoDB operations.

KEY RULES:
1. DATA VALIDATION: Always validate data formats and required parameters before database operations.
2. OPERATION PRIORITY: Confirm connection details, database names, and query formats before execution.
3. PRE-TOOL VALIDATION: Verify database connectivity and required data structure before calling any tool.
4. DATA FOCUS: Extract maximum operational details, provide clear success/failure status and data results.
6. ERROR HANDLING: Provide detailed error descriptions and suggest corrections for failed operations.
Your responses must be comprehensive reports containing operation status, data results, and clear handoff statements.
WORKFLOW: Receive database request → Validate connection/data → Confirm tool requirements → Execute database operations → Structure results
""",
description="""Database management agent for Mongodb and Redis 
SUPPORTED OPERATIONS:
- Redis: SET/GET/DEL operations, key management, data retrieval
- MongoDB: CRUD operations, collection management, document queries, aggregations
- Connection management and status monitoring
- Data backup and restoration operations""",
tools=[Redis,Mongo])