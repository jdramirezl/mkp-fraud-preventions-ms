import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Set default environment
if "TESTING" not in os.environ:
    os.environ["TESTING"] = "false"


def get_connection_string() -> str:
    # Test environment uses SQLite
    if os.getenv("TESTING") == "true":
        return "sqlite://"

    # Production environment
    print(f"ENVIRONMENT: {os.getenv('ENVIRONMENT')}")
    # Print all db related environment variables
    print(f"DB_USER: {os.getenv('DB_USER')}")
    print(f"DB_PASSWORD: {os.getenv('DB_PASSWORD')}")
    print(f"DB_NAME: {os.getenv('DB_NAME')}")
    print(f"DB_HOST: {os.getenv('DB_HOST')}")
    print(f"DB_PORT: {os.getenv('DB_PORT')}")
    print(f"INSTANCE_CONNECTION_NAME: {os.getenv('INSTANCE_CONNECTION_NAME')}")

    if os.getenv("ENVIRONMENT") == "production":
        instance_connection_name = os.getenv("INSTANCE_CONNECTION_NAME")
        db_user = os.getenv("DB_USER")
        db_pass = os.getenv("DB_PASSWORD")
        db_name = os.getenv("DB_NAME")

        # Cloud SQL connection using Unix socket
        unix_socket = f"/cloudsql/{instance_connection_name}"
        return (
            f"mysql+pymysql://{db_user}:{db_pass}@{db_name}?unix_socket={unix_socket}"
        )

    # Local development connection
    db_host = os.getenv("DB_HOST", "localhost")
    db_port = os.getenv("DB_PORT", "3306")
    db_user = os.getenv("DB_USER")
    db_pass = os.getenv("DB_PASSWORD")
    db_name = os.getenv("DB_NAME")
    return f"mysql+pymysql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"


def get_engine_args():
    if os.getenv("TESTING") == "true":
        return {"connect_args": {"check_same_thread": False}}
    return {"pool_size": 5, "max_overflow": 2, "pool_timeout": 30, "pool_recycle": 1800}


# Base class for models
Base = declarative_base()

# Create database engine and session factory lazily
engine = None
SessionLocal = None


def setup_database():
    global engine, SessionLocal
    if engine is None:
        engine = create_engine(get_connection_string(), **get_engine_args())
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return engine, SessionLocal


# Dependency to get database session
def get_db():
    if SessionLocal is None:
        setup_database()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
