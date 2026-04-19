from langchain.agents import create_agent
from langchain.agents.middleware import AgentState
from langchain_core.messages import SystemMessage
from langgraph.checkpoint.memory import InMemorySaver
from utils.logger_handler import logger
from utils.prompts_loder import get_main_prompt
from model.model import get_chat_model
from agent.tools import (
    get_user_id,
    get_current_month,
    fetch_external_data,
    rag_summarize,
    get_weather,
    get_user_location,
    fill_context_for_report
)
from agent.middleware import monitor_tool, monitor_model, select_prompt


class Agent:
    def __init__(self, model_name="qwen3-max-2026-01-23", temperature=0.7):
        self.model_name = model_name
        self.temperature = temperature
        self.llm = get_chat_model(model_name, temperature=temperature)
        self.prompt = SystemMessage(get_main_prompt())
        self.checkpointer = InMemorySaver()
        self.tools = [
            get_user_id,
            get_current_month,
            fetch_external_data,
            rag_summarize,
            get_weather,
            get_user_location,
            fill_context_for_report
        ]
        self.middleware = [monitor_tool, monitor_model, select_prompt]
        self.agent = self._create_agent()

    def _create_agent(self):
        return create_agent(
            model=self.llm,
            tools=self.tools,
            system_prompt=self.prompt,
            middleware=self.middleware,
            checkpointer=self.checkpointer
        )

    def invoke(self, input_data, config=None):
        if isinstance(input_data, str):
            input_data = {"messages": [("user", input_data)]}
        return self.agent.invoke(input_data, config)

    async def ainvoke(self, input_data, config=None):
        if isinstance(input_data, str):
            input_data = {"messages": [("user", input_data)]}
        return await self.agent.ainvoke(input_data, config)

    def stream(self, input_data, config=None):
        if isinstance(input_data, str):
            input_data = {"messages": [("user", input_data)]}
        for chunk in self.agent.stream(input_data, config,stream_mode="values",context={"report": "False"}):
            last_message = chunk["messages"][-1]
            if last_message.content:
                yield last_message.content.strip()+"\n" 

if __name__ == "__main__":
    agent = Agent()
    response = agent.invoke("26摄氏度，该怎么保养")
    print(response)