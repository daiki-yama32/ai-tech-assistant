# AI Technical Assistant

Technical documentation AI assistant using OpenAI API, File Search, FastAPI, and SQLite.

## Overview

AI Technical Assistant is an AI-powered application that allows users to ask questions about technical documents.

The application uses OpenAI File Search to retrieve relevant information from a technical document and generates an answer based on the retrieved content.

User questions and AI-generated answers are also stored in a SQLite database and can be retrieved through the history API.

## Features

* Ask questions about technical documents
* Search documents using OpenAI File Search
* Generate answers using OpenAI Responses API
* Store question and answer history in SQLite
* Retrieve previous questions and answers
* Validate empty questions
* Handle API errors
* Display token usage for each request
* Run the application with Docker

## System Architecture

```text
User
  │
  ▼
FastAPI
  │
  ▼
/ask
  │
  ▼
OpenAI Responses API
  │
  ├── File Search
  │      │
  │      ▼
  │   Vector Store
  │      │
  │      ▼
  │   Technical Document
  │
  ▼
AI-generated Answer
  │
  ▼
SQLite
  │
  ▼
/history
```

## Technologies

| Technology         | Purpose                              |
| ------------------ | ------------------------------------ |
| Python             | Application development              |
| FastAPI            | REST API                             |
| OpenAI API         | AI response generation               |
| OpenAI File Search | Technical document search            |
| Vector Store       | Storage for searchable document data |
| SQLite             | Question and answer history          |
| Docker             | Application containerization         |
| Git / GitHub       | Version control                      |

## Project Structure

```text
ai-tech-assistant/
│
├── app/
│   ├── __init__.py
│   ├── database.py
│   └── main.py
│
├── documents/
│   └── .gitkeep
│
├── tests/
│   └── .gitkeep
│
├── technical_document.pdf
├── test.db
├── Dockerfile
├── requirements.txt
├── upload_file.py
├── test_database.py
├── test_file_search.py
├── test_openai.py
├── .dockerignore
├── .gitignore
└── README.md
```

## API Endpoints

### POST `/ask`

Send a question to the AI assistant.

Example:

```json
{
  "question": "モーターの最大回転数は何rpmですか？"
}
```

The API returns the question, AI-generated answer, model information, and token usage.

### GET `/history`

Returns previously stored questions and answers from the SQLite database.

## Database

The application uses SQLite to store question and answer history.

The `questions` table contains:

```text
id
question
answer
created_at
```

Questions and answers are stored automatically when `/ask` successfully generates a response.

## Error Handling

The application validates user input before sending the request to OpenAI.

For example, an empty question returns:

```text
HTTP 400 Bad Request
```

Unexpected errors during AI processing return:

```text
HTTP 500 Internal Server Error
```

## Environment Variables

Create a `.env` file in the project root.

```text
OPENAI_API_KEY=your_api_key
VECTOR_STORE_ID=your_vector_store_id
```

Do not commit the `.env` file to GitHub.

## Local Setup

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd ai-tech-assistant
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

Windows Git Bash:

```bash
source .venv/Scripts/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure environment variables

Create a `.env` file and add:

```text
OPENAI_API_KEY=your_api_key
VECTOR_STORE_ID=your_vector_store_id
```

### 6. Start the application

```bash
uvicorn app.main:app --reload
```

The API documentation is available at:

```text
http://127.0.0.1:8000/docs
```

## Run with Docker

Build the Docker image:

```bash
docker build -t ai-tech-assistant .
```

Run the container:

```bash
docker run -p 8000:8000 --env-file .env ai-tech-assistant
```

Then open:

```text
http://127.0.0.1:8000/docs
```

## Example

A user asks:

```text
モーターの最大回転数は何rpmですか？
```

The AI searches the technical document using File Search and generates an answer based on the retrieved information.

The question and answer are then stored in SQLite.

## Future Improvements

The following features are planned for future versions:

* Web-based user interface
* Display RAG citation sources
* Web-based conversation history
* Improved error handling
* Better user experience
* Additional technical documents
* More comprehensive automated tests

## Project Goal

This project was developed as a practical exercise in building an AI application using Python and modern AI technologies.

The project covers the complete development flow from API development and database integration to RAG-based document search and Docker containerization.
