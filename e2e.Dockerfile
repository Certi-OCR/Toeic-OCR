FROM python:3.12-slim

# Install system dependencies
RUN apt update && \
    apt install -y htop libgl1-mesa-glx libglib2.0-0

# Copy requirements and install Python dependencies
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Set working directory
WORKDIR /app

# Copy application code
COPY . /app

# Expose the port
EXPOSE 8000

# Set the command to run the application with Gunicorn and Uvicorn workers
CMD ["uvicorn main:app --host 0.0.0.0 --port $PORT"]