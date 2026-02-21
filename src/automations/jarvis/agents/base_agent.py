from abc import ABC, abstractmethod
from pathlib import Path
from typing import Annotated, TypedDict, Optional
from langchain.chat_models import BaseChatModel
from langgraph.graph.message import add_messages
from langgraph.graph.state import CompiledStateGraph
from automations.jarvis.tools.toolkit import Toolkit
from automations.jarvis.memory.memory_factory import (
    MemoryType,
    AgentMemoryFactory,
)
from langgraph.graph import StateGraph
from automations.jarvis.prompt_loader.prompt_loader import PromptLoader


class AgentState(TypedDict):
    messages: Annotated[list, add_messages]


class BaseAgent(ABC):
    def __init__(
        self,
        chat_model: BaseChatModel,
        toolkit: Toolkit,
        memory_type: MemoryType,
        prompt_dir: Optional[Path | str] = None,
    ) -> None:
        self.chat_model = chat_model
        self.toolkit = toolkit
        self.agent = self.chat_model.bind_tools(self.toolkit.tools)
        self.memory = AgentMemoryFactory()._create_memory(memory_type)
        # TODO: refactor default
        self.prompt_loader = PromptLoader(
            prompt_dir or Path("src/automations/jarvis/prompts")
        )

    @abstractmethod
    def build_graph(self) -> StateGraph:
        pass

    @abstractmethod
    def compile_graph(
        self, graph: StateGraph, **compile_kwargs
    ) -> CompiledStateGraph:
        pass

    @abstractmethod
    def load_prompt(
        self, prompt_file_name: Path | str, prompt_type: str
    ) -> dict:
        pass

    @abstractmethod
    def __call__(self, state: AgentState) -> dict:
        pass
