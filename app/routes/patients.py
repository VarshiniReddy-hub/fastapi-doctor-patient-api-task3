from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app import models
from app.schemas import PatientCreate, PatientUpdate
from app.services import (
    create_patient,
    get_patient,
    update_patient,
    delete_patient
)
from app.auth import get_current_user


router = APIRouter(
    prefix="/patients",
    tags=["Patients"]
)


@router.post("/")
def add_patient(
    patient: PatientCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    return create_patient(db, patient)


@router.get("/")
def get_patients(
    age_gt: Optional[int] = Query(None, gt=0),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    db: Session = Depends(get_db)
):
    query = db.query(models.Patient)

    if age_gt is not None:
        query = query.filter(
            models.Patient.age > age_gt
        )

    total = query.count()

    patients = query.offset(
        (page - 1) * limit
    ).limit(limit).all()

    return {
        "total": total,
        "current_page": page,
        "limit": limit,
        "data": patients
    }


@router.get("/{patient_id}")
def get_patient_by_id(
    patient_id: int,
    db: Session = Depends(get_db)
):
    return get_patient(db, patient_id)


@router.put("/{patient_id}")
def update_patient_details(
    patient_id: int,
    patient: PatientUpdate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    return update_patient(db, patient_id, patient)


@router.patch("/{patient_id}")
def patch_patient(
    patient_id: int,
    patient: PatientUpdate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    return update_patient(db, patient_id, patient)


@router.delete("/{patient_id}")
def delete_patient_by_id(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    return delete_patient(db, patient_id)