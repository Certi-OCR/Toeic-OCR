FROM python:3.12-slim

RUN apt update && \
    apt install -y htop libgl1-mesa-glx libglib2.0-0

WORKDIR /app

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY . .

CMD [ "gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8000" ]
