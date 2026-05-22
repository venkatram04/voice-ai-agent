from datetime import datetime, timedelta

from sqlalchemy import and_

from app.db.postgres import SessionLocal
from app.models.appointment import Appointment

from app.agents.nova_ai import ask_nova


VALID_DOCTORS = [
    "Dr Kumar",
    "Dr Priya",
    "Dr Ahmed"
]

VALID_SLOTS = [
    "10 AM",
    "11 AM",
    "2 PM",
    "4 PM"
]

sessions = {}


def reset_session(session_id):

    sessions[session_id] = {
        "stage": "start"
    }


async def process_message(session_id, message):

    message = message.strip()

    lower_message = message.lower()

    if session_id not in sessions:

        reset_session(session_id)

    session = sessions[session_id]

    stage = session["stage"]

    # =========================
    # CANCEL / RESET
    # =========================
    cancel_words = [
        "cancel",
        "stop",
        "reset",
        "exit"
    ]

    if any(word in lower_message for word in cancel_words):

        reset_session(session_id)

        return {
            "response": (
                "Okay, conversation reset successfully."
            ),
            "appointment": None
        }

    # =========================
    # GREETINGS
    # =========================
    greetings = [
        "hi",
        "hello",
        "good morning",
        "good evening"
    ]

    if any(greet in lower_message for greet in greetings):

        ai_reply = await ask_nova(message)

        return {
            "response": ai_reply,
            "appointment": None
        }

    # =========================
    # DOCTOR QUERY
    # =========================
    if (
        "doctor" in lower_message
        or "available doctors" in lower_message
    ):

        doctors_text = "\n".join(VALID_DOCTORS)

        return {
            "response": (
                f"Available doctors are:\n"
                f"{doctors_text}"
            ),
            "appointment": None
        }

    # =========================
    # START BOOKING
    # =========================
    if stage == "start":

        if (
            "appointment" in lower_message
            or "book" in lower_message
        ):

            today = datetime.now().strftime(
                "%Y-%m-%d"
            )

            tomorrow = (
                datetime.now() +
                timedelta(days=1)
            ).strftime("%Y-%m-%d")

            session["stage"] = "date"

            return {
                "response": (
                    f"Available booking dates are "
                    f"{today} and {tomorrow}. "
                    f"Please choose today or tomorrow."
                ),
                "appointment": None
            }

        ai_reply = await ask_nova(message)

        return {
            "response": ai_reply,
            "appointment": None
        }

    # =========================
    # DATE STAGE
    # =========================
    elif stage == "date":

        if "today" in lower_message:

            selected_date = datetime.now().strftime(
                "%Y-%m-%d"
            )

        elif "tomorrow" in lower_message:

            selected_date = (
                datetime.now() +
                timedelta(days=1)
            ).strftime("%Y-%m-%d")

        else:

            return {
                "response": (
                    "Please choose either "
                    "'today' or 'tomorrow'."
                ),
                "appointment": None
            }

        session["appointment_date"] = selected_date

        session["stage"] = "doctor"

        return {
            "response": (
                f"Selected date is "
                f"{selected_date}. "
                f"Please provide doctor name."
            ),
            "appointment": None
        }

    # =========================
    # DOCTOR STAGE
    # =========================
    elif stage == "doctor":

        matched_doctor = None

        for doctor in VALID_DOCTORS:

            if doctor.lower() in lower_message:

                matched_doctor = doctor

                break

        if not matched_doctor:

            return {
                "response": (
                    "Please choose a valid doctor.\n"
                    "Available doctors are:\n"
                    "Dr Kumar\n"
                    "Dr Priya\n"
                    "Dr Ahmed"
                ),
                "appointment": None
            }

        session["doctor"] = matched_doctor

        session["stage"] = "slot"

        return {
            "response": (
                "Available slots are:\n"
                "10 AM\n"
                "11 AM\n"
                "2 PM\n"
                "4 PM"
            ),
            "appointment": None
        }

    # =========================
    # SLOT STAGE
    # =========================
    elif stage == "slot":

        normalized_slot = message.upper()

        valid = False

        for slot in VALID_SLOTS:

            if slot.upper() == normalized_slot:

                valid = True
                normalized_slot = slot
                break

        if not valid:

            return {
                "response": (
                    "Please choose a valid slot:\n"
                    "10 AM, 11 AM, 2 PM, 4 PM"
                ),
                "appointment": None
            }

        db = SessionLocal()

        existing = db.query(Appointment).filter(
            and_(
                Appointment.doctor ==
                session["doctor"],

                Appointment.appointment_date ==
                session["appointment_date"],

                Appointment.slot ==
                normalized_slot
            )
        ).first()

        if existing:

            db.close()

            return {
                "response": (
                    f"{normalized_slot} is already booked. "
                    f"Please choose another slot."
                ),
                "appointment": None
            }

        db.close()

        session["slot"] = normalized_slot

        session["stage"] = "name"

        return {
            "response": (
                "Please tell your full name."
            ),
            "appointment": None
        }

    # =========================
    # NAME STAGE
    # =========================
    elif stage == "name":

        session["patient_name"] = message

        session["stage"] = "age"

        return {
            "response": (
                "Please tell your age."
            ),
            "appointment": None
        }

    # =========================
    # AGE STAGE
    # =========================
    elif stage == "age":

        if not message.isdigit():

            return {
                "response": (
                    "Please provide valid age."
                ),
                "appointment": None
            }

        session["age"] = message

        session["stage"] = "reason"

        return {
            "response": (
                "Please tell reason "
                "for appointment."
            ),
            "appointment": None
        }

    # =========================
    # REASON STAGE
    # =========================
    elif stage == "reason":

        corrected_reason = await ask_nova(
            f"Correct this medical sentence only: {message}"
        )

        session["reason"] = corrected_reason

        db = SessionLocal()

        appointment = Appointment(
            patient_name=session["patient_name"],
            age=session["age"],
            doctor=session["doctor"],
            appointment_date=session["appointment_date"],
            slot=session["slot"],
            reason=session["reason"],
            status="booked"
        )

        db.add(appointment)

        db.commit()

        all_appointments = db.query(
            Appointment
        ).all()

        appointments_list = []

        for appt in all_appointments:

            appointments_list.append({
                "patient_name": appt.patient_name,
                "age": appt.age,
                "doctor": appt.doctor,
                "date": appt.appointment_date,
                "slot": appt.slot,
                "reason": appt.reason
            })

        db.close()

        reset_session(session_id)

        return {
            "response": (
                "Appointment booked successfully."
            ),
            "appointment": appointments_list
        }

    return {
        "response": (
            "Sorry, I didn't understand that."
        ),
        "appointment": None
    }