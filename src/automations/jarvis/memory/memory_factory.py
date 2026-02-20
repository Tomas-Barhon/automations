from enum import Enum
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.checkpoint.postgres import PostgresSaver


class MemoryType(Enum):
    IN_MEMORY = "in_memory"
    POSTGRESQL = "postgresql"


class AgentMemoryFactory:
    def __init__(self):
        pass

    def _create_memory(
        self, memory_type: MemoryType, **db_config
    ) -> InMemorySaver | PostgresSaver:
        match memory_type:
            case MemoryType.IN_MEMORY:
                return InMemorySaver()
            case MemoryType.POSTGRESQL:
                return PostgresSaver(**db_config)
