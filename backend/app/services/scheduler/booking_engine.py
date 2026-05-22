from app.db.postgres import SessionLocal

from app.models.appointment import Appointment

from app.data.doctors import DOCTORS


available_slots = [
    "10 am",
    "11 am",
    "2 pm",
    "4 pm",
    "6 pm"
]


def get_doctors():

    return DOCTORS


def get_available_slots(
    doctor,
    appointment_date
):

    db = SessionLocal()

    appointments = db.query(Appointment).filter(
        Appointment.doctor == doctor,
        Appointment.appointment_date == appointment_date,
        Appointment.status == "booked"
    ).all()

    booked_slots = [
        appt.slot
        for appt in appointments
    ]

    remaining_slots = []

    for slot in available_slots:

        if slot not in booked_slots:

            remaining_slots.append(slot)

    db.close()

    return remaining_slots


def book_appointment(
    patient,
    doctor,
    specialty,
    appointment_date,
    slot
):

    db = SessionLocal()

    existing = db.query(Appointment).filter(
        Appointment.doctor == doctor,
        Appointment.appointment_date == appointment_date,
        Appointment.slot == slot,
        Appointment.status == "booked"
    ).first()

    if existing:

        db.close()

        return {
            "success": False
        }

    appointment = Appointment(

        patient=patient,

        doctor=doctor,

        specialty=specialty,

        appointment_date=appointment_date,

        slot=slot,

        status="booked"
    )

    db.add(appointment)

    db.commit()

    db.refresh(appointment)

    db.close()

    return {
        "success": True
    }