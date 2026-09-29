from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app import models

from app.routes import auth
from app.routes import doctors
from app.routes import patients
from app.routes import appointments


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Doctor Patient API",
    version="0.1.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(
    auth.router,
    prefix="/api/v1"
)

app.include_router(
    doctors.router,
    prefix="/api/v1"
)

app.include_router(
    patients.router,
    prefix="/api/v1"
)

app.include_router(
    appointments.router,
    prefix="/api/v1"
)


@app.get("/")
def root():
    return {
        "message": "Doctor Patient API is running"
    }