import asyncio
import os
from dotenv import load_dotenv
load_dotenv()
from langchain_google_community import CalendarToolkit
from langchain_google_community.calendar.utils import (
    build_resource_service,
    get_google_credentials,
)
import getpass
from langchain.chat_models import init_chat_model
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver as memory
from datetime import datetime, timezone, timedelta
from typing import AsyncIterable, Any
from a2a.utils import task,new_agent_text_message,new_task
from a2a.server.agent_execution import AgentExecutor
from a2a.server.agent_execution.context import RequestContext
from a2a.server.events.event_queue import EventQueue
from a2a.server.tasks import TaskUpdater
from a2a.types import TaskState,UnsupportedOperationError,AgentCard,AgentSkill,AgentCapabilities
from httpx import AsyncClient
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryPushNotifier, InMemoryTaskStore
from a2a.server.apps import A2AStarletteApplication
import uvicorn

credentials = get_google_credentials(
    token_file="token.json",
    scopes=["https://www.googleapis.com/auth/calendar"],
    client_secrets_file="credentials.json",
)
api_resource = build_resource_service(credentials=credentials)
toolkit = CalendarToolkit(api_resource=api_resource)
llm = init_chat_model(model="gpt-4o", temperature=0.0,model_provider="openai")
agent=create_react_agent(model=llm,tools=toolkit.get_tools(),prompt="You are a helpful assistant that can answer questions about Google Calendar. You can also create, update, and delete events in the calendar. Use the tools provided to interact with the calendar. If you need to create an event, make sure to ask for the necessary details such as title, start time, end time, and description. If you need to update or delete an event, ask for the event ID or any other identifying information. Be clear and concise in your responses.",checkpointer=memory())

class gagent:
    async def stream(self, query,conrext_id) -> AsyncIterable[dict[str, Any]]:
        
        self.agent = agent
        self.inputs = {'messages': [('user', query)]}
        self.config = {'configurable': {'thread_id': conrext_id}}
        async for item in self.agent.astream(self.inputs, self.config, stream_mode='values'):
            message = item['messages'][-1]
            yield {'content': message.content, 'is_task_complete': False, 'require_user_input': False}

class agentexecutor(AgentExecutor):
    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        query = context.get_user_input()
        task = new_task(context.message)
        await event_queue.enqueue_event(task)
        updater = TaskUpdater(event_queue,task.id,task.contextId)
        async for item in gagent().stream(query,task.contextId):
            await updater.update_status(
                TaskState.working,new_agent_text_message(item['content'],task.contextId))
        await updater.complete()
    

    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        return await super().cancel(context, event_queue)
capabilities = AgentCapabilities(streaming=True, pushNotifications=True)
skill = AgentSkill(
    id='Google Calendar Agent',
    name='Google Calendar Agent',
    description='An agent that can manage Google Calendar events',
    tags=['calendar', 'google', 'events'],
    examples=['Create a new event for tomorrow at 10 AM', 'What events do I have today?', 'Update my meeting on Friday to 3 PM'],
)
agent_card = AgentCard(
    name='Google Calendar Agent',
    description='An agent that can manage Google Calendar events',
    url='http://localhost:8005/',
    version='1.0.0',
    defaultInputModes=['text'],
    defaultOutputModes=['text'],
    capabilities=capabilities,
    skills=[skill]
)

httpx_client = AsyncClient()
reqhandler = DefaultRequestHandler(agent_executor=agentexecutor(),task_store=InMemoryTaskStore(),push_notifier=InMemoryPushNotifier(httpx_client))

server = A2AStarletteApplication(agent_card=agent_card,http_handler=reqhandler)
if __name__ == "__main__":
    uvicorn.run(server.build, host="localhost", port=8005)

