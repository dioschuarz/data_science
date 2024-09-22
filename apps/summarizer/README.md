# Wikipedia Summarizer API

## Overview

The **Wikipedia Summarizer API** is a FastAPI-based application that allows users to generate summaries of Wikipedia articles. The application supports both synchronous and asynchronous database operations and leverages advanced language models to produce concise summaries.

## Features

- **Insert Wikipedia Articles**: Submit a Wikipedia URL to generate and store a summary.
- **Retrieve Summaries**: Fetch the summary of a Wikipedia article using a unique identifier.
- **Asynchronous Operations**: Efficient handling of database operations using asynchronous programming.
- **Language Model Integration**: Utilizes advanced language models for generating high-quality summaries.

## Table of Contents

- Installation
- Usage
- API Endpoints
- Project Structure
- Configuration
- Running Tests
- Contributing
- License

## Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/yourusername/wikipedia-summarizer-api.git
    cd wikipedia-summarizer-api
    ```

2. **Create and activate a virtual environment**:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

4. **Set up environment variables**:
    Create a `.env` file in the root directory and add the following:
    ```env
    POSTGRES_DB_URL=your_postgres_db_url
    GOOGLE_API_KEY=your_google_api_key
    FASTAPI_URL=http://your_host:your_port/summarizer
    ```

## Usage

1. **Run the FastAPI application**:
    ```sh
    uvicorn app.main:app --reload
    ```

2. **Access the API documentation**:
    Open your browser and navigate to `http://127.0.0.1:8000/docs` to view the interactive API documentation.

## API Endpoints

### Insert Article

- **Endpoint**: `/summarizer/insert_article`
- **Method**: `POST`
- **Description**: Inserts a Wikipedia article and generates a summary.
- **Request Body**:
    ```json
    {
        "wikipedia_url": "https://en.wikipedia.org/wiki/Nikola_Tesla",
        "number_of_words": 1000
    }
    ```
- **Response**:
    ```json
    {
        "id": "unique-identifier",
        "info": "Data inserted successfully",
        "warning": "You configured the number of words below 1000, the lowest value of this parameter is 1000."
    }
    ```

### Get Summary

- **Endpoint**: `/summarizer/get_summary/{uuid}`
- **Method**: `GET`
- **Description**: Retrieves the summary of a Wikipedia article using a unique identifier.
- **Response**:
    ```json
    {
        "uuid": "unique-identifier",
        "summary": "The summary text of the Wikipedia article."
    }
    ```

## Project Structure
```
summarizer/
│
├── .vscode/
│   └── launch.json
├── backend/
│   ├── routes/
│   ├── app/
│   │   ├── api/
│   │   │   ├── routes/
│   │   │   │   ├── init.py
│   │   │   │   └── summarizer.py
│   │   │   ├── init.py
│   │   │   └── main.py
│   │   ├── build/
│   │   │   ├── chains/
│   │   │   │   ├── init.py
│   │   │   │   ├── map.py
│   │   │   │   └── reduce.py
│   │   │   ├── graphs/
│   │   │   │   ├── init.py
│   │   │   │   ├── edges.py
│   │   │   │   ├── nodes.py
│   │   │   │   ├── states.py
│   │   │   │   └── workflow.py
│   │   │   ├── init.py
│   │   │   ├── loader.py
│   │   │   └── models.py
│   │   ├── tests/
│   │   │   ├── init.py
│   │   │   ├── test_routes.py
│   │   │   └── test_utils.py
│   │   ├── utils/
│   │   │   ├── init.py
│   │   │   ├── async_db_connection.py
│   │   │   ├── config.py
│   │   │   ├── functions.py
│   │   │   └── sync_db_connection.py
│   │   ├── init.py
│   │   └── main.py
│   ├── db/
│   │   ├── docker-compose.yaml
│   │   ├── Dockerfile
│   │   └── init.sql
│   ├── Dockerfile
│   ├── poetry.lock
│   └── pyproject.toml
├── docs/
├── frontend/
│   ├── init.py
│   ├── Dockerfile
│   ├── poetry.lock
│   ├── pyproject.toml
│   └── streamlit_app.py
├── .env
├── .gitignore
├── docker-compose.yaml
├── requirements.txt
└── README.md
```

## Configuration

- **POSTGRES_DB_URL**: The URL for your PostgreSQL database.
  - Expected entry is something like: 
    - `://user:password@host:port/wiki_summarizer`
- **GOOGLE_API_KEY**: The API key for accessing Google services.

## Application Preview

![Fig1](/figs/app_example.png)

## Running Tests

1. **Install test dependencies**:
    ```sh
    pip install pytest httpx
    ```

2. **Run the tests**:
    ```sh
    pytest
    ```

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add new feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Open a Pull Request.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

