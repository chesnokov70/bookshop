FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN apt-get update && \
    apt-get install -y postgresql-client && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]
