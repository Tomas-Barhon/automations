import json

from kafka import KafkaConsumer

# Create consumer
consumer = KafkaConsumer(
    "email-events",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="earliest",  # Start from beginning
    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
)

print("Listening for messages... (Press Ctrl+C to stop)")

# Read messages
for message in consumer:
    print("\n--- Message Received ---")
    print(f"Partition: {message.partition}")
    print(f"Offset: {message.offset}")
    print(f"Data: {message.value}")
