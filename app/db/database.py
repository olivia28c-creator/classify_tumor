from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Si hay DATABASE_URL (en la nube), la usa. Si no, usa SQLite (local)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")

# PostgreSQL en la nube requiere una pequeña corrección en la URL usando el driver de SQLAlchemy
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()
