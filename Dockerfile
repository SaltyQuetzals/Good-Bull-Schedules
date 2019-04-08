FROM python:3.6-slim
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY requirements.txt /app
COPY goodbullschedules /app
COPY docker-entrypoint.sh /usr/local/bin
RUN pip install -r requirements.txt
ENTRYPOINT ["docker-entrypoint.sh"]