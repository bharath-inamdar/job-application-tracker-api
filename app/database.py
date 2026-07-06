from pathlib import Path
import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

if __package__ in (None, ""):
    sys.path.append(str(Path(__file__).resolve().parents[1]))

DATABASE_URL = "postgresql://localhost/job_tracker"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


class Base(DeclarativeBase):
    pass


def create_database_tables() -> None:
    import app.db_models  # noqa: F401

    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    create_database_tables()
    print("Database tables created successfully.")