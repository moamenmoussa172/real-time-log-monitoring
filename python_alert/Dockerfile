# Use the official Python base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the script and requirements into the container
COPY . /app

# Install required system libraries and Python dependencies
RUN apt-get update && apt-get install -y gcc libpq-dev && \
    pip install --no-cache-dir kafka-python psycopg2 && \
    pip install --no-cache-dir --upgrade pip

# Default command
CMD ["python", "alert_script.py"]