from automations.jarvis.agents.base_agent import BaseAgent
from automations.jarvis.server.repl_input_listener import REPLInputListener

# from automations.jarvis.agents.IO.agent_input import AgentInput
# from automations.jarvis.agents.IO.agent_output import AgentOutput
from automations.jarvis.agents.jarvis import Jarvis
from langchain_ollama import ChatOllama
from automations.jarvis.memory.memory_factory import MemoryType
from automations.jarvis.tools.toolkit import AgentTools
from automations.jarvis.server.base_event_listener import BaseEventListener
from automations.jarvis.server.output_printer import OutputPrinter


class AgentRunner:
    def __init__(
        self,
        agent: BaseAgent,
        agent_input_listener: BaseEventListener,
        agent_output_listener: BaseEventListener,
    ):
        self.agent = agent
        self.agent_input_listener = agent_input_listener
        self.ageent_output_listener = agent_output_listener

    def start_agent(self):
        print(f"Starting agent: {self.agent.name}")
        print(
            f"""Listening for user input with
            {self.agent_input_listener.__class__.__name__}..."""
        )
        print(
            f"""Outputing with
            {self.ageent_output_listener.__class__.__name__}..."""
        )
        self.run()

    def run(self):
        user_input = self.agent_input_listener.listen_for_input()
        if user_input:
            print(f"Received input: {user_input}")
            # agent_input = AgentInput(role="user", content=user_input)
            # agent_output = self.agent.process_input(agent_input)
            # self.ageent_output_listener.listen(agent_output.message)


def main():
    chat_model = ChatOllama(model="deepseek-r1:1.5b", temperature=0)

    toolkit = AgentTools.from_tool_names(["NOTION_DB"])

    agent = Jarvis(
        chat_model=chat_model,
        toolkit=toolkit,
        memory_type=MemoryType.IN_MEMORY,
    )

    input_listener = REPLInputListener()
    output_listener = OutputPrinter()

    runner = AgentRunner(agent, input_listener, output_listener)
    runner.start_agent()


if __name__ == "__main__":
    main()
