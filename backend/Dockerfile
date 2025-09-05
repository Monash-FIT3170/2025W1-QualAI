FROM python:3.10-slim

WORKDIR /app

# Install ffmpeg and dependencies
RUN apt-get update && \
    apt-get install -y ffmpeg curl git gcc g++ make && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN python -m spacy download en_core_web_sm

# Create a virtual environment for whisper dependencies
RUN python -m venv /opt/venv

# Get whisper-diarization requirements
COPY upload/whisper-diarization/requirements.txt whisper-requirements.txt
COPY upload/whisper-diarization/constraints.txt whisper-constraints.txt

# Install whisper dependencies inside the venv in one RUN command
RUN /bin/bash -c "source /opt/venv/bin/activate && \
    pip install --upgrade pip && \
    pip install -r whisper-requirements.txt -c whisper-constraints.txt"

COPY . .


EXPOSE 5001

CMD ["bash", "start.sh"]