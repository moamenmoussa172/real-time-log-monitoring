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
