# DelTorCarInc — source-based container
FROM python:3.11-slim

# Quality-of-life env
ENV TZ=Pacific/Auckland \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Optional but nice
RUN apt-get update && apt-get install -y --no-install-recommends tzdata && \
    useradd -m -u 10001 appuser && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# If you have real deps, keep this; else comment out both COPY/RUN lines.
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install --no-cache-dir -r /app/requirements.txt || true

# Copy the project
COPY . /app

# Writable location for SQLite DB/logs/artifacts
RUN mkdir -p /data && chown -R appuser:appuser /data
VOLUME ["/data"]

# Expose multiple env var names so existing code keeps working
ENV DELTORCARINC_DB_PATH=/data/deltorcarinc.sqlite
ENV DELTORCARS_DB_PATH=/data/deltorcarinc.sqlite

USER appuser

# Run your launcher (run.py is at /app/run.py)
ENTRYPOINT ["python", "-u", "run.py"]

