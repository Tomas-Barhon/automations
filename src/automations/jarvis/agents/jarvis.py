from langgraph.graph import StateGraph
from langgraph.prebuilt import ToolNode, tools_condition
from automations.jarvis.tools.toolkit import AgentTools
from automations.jarvis.agents.base_agent import AgentState, BaseAgent
from automations.jarvis.memory.memory_factory import MemoryType
from langchain.chat_models import BaseChatModel
from pathlib import Path
from automations.jarvis.prompt_loader.prompt_loader import PromptType
from langchain_core.runnables import Runnable
from typing import Iterator


class Jarvis(BaseAgent):
    def __init__(
        self,
        chat_model: BaseChatModel,
        toolkit: AgentTools,
        memory_type: MemoryType,
    ) -> None:
        super().__init__(chat_model, toolkit, memory_type, name="Jarvis")
        self.graph = self.build_graph()
        self.compiled_graph = self.compile_graph(self.graph)

    # TODO: Refactor logic, adding system prompts
    def __call__(self, messages, config, **kwargs) -> Iterator:
        state = {"messages": [{"role": "user", "content": messages}]}
        return self.compiled_graph.stream(state, config=config, **kwargs)

    def call_chat_model(self, state: AgentState) -> dict:
        print("Calling model")
        # Update message history with response:
        return {"messages": [self.agent.invoke(state["messages"])]}

    def build_graph(self) -> StateGraph:
        self.langchain_graph_builder = StateGraph(state_schema=AgentState)
        self.langchain_graph_builder.add_node("model", self.call_chat_model)

        tool_node = ToolNode(tools=self.toolkit.tools)
        self.langchain_graph_builder.add_node("tools", tool_node)
        self.langchain_graph_builder.add_conditional_edges(
            "model", tools_condition
        )
        self.langchain_graph_builder.add_edge("tools", "model")
        self.langchain_graph_builder.set_entry_point("model")
        return self.langchain_graph_builder

    def compile_graph(self, graph: StateGraph, **compile_kwargs) -> Runnable:
        return graph.compile(checkpointer=self.memory, **compile_kwargs)

    def load_prompt(
        self, prompt_file_name: Path | str, prompt_type: PromptType
    ) -> "Jarvis":
        self.prompt = self.prompt_loader.load_prompt(
            prompt_file_name, prompt_type
        )
        return self
