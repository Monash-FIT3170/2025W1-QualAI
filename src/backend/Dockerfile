FROM python:3.10-slim

WORKDIR /app

ARG FRONTEND_PORT
ENV PORT=$FRONTEND_PORT

# Install ffmpeg and dependencies
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE $PORT

CMD ["python", "app.py"]
