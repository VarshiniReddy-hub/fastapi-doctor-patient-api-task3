from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.auth import create_access_token


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):

    # Admin login
    if (
        form_data.username == "admin"
        and form_data.password == "admin123"
    ):
        access_token = create_access_token(
            username="admin",
            role="admin"
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "role": "admin"
        }

    # Doctor login
    if (
        form_data.username == "doctor"
        and form_data.password == "doctor123"
    ):
        access_token = create_access_token(
            username="doctor",
            role="doctor",
            doctor_id=1
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "role": "doctor"
        }

    raise HTTPException(
        status_code=401,
        detail="Incorrect username or password"
    )