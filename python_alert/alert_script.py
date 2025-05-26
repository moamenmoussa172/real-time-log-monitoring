from kafka import KafkaConsumer
from datetime import datetime, timedelta
import time
import json

# Configuration
KAFKA_BROKER = "localhost:9092"  # Update if using a different Kafka broker
TOPIC = "logs-topic"
THRESHOLD = 10  # Number of ERROR logs to trigger an alert
WINDOW = 300  # Time window in seconds (5 minutes)
ALERT_LOG_FILE = "alerts.log"

# In-memory storage for logs
error_logs = []

def log_alert(error_count):
    """
    Log the alert to the console and save it to a file.
    """
    alert_message = f"ALERT! {error_count} ERROR logs detected in the last {WINDOW // 60} minutes. Timestamp: {datetime.now()}"
    print(alert_message)
    
    # Save the alert to a file
    with open(ALERT_LOG_FILE, "a") as file:
        file.write(alert_message + "\n")

def consume_logs():
    """
    Consume logs from the Kafka topic and check for ERROR logs.
    """
    global error_logs

    # Connect to Kafka
    consumer = KafkaConsumer(
        TOPIC,
        bootstrap_servers=[KAFKA_BROKER],
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        value_deserializer=lambda x: json.loads(x.decode("utf-8"))
    )
    print(f"Connected to Kafka topic: {TOPIC}")

    for message in consumer:
        log = message.value
        log_level = log.get("log_level", "").upper()
        timestamp = datetime.strptime(log.get("timestamp", ""), "%Y-%m-%d %H:%M:%S")

        # Add ERROR logs to the in-memory storage
        if log_level == "ERROR":
            error_logs.append(timestamp)

        # Remove logs older than the time window
        five_minutes_ago = datetime.now() - timedelta(seconds=WINDOW)
        error_logs = [log_time for log_time in error_logs if log_time >= five_minutes_ago]

        # Check if the threshold is exceeded
        if len(error_logs) >= THRESHOLD:
            log_alert(len(error_logs))

        # Debugging: Print log counts
        print(f"Total ERROR logs in the last {WINDOW // 60} minutes: {len(error_logs)}")

if __name__ == "__main__":
    consume_logs()