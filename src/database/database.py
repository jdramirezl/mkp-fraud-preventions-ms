import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

def get_connection_string() -> str:
    if os.getenv("NODE_ENV") == "production":
        instance_connection_name = os.getenv("INSTANCE_CONNECTION_NAME")
        db_user = os.getenv("DB_USER")
        db_pass = os.getenv("DB_PASSWORD")
        db_name = os.getenv("DB_NAME")
        
        # Cloud SQL connection using Unix socket
        unix_socket = f"/cloudsql/{instance_connection_name}"
        return f"mysql+pymysql://{db_user}:{db_pass}@localhost/{db_name}?unix_socket={unix_socket}"
    else:
        # Local development connection
        db_host = os.getenv("DB_HOST", "localhost")
        db_port = os.getenv("DB_PORT", "3306")
        db_user = os.getenv("DB_USER")
        db_pass = os.getenv("DB_PASSWORD")
        db_name = os.getenv("DB_NAME")
        return f"mysql+pymysql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"

# Create database engine
engine = create_engine(
    get_connection_string(),
    pool_size=5,
    max_overflow=2,
    pool_timeout=30,
    pool_recycle=1800
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 