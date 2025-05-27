FROM python:3.10-slim

WORKDIR /app

# Install ffmpeg and dependencies
RUN apt-get update && \
    apt-get install -y ffmpeg curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN python -m spacy download en_core_web_sm

COPY . .

EXPOSE 5001

CMD ["bash", "start.sh"]