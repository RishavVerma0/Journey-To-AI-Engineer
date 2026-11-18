import uuid
import time
import threading

from abc import ABC, abstractmethod
from collections import defaultdict, deque
from datetime import datetime
from enum import Enum


# --------------------------------
# Message 
# --------------------------------

class MessageStatus(Enum):
    PENDING = "Pending"
    PROCESSING = "Processing"
    ACKNOWLEDGED = "Acknowledged"
    FAILED = "Failed"


# --------------------------------
# Custom Exceptions
# --------------------------------

class TopicNotFoundError(Exception):
    pass


class ConsumerNotFoundError(Exception):
    pass


# --------------------------------
# Message Model
# --------------------------------

class Message:

    def __init__(self, payload, topic):

        self.message_id = str(uuid.uuid4())[:10]
        self.payload = payload
        self.topic = topic

        self.status = MessageStatus.PENDING
        self.retry_count = 0

        self.created_at = datetime.now()

    def __repr__(self):

        return (
            f"Message(id={self.message_id}, "
            f"status={self.status.value})"
        )


# --------------------------------
# Abstract Consumer
# --------------------------------

class BaseConsumer(ABC):

    def __init__(self, consumer_id):
        self.consumer_id = consumer_id

    @abstractmethod
    def process(self, message):
        pass


# --------------------------------
# Concrete Consumers
# --------------------------------

class EmailConsumer(BaseConsumer):

    def process(self, message): # type: ignore

        print(
            f"[EMAIL] Processing: {message.payload}"
        )

        time.sleep(1)

        return True


class AnalyticsConsumer(BaseConsumer):

    def process(self, message): # type: ignore

        print(
            f"[ANALYTICS] Processing: {message.payload}"
        )

        time.sleep(0.5)

        return True


# --------------------------------
# Topic Manager
# --------------------------------

class Topic:

    def __init__(self, name):

        self.name = name
        self.messages = deque()
        self.consumers = {}

        self.dead_letter_queue = deque()

    def add_message(self, message):
        self.messages.append(message)

    def register_consumer(self, consumer):

        self.consumers[
            consumer.consumer_id
        ] = consumer


# --------------------------------
# Message Broker
# --------------------------------

class MessageBroker:

    def __init__(self, max_retries=3):

        self.topics = {}

        self.max_retries = max_retries

        self.lock = threading.Lock()

    def create_topic(self, topic_name):

        if topic_name in self.topics:
            print("Topic already exists!")
            return

        self.topics[topic_name] = Topic(topic_name)

        print(f"Topic created: {topic_name}")

    def register_consumer(self, topic_name, consumer):

        topic = self.topics.get(topic_name)

        if not topic:
            raise TopicNotFoundError(topic_name)

        topic.register_consumer(consumer)

        print(
            f"Consumer {consumer.consumer_id} "
            f"subscribed to {topic_name}"
        )

    def publish(self, topic_name, payload):

        topic = self.topics.get(topic_name)

        if not topic:
            raise TopicNotFoundError(topic_name)

        message = Message(payload, topic_name)

        with self.lock:
            topic.add_message(message)

        print(
            f"Published message: {message.message_id}"
        )

        return message

    def consume(self, topic_name, consumer_id):

        topic = self.topics.get(topic_name)

        if not topic:
            raise TopicNotFoundError(topic_name)

        consumer = topic.consumers.get(consumer_id)

        if not consumer:
            raise ConsumerNotFoundError(consumer_id)

        with self.lock:

            if not topic.messages:
                return None

            message = topic.messages.popleft()

            message.status = MessageStatus.PROCESSING

        try:

            success = consumer.process(message)

            if success:

                message.status = MessageStatus.ACKNOWLEDGED

                print(
                    f"Message acknowledged: "
                    f"{message.message_id}"
                )

            else:

                self.handle_failure(topic, message)

        except Exception as error:

            print(f"Processing error: {error}")

            self.handle_failure(topic, message)

        return message

    def handle_failure(self, topic, message):

        message.retry_count += 1

        if message.retry_count <= self.max_retries:

            message.status = MessageStatus.PENDING

            with self.lock:
                topic.messages.append(message)

            print(
                f"Retrying message: {message.message_id}"
            )

        else:

            message.status = MessageStatus.FAILED

            topic.dead_letter_queue.append(message)

            print(
                f"Moved to Dead Letter Queue: "
                f"{message.message_id}"
            )

    def get_topic_statistics(self, topic_name):

        topic = self.topics.get(topic_name)

        if not topic:
            raise TopicNotFoundError(topic_name)

        return {
            "topic": topic_name,
            "pending": len(topic.messages),
            "dead_lettered": len(topic.dead_letter_queue),
            "consumers": len(topic.consumers)
        }


# --------------------------------
# Application
# --------------------------------

broker = MessageBroker(max_retries=2)

# Create topics
broker.create_topic("notifications")
broker.create_topic("analytics")

# Create consumers
email_worker = EmailConsumer("email-worker-01")

analytics_worker = AnalyticsConsumer(
    "analytics-worker-01"
)

# Register consumers
broker.register_consumer(
    "notifications",
    email_worker
)

broker.register_consumer(
    "analytics",
    analytics_worker
)

# Publish messages
print("\n----- Publishing Messages -----")

broker.publish(
    "notifications",
    {"user": "Rishav", "event": "Welcome"}
)

broker.publish(
    "notifications",
    {"user": "Rahul", "event": "Password Reset"}
)

broker.publish(
    "analytics",
    {"event": "Page Visit", "count": 150}
)

# Consume messages
print("\n----- Processing Messages -----")

broker.consume(
    "notifications",
    "email-worker-01"
)

broker.consume(
    "notifications",
    "email-worker-01"
)

broker.consume(
    "analytics",
    "analytics-worker-01"
)

# Display statistics
print("\n----- Broker Statistics -----")

print(
    broker.get_topic_statistics("notifications")
)

print(
    broker.get_topic_statistics("analytics")
)