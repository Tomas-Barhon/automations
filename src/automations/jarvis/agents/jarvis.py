from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, CompiledStateGraph
from langgraph.prebuilt import ToolNode, tools_condition
from automations.jarvis.tools.toolkit import Toolkit
from automations.jarvis.agents.base_agent import AgentState, BaseAgent
from automations.jarvis.memory.memory_factory import MemoryType
from langchain.chat_models import BaseChatModel
from pathlib import Path


class Jarvis(BaseAgent):
    def __init__(
        self,
        chat_model: BaseChatModel,
        toolkit: Toolkit,
        memory_type: MemoryType,
    ) -> None:
        super().__init__(chat_model, toolkit, memory_type)
        self.graph = self.build_graph()
        self.compiled_graph = self.compile_graph(self.graph)

    def __call__(self, state: AgentState):
        print("Calling model")
        # Update message history with response:
        return {"messages": [self.chat_model.invoke(state["messages"])]}

    def build_graph(self) -> StateGraph:
        self.langchain_graph_builder = StateGraph(state_schema=AgentState)
        self.langchain_graph_builder.add_node("model", self.__call__)

        tool_node = ToolNode(tools=self.toolkit.tools)
        self.langchain_graph_builder.add_node("tool_node", tool_node)
        self.langchain_graph_builder.add_conditional_edges(
            "model", tools_condition
        )
        self.langchain_graph_builder.add_edge("tool_node", "model")
        self.langchain_graph_builder.set_entry_point("model")
        return self.langchain_graph_builder

    def compile_graph(
        self, graph: StateGraph, **compile_kwargs
    ) -> CompiledStateGraph:
        return graph.compile(checkpointer=self.memory, **compile_kwargs)

    def load_prompt(
        self, prompt_file_name: Path | str, prompt_type: Path | str
    ) -> dict:
        return self.prompt_loader.load_prompt(prompt_file_name, prompt_type)
