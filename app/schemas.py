from datetime import datetime
from typing import Optional, Literal

from pydantic import BaseModel, EmailStr, Field


class DoctorCreate(BaseModel):
    name: str
    specialization: str
    email: EmailStr


class DoctorUpdate(BaseModel):
    name: Optional[str] = None
    specialization: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None


class PatientCreate(BaseModel):
    name: str
    age: int = Field(gt=0)
    phone: str
    doctor_id: Optional[int] = None


class PatientUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = Field(default=None, gt=0)
    phone: Optional[str] = None
    doctor_id: Optional[int] = None


class AppointmentCreate(BaseModel):
    doctor_id: int
    patient_id: int
    appointment_date: datetime
    status: Literal["scheduled", "completed", "cancelled"] = "scheduled"


class AppointmentUpdate(BaseModel):
    doctor_id: Optional[int] = None
    patient_id: Optional[int] = None
    appointment_date: Optional[datetime] = None
    status: Optional[Literal["scheduled", "completed", "cancelled"]] = None