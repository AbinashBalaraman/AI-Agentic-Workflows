from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.sessions import InMemorySessionService
from google.adk.memory import InMemoryMemoryService
from google.adk.runners import Runner
from typing import Optional, Any,Dict
from google.adk.tools import ToolContext, BaseTool
from O365 import Account,FileSystemTokenBackend
from langchain_community.agent_toolkits import O365Toolkit
from google.genai import types
from google.adk.tools.langchain_tool import LangchainTool
from datetime import datetime
from dotenv import load_dotenv
from langchain_community.tools.office365 import O365CreateDraftMessage
from langchain_community.tools.office365 import O365SearchEmails
from langchain_community.tools.office365 import O365SearchEvents
from langchain_community.tools.office365 import O365SendEvent
from langchain_community.tools.office365 import O365SendMessage
import asyncio

load_dotenv()
account = Account(
    credentials=("e573c8de-ce16-4281-ace7-f8dec2500184", None),
    token_backend=FileSystemTokenBackend(token_path='.', token_filename='o365_token.txt')
)
if not account.is_authenticated:
  account.authenticate(scopes=[
    'basic',
    'calendar_all', 
    'calendar_shared_all',
    'message_all',
    'message_send',
    'address_book_all',
    'onedrive_all',
    'tasks_all'
])
toolkit1 = O365Toolkit(account=account)

toolkit1.model_rebuild()

O365SearchEmails.model_rebuild()
O365SendEvent.model_rebuild()
O365SendMessage.model_rebuild()
O365CreateDraftMessage.model_rebuild()
O365SearchEvents.model_rebuild()
wrapped_tools = [LangchainTool(tool=t) for t in toolkit1.get_tools()]
current_time = datetime.now()  


def handle_tool_error( error: Exception)-> Optional[dict]:
    """Handle tool execution errors gracefully"""
    return {
        "success": False,
        "error_message": f"Stock data tool encountered an issue: {str(error)}",
        "continue_execution": True
    }

def before_errors(
    tool: BaseTool,
    tool_response: dict,
    tool_context: ToolContext,
    args: dict,
) -> Optional[dict]:
    """Intercept tool responses and handle errors gracefully."""
    print(f"\nfdfdfd{tool_response}\nsdksmdksm")
    # Check if tool response indicates an error
    if isinstance(tool_response, dict) and tool_response.get('status') == 'error':
        # Log the error
        print(f"Tool {tool.name} failed: {tool_response.get('error_message')}")
        
        # Transform error response for the agent
        return {
            "status": "error",
            "message": "I encountered an issue with the service. Please try again or contact support.",
            "retry_suggested": True
        }
    
    return tool_response  # Pass through successful responses

def handle_tool_errors(
    tool: BaseTool,  # The tool being called
    tool_args: Dict[str, Any],  # Arguments passed to the tool
    tool_context: ToolContext  # Access to agent state/session
) -> Optional[Dict[str, Any]]:
    """Validate and log inputs before tool execution."""
    print("Dsnkkkkkkkkkkkkkkkkkkkkkkkksmfd ,sdfdnfd,mfldnfkldjnfkdjn")
    print(f"[Before Tool] Calling {tool.name} with args: {tool_args}")
    
    # Example validation: Ensure 'query' is provided and not empty
    if 'query' not in tool_args or not tool_args['query']:
        print("[Validation Failed] Query is missing or empty.")
        return {"error": "Invalid input: Query is required."}  # Override to skip tool
    
    # Modify args if needed (e.g., add a default parameter)
    tool_args['max_results'] = 5
    
    # Access and update context state
    tool_context.state['last_tool_called'] = tool.name
    
    return tool_args  # Return modified args to proceed with execution




session_service = InMemorySessionService()
Memory_service = InMemoryMemoryService()



root_agent= Agent(name="calander_Agent", generate_content_config=types.GenerateContentConfig(
        temperature=0.75),model="gemini-2.0-flash",instruction=f"""
        -you can access conversation history
        Your primary instructions are:
                  -dont directly call tools, first analyse the instruction or data and decide how and which tool to call and complete task without error
                  -ensure which format and data needed for each tool and try to convert given data to that format dont raise error by sending unsupported format to tools
                  -inform the agent or user which calling you about the data needs and format to proceed with tool
                  -Agent to manage microsoft calender with available tools switch to master agrnt after completing every tast given by master agent don't directly communicate with user give all the information to master agent so Master agent could communicate with user behalf of you...You are an AI agent designed to perform microsft 365 tools actions. "
                  "The current date and time is {current_time.strftime('%Y-%m-%d %H:%M:%S')}"
                  "When creating events, set a default duration of one hour using the user's own account email : abinash.b@kestoneglobal.biz. "
                  "If an attendee is to be added, ask for their email address."
                  "the calendar blocking tool consider your time as UTC and add 5hour 30 mins in th time you send to covert it to IST so while sending time to the calender event tool for event or blocking send time as 5 hour 30 min befor eg.if user said 3pm you send 9.30am to the tool but tell user booked at 3pm"
                   Calendar blocking agent: This agent helps schedule and block calendar events efficiently.
                  It can create, update, and manage calendar entries based on user requests.
                  if i didn't provided enough information or given wrong or unrelated info for any tool function don't directly send operation with incomplete data you have to confirm data format and required data befor sent to the curresponding tool send only correct data to the tool calling
                 "When 'include_recurring' is True you must provide a 'start_recurring' and 'end_recurring' with a datetime string.""",
description= """access microsft 365 tools like calender blocking, search events ,search in mail ,send mails,send evnts,send message ,draft message""", 
before_tool_callback=handle_tool_errors,tools=[wrapped_tools[0],wrapped_tools[1],wrapped_tools[2],wrapped_tools[3],wrapped_tools[4]],output_key="calender_response",after_tool_callback=before_errors)

session_id="b"


if __name__== "__main__" :
    async def main():
        a=await session_service.create_session(user_id="A",session_id="b",app_name="Calendar")
        runner= Runner(app_name="Calendar",agent=root_agent,session_service=session_service,memory_service=Memory_service)
        while True:
            intputt=input("here ")
            if intputt == "q":
                break
            else :
                try:
                  events=[event async for event in runner.run_async(user_id="A",session_id=session_id,new_message=types.Content(role="user",parts=[types.Part(text=intputt)]))]
                  for event in reversed(events):
                       if event.is_final_response() and hasattr(event, 'content') and event.content:
                            print(f"Agent: {event.content.parts[0].text}")
                            break
                except Exception as e:
                   print(f"Memory check failed: {e}")
            await Memory_service.add_session_to_memory(a)
    asyncio.run(main())

