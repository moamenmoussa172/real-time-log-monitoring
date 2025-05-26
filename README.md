# Real-Time Log Monitoring and Alerting System 🚀  

This repository contains the implementation of a **Real-Time Data Pipeline** for monitoring application logs. This project was developed as part of the **Data Engineering Track at IWD - Data & Tech in Action** and demonstrates the integration of multiple tools and technologies for real-time log processing, alerting, and orchestration.  

---

## 📋 **Project Overview**  

The objective of this project is to build a real-time data pipeline capable of:  
- **Monitoring application logs** in real-time for an e-commerce platform.  
- **Raising alerts** when error thresholds or specific patterns are detected.  
- **Storing and processing structured log data** for further analysis.  

The entire pipeline is **containerized using Docker**, ensuring portability and smooth deployment.

---

## 🎯 **Key Features**  

1️⃣ **Log Producer**  
   - A Python script to simulate application logs (INFO, WARNING, ERROR) and publish them to a Kafka topic in real-time.  

2️⃣ **Kafka Pipeline**  
   - Created a Kafka topic (`logs-topic`) to ingest and stream logs seamlessly.  

3️⃣ **PySpark Streaming Application**  
   - Consumed logs from Kafka, parsed them into structured format (`timestamp`, `log_level`, `log_type`, `message`).  
   - Filtered `ERROR` logs and stored all logs in a PostgreSQL database for analysis.  

4️⃣ **Alerting System**  
   - A Python script that monitors PostgreSQL for `ERROR` logs and triggers **alerts** (console or file-based) if the number of errors exceeds a threshold (e.g., 10 errors in 5 minutes).  

5️⃣ **Airflow Orchestration**  
     - Built an Airflow **DAG** to automate:  
     - Log generation using the producer.  
     - Log processing using the PySpark application.  
     - Real-time alert monitoring.
     - Cleanup of old logs in PostgreSQL.  

6️⃣ **Docker Integration**  
   - **Dockerized** all components (Kafka, Zookeeper, PySpark, PostgreSQL, Airflow) for seamless deployment and scalability.

## 🛠️ **Technologies Used**  

- **Kafka**: Real-time ingestion of logs.  
- **PySpark**: Processing and transforming log data.  
- **PostgreSQL**: Storing the structured logs.  
- **Python**: Scripting for log generation and alerting.  
- **Airflow**: Orchestrating and scheduling the pipeline.  
- **Docker**: Containerizing the entire pipeline for portability and ease of deployment.  

---

## 📂 **Project Structure**  

├── airflow/ # Airflow DAGs and configuration files
├── kafka/ # Kafka setup and configuration
├── pyspark/ # PySpark streaming application
├── producer/ # Log producer Python script
├── alerting/ # Alerting Python script
├── docker-compose.yml # Docker Compose file for the entire pipeline
├── README.md # Project documentation
└── requirements.txt # Python dependencies


## ⚙️ **Setup Instructions**  

Follow the steps below to set up the project locally:

1. Clone the Repository**  
bash
```git clone https://github.com/your-username/real-time-log-monitoring.git```
```cd real-time-log-monitoring```

2. Install Prerequisites
Make sure you have the following installed on your system:

Docker
Docker Compose
3. Start the Pipeline
Run the following command to start all services using Docker Compose:
docker-compose up -d

This will spin up the following services:

   Kafka
   Zookeeper
   PostgreSQL
   Airflow
   PySpark

4. Access Services
   Airflow Web UI: http://localhost:8080 (default login: airflow / airflow)
   PostgreSQL: localhost:5432 (default user: airflow, password: airflow)
   Kafka Broker: localhost:9093
   
5. Run the Pipeline
   Trigger the Airflow DAG to start the pipeline:
   Log producer
   PySpark log processing
   Alerting system

📝 How the Pipeline Works
   1. Log Producer
      Simulates logs (INFO, WARNING, ERROR) and streams them to logs-topic in Kafka.
   2. Kafka Pipeline
      Streams logs to the PySpark application for processing.
   3. PySpark Streaming Application
      Parses logs into a structured format and stores them in PostgreSQL.
   4. Alerting System
      Monitors PostgreSQL and raises alerts if error thresholds are exceeded.
   5. Airflow Orchestration
      Automates the entire pipeline, including log cleanup tasks.
📊 Example Use Case
Imagine an e-commerce platform that generates logs like:
   {"timestamp": "2025-05-25 12:00:00", "log_level": "ERROR", "log_type": "Payment", "message": "Payment failed"}
   {"timestamp": "2025-05-25 12:01:00", "log_level": "INFO", "log_type": "Server", "message": "Server is running"}

The pipeline will:
   Parse these logs and store them in PostgreSQL.
   Raise an alert if more than 10 ERROR logs occur within 5 minutes.
       
