from abc import ABC, abstractmethod
from typing import Annotated, TypedDict
from langchain.chat_models import BaseChatModel
from langgraph.graph.message import add_messages
from langgraph.graph.state import CompiledStateGraph
from automations.jarvis.tools.toolkit import Toolkit
from automations.jarvis.memory.memory_factory import (
    MemoryType,
    AgentMemoryFactory,
)


class AgentState(TypedDict):
    messages: Annotated[list, add_messages]


class BaseAgent(ABC):
    def __init__(
        self,
        chat_model: BaseChatModel,
        toolkit: Toolkit,
        memory_type: MemoryType,
    ) -> None:
        self.chat_model = chat_model
        self.toolkit = toolkit
        self.agent = self.chat_model.bind_tools(self.toolkit.tools)
        self.memory = AgentMemoryFactory()._create_memory(memory_type)

    @abstractmethod
    def build_graph(self):
        pass

    @abstractmethod
    def compile_graph(self) -> CompiledStateGraph:
        pass

    @abstractmethod
    def load_prompt(self):
        pass

    @abstractmethod
    def __call__(self, prompt: str) -> str:
        pass
