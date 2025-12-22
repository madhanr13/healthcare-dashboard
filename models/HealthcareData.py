from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from enum import Enum


class PatientStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    DISCHARGED = "discharged"


@dataclass
class Patient:
    patient_id: str
    name: str
    age: int
    gender: str
    status: PatientStatus
    admission_date: datetime
    discharge_date: Optional[datetime] = None


@dataclass
class VitalSigns:
    patient_id: str
    timestamp: datetime
    heart_rate: float  # bpm
    blood_pressure_systolic: float  # mmHg
    blood_pressure_diastolic: float  # mmHg
    temperature: float  # Celsius
    respiratory_rate: float  # breaths/min
    oxygen_saturation: float  # percentage


@dataclass
class LabResults:
    patient_id: str
    timestamp: datetime
    test_name: str
    value: float
    unit: str
    reference_range: str
    abnormal: bool = False
