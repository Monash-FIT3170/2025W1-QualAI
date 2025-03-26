#!/bin/bash

# Install all package dependencies listed within requirements.txt.
pip install -r resources/requirements.txt

# Check the name of the python executable.
PYTHON=$(command -v python3 || command -v python)

# Download the spaCy language model that the sentence_transformer spike utilises.
$PYTHON -m spacy download en_core_web_sm
