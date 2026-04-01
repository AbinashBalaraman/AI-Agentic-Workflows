import os
from dotenv import load_dotenv

load_dotenv()
os.environ["SERP_API_KEY"] = os.getenv("SERP_API_KEY", "")
os.environ["SERPAPI_API_KEY"] = os.getenv("SERP_API_KEY", "")
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY", "")
from langchain_community.tools.google_finance import GoogleFinanceQueryRun
from langchain_community.utilities.google_finance import GoogleFinanceAPIWrapper
from langchain.chat_models import init_chat_model
import google.generativeai as genai
from langchain_community.agent_toolkits.load_tools import load_tools
from langgraph.prebuilt import create_react_agent

try:
    llm = init_chat_model("gemini-2.0-flash", model_provider="google-genai")
except Exception as e:
    print("Error initializing LLM:", e)


tool = GoogleFinanceQueryRun(api_wrapper=GoogleFinanceAPIWrapper())
def search(query: str):
    response = tool.run(query)
    print(response)

query = "Compare Apple's and Tesla's stock performance over the past year and summarize 10 major differences."
search('nesley ticker name')

def ltools():
    tools = load_tools(["google-scholar", "google-finance"], llm=llm)
    return tools
def react_agent(a : str):
    agent = create_react_agent(llm, ltools())
    events = agent.stream({
        "messages": [(a)]
        
    },stream_mode="values")
    print(events)
    for event in events:
        print(event['messages'][-1].pretty_print())
#react_agent("Compare Apple's and Tesla's stock performance over the past year and summarize 10 major differences.")