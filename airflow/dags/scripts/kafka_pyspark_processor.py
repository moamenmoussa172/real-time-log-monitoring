from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StringType
from pyspark.sql.functions import col, from_json, to_timestamp
import time

# Initialize Spark Session
spark = SparkSession.builder \
    .appName("KafkaLogProcessor") \
    .getOrCreate()

# Kafka configuration
kafka_broker = "kafka:9093"
topic = "logs-topic"

# PostgreSQL configuration
pg_url = "jdbc:postgresql://postgres:5432/airflow"
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

# Rename `timestamp_parsed` to `timestamp`
logs = logs.withColumnRenamed("timestamp_parsed", "timestamp")

# 3. Write All Logs to PostgreSQL
def write_all_logs_to_postgres(batch_df, batch_id):
    """Write all logs to Postgres database."""
    batch_df.write \
        .jdbc(url=pg_url, table="all_logs", mode="append", properties=pg_properties)

# Stream Processing: Write all logs to PostgreSQL
query = logs.writeStream \
    .foreachBatch(write_all_logs_to_postgres) \
    .outputMode("append") \
    .start()

# 4. Run Streaming for 10 Seconds and Stop
try:
    print("Running streaming queries for 10 seconds...")
    time.sleep(10)  # Allow the queries to process for 10 seconds

    # Stop the streaming queries
    query.stop()
    print("Stopped streaming queries after 10 seconds.")

except Exception as e:
    print(f"Error occurred: {e}")

finally:
    # Ensure all Spark resources are released
    for active_query in spark.streams.active:
        active_query.stop()
    spark.stop()
    print("Spark session stopped.")