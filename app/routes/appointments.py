from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app import models
from app.schemas import AppointmentCreate, AppointmentUpdate
from app.auth import get_current_user, require_admin


router = APIRouter(
    prefix="/appointments",
    tags=["Appointments"]
)


@router.post("/")
def create_appointment(
    appointment: AppointmentCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    doctor = db.query(models.Doctor).filter(
        models.Doctor.id == appointment.doctor_id
    ).first()

    if not doctor:
        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
        )

    if not doctor.is_active:
        raise HTTPException(
            status_code=400,
            detail="Cannot create appointment with inactive doctor"
        )

    patient = db.query(models.Patient).filter(
        models.Patient.id == appointment.patient_id
    ).first()

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    existing = db.query(models.Appointment).filter(
        models.Appointment.doctor_id == appointment.doctor_id,
        models.Appointment.appointment_date == appointment.appointment_date,
        models.Appointment.status == "scheduled"
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Doctor already has an appointment at this time"
        )

    new_appointment = models.Appointment(
        doctor_id=appointment.doctor_id,
        patient_id=appointment.patient_id,
        appointment_date=appointment.appointment_date,
        status=appointment.status
    )

    db.add(new_appointment)
    db.commit()
    db.refresh(new_appointment)

    return new_appointment


@router.get("/")
def get_appointments(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    query = db.query(models.Appointment)

    if current_user["role"] == "doctor":
        query = query.filter(
            models.Appointment.doctor_id == current_user["doctor_id"]
        )

    return query.all()


@router.get("/{appointment_id}")
def get_appointment(
    appointment_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    appointment = db.query(models.Appointment).filter(
        models.Appointment.id == appointment_id
    ).first()

    if not appointment:
        raise HTTPException(
            status_code=404,
            detail="Appointment not found"
        )

    if current_user["role"] == "doctor":
        if appointment.doctor_id != current_user["doctor_id"]:
            raise HTTPException(
                status_code=403,
                detail="You can only view your appointments"
            )

    return appointment


@router.put("/{appointment_id}")
def update_appointment(
    appointment_id: int,
    appointment: AppointmentUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    existing = db.query(models.Appointment).filter(
        models.Appointment.id == appointment_id
    ).first()

    if not existing:
        raise HTTPException(
            status_code=404,
            detail="Appointment not found"
        )

    update_data = appointment.model_dump(exclude_unset=True)

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
                detail="Cannot assign appointment to inactive doctor"
            )

    if "patient_id" in update_data:
        patient = db.query(models.Patient).filter(
            models.Patient.id == update_data["patient_id"]
        ).first()

        if not patient:
            raise HTTPException(
                status_code=404,
                detail="Patient not found"
            )

    for key, value in update_data.items():
        setattr(existing, key, value)

    db.commit()
    db.refresh(existing)

    return existing


@router.delete("/{appointment_id}")
def delete_appointment(
    appointment_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    appointment = db.query(models.Appointment).filter(
        models.Appointment.id == appointment_id
    ).first()

    if not appointment:
        raise HTTPException(
            status_code=404,
            detail="Appointment not found"
        )

    db.delete(appointment)
    db.commit()

    return {
        "message": "Appointment deleted successfully"
    }


@router.get("/doctors/{doctor_id}")
def get_doctor_appointments(
    doctor_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    if current_user["role"] == "doctor":
        if current_user["doctor_id"] != doctor_id:
            raise HTTPException(
                status_code=403,
                detail="You can only view your appointments"
            )

    doctor = db.query(models.Doctor).filter(
        models.Doctor.id == doctor_id
    ).first()

    if not doctor:
        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
        )

    return db.query(models.Appointment).filter(
        models.Appointment.doctor_id == doctor_id
    ).all()


@router.get("/patients/{patient_id}")
def get_patient_appointments(
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
                detail="You can only view appointments of your assigned patients"
            )

    return db.query(models.Appointment).filter(
        models.Appointment.patient_id == patient_id
    ).all()