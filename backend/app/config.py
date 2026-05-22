import os

from dotenv import load_dotenv

load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv(
    "AWS_ACCESS_KEY_ID"
)

AWS_SECRET_ACCESS_KEY = os.getenv(
    "AWS_SECRET_ACCESS_KEY"
)

AWS_REGION = os.getenv(
    "AWS_REGION"
)

POSTGRES_USER = os.getenv(
    "POSTGRES_USER"
)

POSTGRES_PASSWORD = os.getenv(
    "POSTGRES_PASSWORD"
)

POSTGRES_DB = os.getenv(
    "POSTGRES_DB"
)

POSTGRES_HOST = os.getenv(
    "POSTGRES_HOST"
)

POSTGRES_PORT = os.getenv(
    "POSTGRES_PORT"
)