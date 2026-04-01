from google.adk.agents import Agent,sequential_agent
from google.adk.tools import agent_tool
from google.adk.models.lite_llm import LiteLlm
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types
from a2a.types import  Message,SendStreamingMessageRequest,SendStreamingMessageResponse,MessageSendParams,SendMessageRequest,SendMessageResponse,Part
from prompt import d 
import warnings
import logging
from dotenv import load_dotenv
load_dotenv()
warnings.filterwarnings("ignore")
logging.basicConfig(level=logging.ERROR)
from Redis.agent import root_agent as redis_agent
# from yfinance.agent import root_agent as yfinance_agent
# from .calendar.agent import root_agent as calendar_agent
from a2a.client import A2AClient,A2ACardResolver
import httpx,json
from uuid import uuid4
from typing import Any
from pydantic import BaseModel

def add_numbers_tool(a : int ,b:int) -> int:
    """A simple tool to add two numbers.
    Args:
        a (int): The first number.
        b (int): The second number.  
        Returns:int: The sum of the two numbers.
        """

    return a + b

async def gcalh (query:str):
    async with httpx.AsyncClient() as ht:
       resolver=A2ACardResolver(base_url="http://localhost:8005",httpx_client=ht)
    send_message_payload: dict[str, Any] = {
    'message': {
        'role': 'user',
        'parts': [
            {'kind': 'text', 'text': query}
        ],
        'messageId': uuid4().hex,
    },
} 
    client=A2AClient(httpx_client=ht,url="http://localhost:8005")
    response= client.send_message_streaming(SendStreamingMessageRequest(id="1",jsonrpc="2.0",method="message/stream",params=MessageSendParams(**send_message_payload)))
    async for i in response:
     print(i)
import asyncio
#asyncio.run(gcalh("hi"))
import asyncio,json
from a2a.types import Message, TextPart, Role  # adjust import path if different
from httpx_sse import SSEError, aconnect_sse

async def gcal(qry: list,ua: str) :
    """Send a streaming request to the local A2A agent and print every chunk."""
    query= str(qry)+ua
    # 1️⃣ Keep everything **inside** the AsyncClient context
    async with httpx.AsyncClient(timeout=20) as ht:
        # 3️⃣ Create the client that will talk to the agent
        client = A2AClient(httpx_client=ht, url="http://localhost:8005")              # [1][2]
       
        # 4️⃣ Build an A2A Message object instead of a raw dict
        msg = Message(kind="message",parts=[(Part(TextPart(kind='text',text=query)))],messageId=str(uuid4()),role=Role.user)

        # 5️⃣ Wrap it in the standard request model
        request = SendStreamingMessageRequest(
            id=uuid4().hex,
            params=MessageSendParams(message=msg)
        
        )
        r=[]
        try:
          async for event in client.send_message_streaming(request):
            a=event.model_dump(mode="json", exclude_none=True)
            try:
                if a["result"]["status"]["message"]["parts"][0]["text"]:
                    r.append(a["result"]["status"]["message"]["parts"][0]["text"])
            except Exception as e:
                E=e
        except Exception as er:
           return er        
        return (r[-1])
async def gc():
    dz=[]
    while True:
        a=input("hi :" )
        if a=="q":
          break
        b=await gcal(dz,a)
        print(b)
        c={"user": a,"agent":b}
        dz.append(c)
        
asyncio.run(gc())

# coordinator= Agent(name="MasterAgent",model="gemini-2.0-flash",instruction=d,
#                   tools=[add_numbers_tool,agent_tool.AgentTool(calendar_agent),agent_tool.AgentTool(yfinance_agent),agent_tool.AgentTool(redis_agent)])
# root_agent = coordinator
#agent_tool.AgentTool(agent=redis_agent),


dz=[]
async def gcal(qry: list,ua: str) :
    """Send a streaming request to the local A2A agent and print every chunk."""
    query= str(qry)+ua
    async with httpx.AsyncClient(timeout=20) as ht:
        client = A2AClient(httpx_client=ht, url="http://localhost:8005") 
        msg = Message(kind="message",parts=[Part(TextPart(kind='text',text=query))],
                      messageId=uuid4().hex,
                      role=Role.user)
        request = SendStreamingMessageRequest(
            id=uuid4().hex,
            params=MessageSendParams(message=msg)
        )

        r=[]
        async for event in client.send_message_streaming(request):
            a=event.model_dump(mode="json", exclude_none=True)
            try:
                text=a["result"]["status"]["message"]["parts"][0]["text"]
                if text:
                    r.append(text)
            except Exception as e:
                E=e
        return (r[-1])
        
async def gc(query: str)-> str:
        """send your query regarding to google calender"""
        a=query
        b=await gcal(dz,a)
        print(b)
        c={"user": a,"agent":b}
        
        dz.append(c)
        return b 
