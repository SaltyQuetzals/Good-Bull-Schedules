FROM python:3.6-slim
WORKDIR /app
COPY requirements.txt /app
COPY goodbullschedules /app
RUN pip install -r requirements.txt