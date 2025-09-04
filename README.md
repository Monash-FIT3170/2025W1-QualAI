# 2025W1-QualAI
QualAI is an AI-Powered Qualitative Research Assistant, augmenting human analysis by providing researchers with an offline toolkit capable of thematic analysis 
## Features 
* A file manager to upload audio files and convert into transcripts
* A chatbot capable of thematic analysis
* A text editor to update generated scripts
* Fully offline for security

## Set-up Guide  
### Software Requirements
This project uses **Docker** (required) to containerise all dependencies, including:  
* **Flask** backend
* **Mongodb** database
* **Neo4j** vector database
* **React** frontend
* **Ollama** LLM 
### Recommended Hardware 
* Minimum 8GB RAM 
* 10GB free disk space
* GPU (*highly*) recommended 

### Installation 
1. Clone the repository 
```bash
git clone https://github.com/Monash-FIT3170/2025W1-QualAI.git
cd 2025W1-QualAI
```

### Usage
```bash
docker-compose up
```
*Note*: This will likely take a long time (upwards of 30 minutes) on first run as dependencies are built/downloaded.

## Running the Project
* Once started, the application should be available on
http://localhost:5173

## Common Issues
* Slow first build: First build may take upwards of 30 minutes due to large image dependencies 

## Additional Notes for Developers
### Project Structure:
- **/frontend** – React frontend application  
- **/backend** – Flask API backend  
  - **/upload** – Handles file uploads  
  - **/mongodb** – Manages MongoDB connection  
  - **/editor** – Handles file editing and removal  
  - **/chat** – Chatbot functionality & DeepSeek integration  
  - **/database_client** – Manages Neo4j connection
### Future Development Plans
* Multiple project support
* Live file updating
* Chatbot history
* In application user guides
* Improved Qualitative Analysis

### Testing 
* Test files are located in the test folder
  
# Contributors 
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

