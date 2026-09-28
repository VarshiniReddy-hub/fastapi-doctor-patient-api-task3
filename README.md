# FastAPI Doctor Patient API - Task 3

This project is an enhanced version of the Doctor Patient API developed using FastAPI.

The project includes doctor and patient management, database integration, authentication, validation, filtering, pagination, testing, and other production-level improvements.

## Technologies Used

- Python
- FastAPI
- Pydantic
- SQLAlchemy
- SQLite
- JWT Authentication
- Uvicorn
- Pytest
- Docker

## Features

- Doctor management
- Patient management
- Doctor-Patient relationship
- Assign patients to doctors
- Doctor CRUD operations
- Patient CRUD operations
- Soft delete for doctors
- Email validation
- Phone number validation
- Unique doctor email validation
- Filtering
- Pagination
- SQLite database
- SQLAlchemy ORM
- JWT authentication
- API versioning
- Logging
- CORS
- Environment variables
- Docker support
- Unit testing using pytest

## Project Structure

```text
Task3/
│
├── app/
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── doctors.py
│   │   └── patients.py
│   │
│   ├── __init__.py
│   ├── auth.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   └── services.py
│
├── tests/
│   └── test_api.py
│
├── SCREENSHOTS/
│
├── .env
├── .gitignore
├── Dockerfile
├── pytest.ini
├── requirements.txt
└── README.md