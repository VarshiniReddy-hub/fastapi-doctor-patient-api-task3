from typing import Optional

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app import models
from app.schemas import PatientCreate, PatientUpdate
from app.auth import get_current_user, require_admin


router = APIRouter(
    prefix="/patients",
    tags=["Patients"]
)


@router.post("/")
def add_patient(
    patient: PatientCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    doctor = db.query(models.Doctor).filter(
        models.Doctor.id == patient.doctor_id
    ).first()

    if not doctor:
        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
        )

    if not doctor.is_active:
        raise HTTPException(
            status_code=400,
            detail="Cannot assign patient to an inactive doctor"
        )

    new_patient = models.Patient(
        name=patient.name,
        age=patient.age,
        phone=patient.phone,
        doctor_id=patient.doctor_id
    )

    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)

    return new_patient


@router.get("/")
def get_patients(
    age_gt: Optional[int] = Query(None, gt=0),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    query = db.query(models.Patient)

    if current_user["role"] == "doctor":
        query = query.filter(
            models.Patient.doctor_id == current_user["doctor_id"]
        )

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
        "page": page,
        "limit": limit,
        "data": patients
    }


@router.get("/{patient_id}")
def get_patient_by_id(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    patient = db.query(models.Patient).filter(
        models.Patient.id == patient_id
    ).first()

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    if current_user["role"] == "doctor":
        if patient.doctor_id != current_user["doctor_id"]:
            raise HTTPException(
                status_code=403,
                detail="You can only view your assigned patients"
            )

    return patient


@router.put("/{patient_id}")
def update_patient_details(
    patient_id: int,
    patient: PatientCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    existing_patient = db.query(models.Patient).filter(
        models.Patient.id == patient_id
    ).first()

    if not existing_patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    doctor = db.query(models.Doctor).filter(
        models.Doctor.id == patient.doctor_id
    ).first()

    if not doctor:
        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
        )

    if not doctor.is_active:
        raise HTTPException(
            status_code=400,
            detail="Cannot assign patient to an inactive doctor"
        )

    existing_patient.name = patient.name
    existing_patient.age = patient.age
    existing_patient.phone = patient.phone
    existing_patient.doctor_id = patient.doctor_id

    db.commit()
    db.refresh(existing_patient)

    return existing_patient


@router.patch("/{patient_id}")
def patch_patient(
    patient_id: int,
    patient: PatientUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    existing_patient = db.query(models.Patient).filter(
        models.Patient.id == patient_id
    ).first()

    if not existing_patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    update_data = patient.model_dump(exclude_unset=True)

    if "doctor_id" in update_data:
        doctor = db.query(models.Doctor).filter(
            models.Doctor.id == update_data["doctor_id"]
        ).first()

        if not doctor:
            raise HTTPException(
                status_code=404,
                detail="Doctor not found"
            )

        if not doctor.is_active:
            raise HTTPException(
                status_code=400,
                detail="Cannot assign patient to an inactive doctor"
            )

    for key, value in update_data.items():
        setattr(existing_patient, key, value)

    db.commit()
    db.refresh(existing_patient)

    return existing_patient


@router.delete("/{patient_id}")
def delete_patient_by_id(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    patient = db.query(models.Patient).filter(
        models.Patient.id == patient_id
    ).first()

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    db.delete(patient)
    db.commit()

    return {
        "message": "Patient deleted successfully"
    }