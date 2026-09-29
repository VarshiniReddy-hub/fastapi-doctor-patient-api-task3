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
from app.auth import get_current_user, require_admin


router = APIRouter(
    prefix="/doctors",
    tags=["Doctors"]
)


@router.post("/")
def add_doctor(
    doctor: DoctorCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    return create_doctor(db, doctor)


@router.get("/")
def get_doctors(
    specialization: Optional[str] = Query(None),
    is_active: Optional[bool] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    query = db.query(models.Doctor)

    if specialization:
        query = query.filter(
            models.Doctor.specialization.ilike(
                f"%{specialization}%"
            )
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
        "page": page,
        "limit": limit,
        "data": doctors
    }


@router.get("/{doctor_id}")
def get_doctor_by_id(
    doctor_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    doctor = get_doctor(db, doctor_id)

    if not doctor:
        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
        )

    return doctor


@router.get("/{doctor_id}/patients")
def get_doctor_patients(
    doctor_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    doctor = db.query(models.Doctor).filter(
        models.Doctor.id == doctor_id
    ).first()

    if not doctor:
        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
        )

    if current_user["role"] == "doctor":
        if current_user["doctor_id"] != doctor_id:
            raise HTTPException(
                status_code=403,
                detail="You can only view your assigned patients"
            )

    patients = db.query(models.Patient).filter(
        models.Patient.doctor_id == doctor_id
    ).all()

    return patients


@router.put("/{doctor_id}")
def update_doctor_details(
    doctor_id: int,
    doctor: DoctorCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    return update_doctor(db, doctor_id, doctor)


@router.patch("/{doctor_id}")
def patch_doctor(
    doctor_id: int,
    doctor: DoctorUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    return update_doctor(db, doctor_id, doctor)


@router.delete("/{doctor_id}")
def delete_doctor_by_id(
    doctor_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    return delete_doctor(db, doctor_id)