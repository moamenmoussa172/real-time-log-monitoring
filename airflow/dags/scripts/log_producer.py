from kafka import KafkaProducer
import time
import random
import json

# Kafka topic name
TOPIC = 'logs-topic'

# Initialize Kafka producer
producer = KafkaProducer(
    bootstrap_servers='kafka:9093',  # Use localhost to connect from the host machine
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Simulate log data
def generate_log():
    # Define log types
    log_types = ['user_activity', 'server_error', 'payment']
    log_type = random.choice(log_types)

    # Generate log based on type
    if log_type == 'user_activity':
        log = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "log_level": "INFO",
            "log_type": "user_activity",
            "message": f"User {random.randint(100, 999)} {random.choice(['viewed', 'added to cart', 'purchased'])} product {random.randint(1000, 9999)}"
        }
    elif log_type == 'server_error':
        log = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "log_level": random.choice(["WARNING", "ERROR"]),
            "log_type": "server_error",
            "message": random.choice([
                "Database connection timeout",
                "High memory usage detected on server",
                "Failed to process API request"
            ])
        }
    elif log_type == 'payment':
        success = random.choice([True, False])
        if success:
            log = {
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "log_level": "INFO",
                "log_type": "payment",
                "message": f"Successful payment for order {random.randint(1000, 9999)}, amount ${random.uniform(10.0, 200.0):.2f}"
            }
        else:
            log = {
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "log_level": "ERROR",
                "log_type": "payment",
                "message": f"Payment failed for order {random.randint(1000, 9999)}, reason: insufficient funds"
            }
    return log

# Continuously produce logs
while True:
    log_message = generate_log()
    producer.send(TOPIC, log_message)
    print(f"Produced: {log_message}")
    time.sleep(2)  # Simulate log generation every 2 seconds