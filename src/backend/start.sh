#!/bin/bash

set -e

curl -X POST http://localhost:11434/api/pull -d '{"name": "deepseek-coder:1.3b"}' || echo "Model already pulled"

echo "Starting backend..."
exec python app.py
