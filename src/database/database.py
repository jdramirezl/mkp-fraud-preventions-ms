import os
import logging

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Set default environment
if "TESTING" not in os.environ:
    os.environ["TESTING"] = "false"

logger = logging.getLogger(__name__)

def get_connection_string() -> str:
    # Test environment uses SQLite
    if os.getenv("TESTING") == "true":
        return "sqlite://"

    db_url = os.getenv("DB_URL")
    logger.info("DB_URL: %s", db_url)
    
    if db_url:
        return db_url

    # Log environment variables for debugging
    environment = os.getenv('ENVIRONMENT')
    db_user = os.getenv('DB_USER')
    db_pass = os.getenv('DB_PASSWORD')
    db_name = os.getenv('DB_NAME')
    db_host = os.getenv('DB_HOST')
    db_port = os.getenv('DB_PORT')
    
    logger.info("ENVIRONMENT: %s", environment)
    logger.info("DB_USER: %s", db_user)
    logger.info("DB_PASSWORD: %s", db_pass)
    logger.info("DB_NAME: %s", db_name)
    logger.info("DB_HOST: %s", db_host)
    logger.info("DB_PORT: %s", db_port)
    
    # Get common variables
    cloud_sql_public_ip = os.getenv("CLOUD_SQL_PUBLIC_IP")
    
    return (
        f"postgresql://{db_user}:{db_pass}@/{db_name}?host={cloud_sql_public_ip}"
    )



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
