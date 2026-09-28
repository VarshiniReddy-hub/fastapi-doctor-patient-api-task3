from sqlalchemy.orm import Session
from fastapi import HTTPException
from app import models
from app.schemas import DoctorCreate, DoctorUpdate, PatientCreate, PatientUpdate


def create_doctor(db: Session, doctor: DoctorCreate):
    existing_doctor = db.query(models.Doctor).filter(
        models.Doctor.email == doctor.email
    ).first()

    if existing_doctor:
        raise HTTPException(
            status_code=400,
            detail="Doctor email already exists"
        )

    new_doctor = models.Doctor(
        name=doctor.name,
        specialization=doctor.specialization,
        email=doctor.email,
        is_active=True
    )

    db.add(new_doctor)
    db.commit()
    db.refresh(new_doctor)

    return new_doctor


def get_doctor(db: Session, doctor_id: int):
    doctor = db.query(models.Doctor).filter(
        models.Doctor.id == doctor_id
    ).first()

    if not doctor:
        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
        )

    return doctor


def update_doctor(db: Session, doctor_id: int, doctor_data: DoctorUpdate):
    doctor = get_doctor(db, doctor_id)

    update_data = doctor_data.model_dump(exclude_unset=True)

    if "email" in update_data:
        existing_doctor = db.query(models.Doctor).filter(
            models.Doctor.email == update_data["email"],
            models.Doctor.id != doctor_id
        ).first()

        if existing_doctor:
            raise HTTPException(
                status_code=400,
                detail="Doctor email already exists"
            )

    for key, value in update_data.items():
        setattr(doctor, key, value)

    db.commit()
    db.refresh(doctor)

    return doctor


def delete_doctor(db: Session, doctor_id: int):
    doctor = get_doctor(db, doctor_id)

    doctor.is_active = False

    db.commit()
    db.refresh(doctor)

    return doctor


def create_patient(db: Session, patient: PatientCreate):
    if patient.doctor_id is not None:
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


def get_patient(db: Session, patient_id: int):
    patient = db.query(models.Patient).filter(
        models.Patient.id == patient_id
    ).first()

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    return patient


def update_patient(db: Session, patient_id: int, patient_data: PatientUpdate):
    patient = get_patient(db, patient_id)

    update_data = patient_data.model_dump(exclude_unset=True)

    if "doctor_id" in update_data and update_data["doctor_id"] is not None:
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
        setattr(patient, key, value)

    db.commit()
    db.refresh(patient)

    return patient


def delete_patient(db: Session, patient_id: int):
    patient = get_patient(db, patient_id)

    db.delete(patient)
    db.commit()

    return {
        "message": "Patient deleted successfully"
    }