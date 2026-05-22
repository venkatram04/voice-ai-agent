from app.db.postgres import Base
from app.db.postgres import engine

from app.models.appointment import Appointment

print("Creating tables...")

Base.metadata.drop_all(bind=engine)

Base.metadata.create_all(bind=engine)

print("Tables created successfully")