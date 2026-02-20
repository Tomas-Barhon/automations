import os
import time
from typing import Annotated, Tuple, TypedDict
from abc import ABC, abstractmethod
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from automations.jarvis.tools.toolkit import Toolset
from automations.jarvis.agents.base_agent import AgentState, BaseAgent
from automations.jarvis.memory.memory_factory import MemoryType
from langchain_core.chat_models import BaseChatModel
from automations.jarvis.tools.toolkit import Toolkit


class Jarvis(BaseAgent):
    def __init__(
        self,
        chat_model: BaseChatModel,
        toolkit: Toolkit,
        memory_type: MemoryType,
    ) -> None:
        super().__init__(chat_model, toolkit, memory_type)

        load_dotenv()

        self.agent = self.llm.bind_tools(self.toolkit.get_tools())

        # Building LangGraph workflow
        self.langchain_graph_builder = StateGraph(state_schema=AgentState)
        self.langchain_graph_builder.add_node("model", self.call_model)

        tool_node = ToolNode(tools=self.toolkit.get_tools())
        self.langchain_graph_builder.add_node("tool_node", tool_node)
        self.langchain_graph_builder.add_conditional_edges(
            "model", tools_condition
        )
        self.langchain_graph_builder.add_edge("tool_node", "model")
        self.langchain_graph_builder.set_entry_point("model")

        # Add memory
        # TODO: Upgrade to PostgreSQL database
        self.chat_memory = MemorySaver()
        self.graph = self.langchain_graph_builder.compile(
            checkpointer=self.chat_memory
        )

    def call_model(self, state: AgentState):
        print("Calling model")
        # Update message history with response:
        return {"messages": [self.llm.invoke(state["messages"])]}
