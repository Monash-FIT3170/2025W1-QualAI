# 2025W1-QualAI

## 1. Project Overview

QualAI is an AI-Powered Qualitative Research Assistant, augmenting human analysis by providing researchers with an offline toolkit capable of thematic analysis.

The tool streamlines the research workflow by automating transcriptions, facilitating in-depth analysis and enabling the extraction of insights from interview data. It does this using speech-to-text transcription, semantic analysis, and live text editing.

This project is open-source. It was initally developeed as a part of Monash FIT3170 - "Software Engineering Practice".

## 2. Features

### 2.1 Key Features

- A file manager to upload audio files and convert into transcripts
- A chatbot capable of thematic analysis
- A text editor to update generated scripts
- Fully offline for security

### 2.2 Epics

- Add here table with each epic, its description and status

## 3. Set-up Guide

### 3.1 Software Requirements

This project uses **Docker** (required) to containerise all dependencies, including:

- **Flask** backend
- **Mongodb** database
- **Neo4j** vector database
- **React** frontend
- **Ollama** LLM

### 3.2 Recommended Hardware

- Minimum 8GB RAM
- 10GB free disk space
- GPU (_highly_) recommended

### 3.3 Installation

1. Clone the repository

```bash
git clone https://github.com/Monash-FIT3170/2025W1-QualAI.git
cd 2025W1-QualAI
```

2. Environment variables

### 3.4 Usage

```bash
docker-compose up
```

_Note_: This will likely take a long time (upwards of 30 minutes) on first run as dependencies are built/downloaded.

Once started, the application should be available on
http://localhost:5173

## 4. Common Issues & Troubleshooting

### 4.1 Issues

- Slow first build: First build may take upwards of 30 minutes due to large image dependencies
- Local dependency issues: Dependencies can be hard to manage due to the large number within the project. Utilising Docker can reduce these issues.

### 4.2 Known Bugs

## 5. Additional Notes for Developers

### 5.1 Source Coded

Git repository found [here](https://github.com/Monash-FIT3170/2025W1-QualAI/).

### 5.2 Project Structure:

- **/frontend** – React frontend application
- **/backend** – Flask API backend
  - **/upload** – Handles file uploads
  - **/mongodb** – Manages MongoDB connection
  - **/editor** – Handles file editing and removal
  - **/chat** – Chatbot functionality & DeepSeek integration
  - **/database_client** – Manages Neo4j connection

### 5.3 Technical Documentation

- where to find technical documentation

### 5.4 Outstanding tasks

### 5.5 Future Development Plans

- Multiple project support
- Live file updating
- Chatbot history
- In application user guides
- Improved Qualitative Analysis

### 5.6 Testing

- set up of CI/CD
- Test files are located in the test folder

### 5.7 Security and Privacy Compliance

A security and privacy audit has been completed for the project. This document can be found [here](https://drive.google.com/file/d/1Yc7g50En0GwmHXwVwVaX5X9ZgGpk5ELg/view?usp=sharing)

## 6. Contributors

### 6.1 Main Contact Person

Any enquiries should be referred to Felix Chung at fchu0006@student.monash.edu

### 6.2 Developers

Felix Chung: fchu0006@student.monash.edu\
Terence Bai: tbai0012@student.monash.edu\
Jonathan Farrand: jfar0026@student.monash.edu\
Kays Beslen: kbes0005@student.monash.edu\
Kade Lucy: kluc0006@student.monash.edu\
Luka Boskovic: lbos0001@student.monash.edu\
Rohan Shetty: rshe0040@student.monash.edu\
Duleesha Gunaratne: dgun0024@student.monash.edu\
Rachana Devi: rdev0023@student.monash.edu\
Jaemin Park: jpar0073@student.monash.edu\
Gunni Singh: gsin0055@student.monash.edu
