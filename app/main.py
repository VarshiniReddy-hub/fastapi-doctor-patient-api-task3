import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app import models
from app.routes import doctors, patients, auth


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


Base.metadata.create_all(bind=engine)


app = FastAPI(title="Doctor Patient API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
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


@app.get("/")
def root():
    logger.info("Root API endpoint accessed")
    return {"message": "Doctor Patient API is running"}