from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from app.db.postgres import Base


class Appointment(Base):

    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)

    patient_name = Column(String)

    age = Column(String)

    doctor = Column(String)

    appointment_date = Column(String)

    slot = Column(String)

    reason = Column(String)

    status = Column(String, default="booked")