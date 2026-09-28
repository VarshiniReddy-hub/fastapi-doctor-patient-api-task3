from typing import Optional

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app import models
from app.schemas import DoctorCreate, DoctorUpdate
from app.services import (
    create_doctor,
    get_doctor,
    update_doctor,
    delete_doctor
)
from app.auth import get_current_user


router = APIRouter(
    prefix="/doctors",
    tags=["Doctors"]
)


@router.post("/")
def add_doctor(
    doctor: DoctorCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    return create_doctor(db, doctor)


@router.get("/")
def get_doctors(
    specialization: Optional[str] = None,
    is_active: Optional[bool] = None,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    db: Session = Depends(get_db)
):
    query = db.query(models.Doctor)

    if specialization:
        query = query.filter(
            models.Doctor.specialization.ilike(specialization)
        )

    if is_active is not None:
        query = query.filter(
            models.Doctor.is_active == is_active
        )

    total = query.count()

    doctors = query.offset(
        (page - 1) * limit
    ).limit(limit).all()

    return {
        "total": total,
        "current_page": page,
        "limit": limit,
        "data": doctors
    }


@router.get("/{doctor_id}/patients")
def get_doctor_patients(
    doctor_id: int,
    db: Session = Depends(get_db)
):
    doctor = db.query(models.Doctor).filter(
        models.Doctor.id == doctor_id
    ).first()

    if not doctor:
        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
        )

    if not doctor.is_active:
        raise HTTPException(
            status_code=400,
            detail="Doctor is inactive"
        )

    return db.query(models.Patient).filter(
        models.Patient.doctor_id == doctor_id
    ).all()


@router.get("/{doctor_id}")
def get_doctor_by_id(
    doctor_id: int,
    db: Session = Depends(get_db)
):
    return get_doctor(db, doctor_id)


@router.put("/{doctor_id}")
def update_doctor_details(
    doctor_id: int,
    doctor: DoctorUpdate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    return update_doctor(db, doctor_id, doctor)


@router.patch("/{doctor_id}")
def patch_doctor(
    doctor_id: int,
    doctor: DoctorUpdate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    return update_doctor(db, doctor_id, doctor)


@router.delete("/{doctor_id}")
def delete_doctor_by_id(
    doctor_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    return delete_doctor(db, doctor_id)