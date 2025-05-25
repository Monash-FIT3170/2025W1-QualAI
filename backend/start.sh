#!/bin/bash

set -e

curl -X POST http://ollama:11434/api/pull -d '{"name": "deepseek-r1:1.5b"}'

echo "Starting backend..."
exec python app.py
