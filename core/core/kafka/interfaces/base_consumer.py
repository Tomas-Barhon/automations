from core.email_connector.interfaces.polling import PollingServiceInterface


class KafkaConsumerInterface(PollingServiceInterface):
    """Interface for a Kafka consumer that polls messages from a Kafka topic."""

    def __init__(self, topic: str, group_id: str, bootstrap_servers: str):
        self.topic = topic
        self.group_id = group_id
        self.bootstrap_servers = bootstrap_servers

    def poll_messages(self) -> list[dict] | None:
        """Poll for new messages from the Kafka topic."""
