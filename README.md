# Doctor Patient Management API

A FastAPI backend application for managing doctors, patients, authentication, and appointments.

## Technologies Used

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- JWT Authentication
- Pytest
- Uvicorn

## Features

### Authentication
- JWT based login
- Role-based authorization
- Admin and Doctor roles

### Doctor Management
- Add doctor
- View doctors
- View doctor by ID
- Update doctor
- Patch doctor details
- Delete doctor
- Filter doctors by specialization and active status
- Pagination support

### Patient Management
- Add patient
- View patients
- View patient by ID
- Update patient
- Patch patient details
- Delete patient
- Doctors can view their assigned patients

### Appointment Management
- Create appointments
- View appointments
- View appointment by ID
- Update appointments
- Delete appointments
- View appointments by doctor
- View appointments by patient
- Validate doctor and patient
- Prevent appointments for inactive doctors
- Prevent overlapping appointments

### Data Integrity
- Unique doctor email
- Foreign key relationships
- Database error handling
- Meaningful API error messages

### Testing
- API tests using Pytest
- Authentication testing
- Protected API testing
- Doctor API testing
- Patient API testing

## Project Structure

```text
Task3/
│
├── app/
│   ├── __init__.py
│   ├── auth.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── services.py
│   │
│   └── routes/
│       ├── __init__.py
│       ├── auth.py
│       ├── doctors.py
│       ├── patients.py
│       └── appointments.py
│
├── tests/
│   └── test_api.py
│
├── SCREENSHOTS/
│
├── .gitignore
├── pytest.ini
├── requirements.txt
└── README.md