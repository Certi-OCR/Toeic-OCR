FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
COPY . /app
RUN apt-get update -y && apt-get install -y ffmpeg libsm6 libxext6 libglib2.0-0 
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8501
CMD ["streamlit", "run", "app/main.py"]
