import datetime
import os
from dotenv import load_dotenv
# from langchain_google_community import CalendarToolkit
# from langchain_google_community.calendar.utils import (
#     build_resource_service,
#     get_google_credentials,
# )
import getpass
from langchain.chat_models import init_chat_model
from langgraph.prebuilt import create_react_agent
import pytz
from datetime import datetime, timezone, timedelta
from O365 import Account
from O365.utils.token import FileSystemTokenBackend
from langchain_community.agent_toolkits import O365Toolkit
from langchain_community.tools.office365 import O365CreateDraftMessage
from langchain_community.tools.office365 import O365SearchEmails
from langchain_community.tools.office365 import O365SearchEvents
from langchain_community.tools.office365 import O365SendEvent
from langchain_community.tools.office365 import O365SendMessage
os.environ["CLIENT_ID"]="e573c8de-ce16-4281-ace7-f8dec2500184"
# os.environ["CLIENT_SECRET"]="f43a1759-79a2-4745-bc10-a14192c08571"
from python_a2a import to_a2a_server

load_dotenv()
# credentials = get_google_credentials(
#     token_file="token.json",
#     scopes=["https://www.googleapis.com/auth/calendar"],
#     client_secrets_file="credentials.json",
# )
# api_resource = build_resource_service(credentials=credentials)
# toolkit = CalendarToolkit(api_resource=api_resource)


account = Account(
    credentials=("e573c8de-ce16-4281-ace7-f8dec2500184", None),
    token_backend=FileSystemTokenBackend(token_path='.', token_filename='o365_token.txt')
)
if not account.is_authenticated:
    account.authenticate(scopes=['basic', 'calendar_all'])
toolkit1 = O365Toolkit(account=account)
toolkit1.model_rebuild()
O365SearchEvents.model_rebuild()
O365SearchEmails.model_rebuild()
O365SendEvent.model_rebuild()
O365SendMessage.model_rebuild()
O365CreateDraftMessage.model_rebuild()

tools1 = toolkit1.get_tools()
llm = init_chat_model("gemini-2.5-flash", model_provider="google_genai")
# tools = toolkit.get_tools()
current_time = datetime.now()  

agent_executor = create_react_agent(llm, tools1)
current_time = datetime.now()  
llm_server = to_a2a_server(llm)
conversation_history = []
print("Welcome to the Calendar Assistant! Type 'exit' or 'quit' to end the conversation.")
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from python_a2a import A2AClient, run_server
from python_a2a.langchain import to_a2a_server
# Create a simple chain
template = f"You are an AI agent designed to perform calendar tasks. The current date and time is {current_time.strftime('%Y-%m-%d %H:%M:%S')}When creating events, set a default duration of one hour using the user's own account email : abinash.b@kestoneglobal.biz. If an attendee is to be added, ask for their email address.as the current time is IST set the time 5 hours 30 minutes earlier than the current time for all events to send as UTC timezone, but show me the time in only IST timezone."""
prompt = PromptTemplate.from_template(template)
travel_chain = prompt | llm | StrOutputParser()

# Convert chain to A2A server
travel_server = to_a2a_server(travel_chain)

# Run servers in background threads
import threading
llm_thread = threading.Thread(
    target=lambda: run_server(llm_server, port=5003),
    daemon=True
)
llm_thread.start()

travel_thread = threading.Thread(
    target=lambda: run_server(travel_server, port=5004),
    daemon=True
)
travel_thread.start()
import time

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Shutting down servers.")
# while False:
#     user_input = input("You: ")
    
#     if user_input.lower() in ["exit", "quit"]:
#         print("Goodbye!")
#         break
#     system_prompt = (
#     "You are an AI agent designed to perform calendar tasks. "
#     f"The current date and time is {current_time.strftime('%Y-%m-%d %H:%M:%S')}"
#     "When creating events, set a default duration of one hour using the user's own account email : abinash.b@kestoneglobal.biz. "
#     "If an attendee is to be added, ask for their email address."
#     "as the current time is IST set the time 5 hours 30 minutes earlier than the current time for all events to send as UTC timezone, but show me the time in only IST timezone."
    
# )
#     if user_input.strip():
#         conversation_history.append(("user", user_input))
#     messages = [("system",system_prompt)]+conversation_history
#     events = agent_executor.stream(
#         {
#             "messages": messages,
#             "time": current_time
#         },
#         stream_mode="values",
#     )

#     for event in events:
#         reply = event["messages"][-1].content
#         print("Agent:", reply)
#         conversation_history.append(("ai", reply))