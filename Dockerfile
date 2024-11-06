FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
COPY . /app
RUN apt-get update && apt-get install -y libgl1-mesa-glx
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8501
CMD ["streamlit", "run", "app/main.py"]
