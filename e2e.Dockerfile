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

ENV PORT=8000

# # Expose the port
EXPOSE $PORT

# Set the command to run the application with Gunicorn and Uvicorn workers
CMD gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app --host 0.0.0.0 --port $PORT