import json
from datetime import datetime

from kafka import KafkaProducer

# Create producer
producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)

# Send a test message
message = {
    "timestamp": datetime.now().isoformat(),
    "subject": "Test Email",
    "from": "test@example.com",
    "body": "This is a test message",
}

# Send to topic
future = producer.send("email-events", value=message)

# Wait for send to complete
record_metadata = future.get(timeout=10)

print("Message sent successfully!")
print(f"Topic: {record_metadata.topic}")
print(f"Partition: {record_metadata.partition}")
print(f"Offset: {record_metadata.offset}")

# Close producer
producer.close()
