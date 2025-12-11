FROM python:3.11-slim
WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY bot.py ./
COPY README.md ./

ENV PYTHONUNBUFFERED=1

# create persistent data directory for state
RUN mkdir -p /data && chown 1000:1000 /data || true

VOLUME ["/data"]

CMD ["python", "bot.py"]
