from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class DoctorBase(BaseModel):
    name: str
    specialization: str
    email: EmailStr


class DoctorCreate(DoctorBase):
    pass


class DoctorUpdate(BaseModel):
    name: Optional[str] = None
    specialization: Optional[str] = None
    email: Optional[EmailStr] = None


class PatientBase(BaseModel):
    name: str
    age: int = Field(gt=0)
    phone: str = Field(pattern=r"^[0-9]{10}$")
    doctor_id: Optional[int] = None


class PatientCreate(PatientBase):
    pass


class PatientUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = Field(default=None, gt=0)
    phone: Optional[str] = Field(default=None, pattern=r"^[0-9]{10}$")
    doctor_id: Optional[int] = None