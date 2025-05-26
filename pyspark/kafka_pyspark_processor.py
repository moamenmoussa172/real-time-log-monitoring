from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StringType, TimestampType
from pyspark.sql.functions import col, from_json, to_timestamp

# Initialize Spark Session
spark = SparkSession.builder \
    .appName("KafkaLogProcessor") \
    .getOrCreate()

# Kafka configuration
kafka_broker = "kafka:9093"  # Internal Kafka address in Docker
topic = "logs-topic"  # Kafka topic

# Postgres configuration
pg_url = "jdbc:postgresql://postgres:5432/airflow"  # Internal Docker network
pg_properties = {
    "user": "airflow",
    "password": "airflow",
    "driver": "org.postgresql.Driver"
}

# Define Schema for Logs
log_schema = StructType() \
    .add("timestamp", StringType()) \
    .add("log_level", StringType()) \
    .add("log_type", StringType()) \
    .add("message", StringType())

# 1. Read from Kafka
kafka_stream = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", kafka_broker) \
    .option("subscribe", topic) \
    .option("startingOffsets", "earliest") \
    .load()

# 2. Parse and Structure the Kafka Stream
logs = kafka_stream \
    .select(from_json(col("value").cast("string"), log_schema).alias("data")) \
    .select("data.*") \
    .withColumn("timestamp_parsed", to_timestamp(col("timestamp"), "yyyy-MM-dd HH:mm:ss")) \
    .drop("timestamp")  # Drop the raw string timestamp column

# Rename `timestamp_parsed` to `timestamp` to match Postgres schema
logs = logs.withColumnRenamed("timestamp_parsed", "timestamp")

# 3. Write All Logs to Postgres
def write_all_logs_to_postgres(batch_df, batch_id):
    """Write all logs to Postgres database."""
    batch_df.write \
        .jdbc(url=pg_url, table="all_logs", mode="append", properties=pg_properties)

# Stream Processing: Write all logs to Postgres
query = logs.writeStream \
    .foreachBatch(write_all_logs_to_postgres) \
    .outputMode("append") \
    .start()

# 4. Filter `ERROR` Logs for Alerting
error_logs = logs.filter(col("log_level") == "ERROR")

# Optional: Process ERROR logs for additional actions
def process_error_logs(batch_df, batch_id):
    """Process filtered ERROR logs."""
    error_count = batch_df.count()
    print(f"Batch ID: {batch_id}, ERROR count: {error_count}")
    if error_count >= 10:  # Example threshold
        print(f"ALERT! {error_count} ERROR logs detected!")

# Real-Time Alert Processing
error_logs_query = error_logs.writeStream \
    .foreachBatch(process_error_logs) \
    .outputMode("append") \
    .start()

# Keep the Stream Running
spark.streams.awaitAnyTermination()