from fastapi import APIRouter

from app.db.postgres import SessionLocal
from app.models.appointment import Appointment

router = APIRouter()


@router.get("/appointments")
def get_appointments():

    db = SessionLocal()

    appointments = db.query(Appointment).all()

    result = []

    for appt in appointments:

        result.append({
            "patient_name": appt.patient_name,
            "age": appt.age,
            "doctor": appt.doctor,
            "date": appt.appointment_date,
            "slot": appt.slot,
            "reason": appt.reason,
            "status": appt.status
        })

    db.close()

    return result