from app.services.scheduler.booking_engine import (
    get_available_slots,
    book_appointment
)

def route_tool(message):

    message = message.lower()

    if "book" in message:

        slots = get_available_slots()

        return {
            "tool": "availability",
            "slots": slots
        }

    return None