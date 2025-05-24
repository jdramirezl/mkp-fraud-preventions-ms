from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.database.database import Base, setup_database
from src.routes.fraud_prevention import router as fraud_prevention_router

# Initialize database
engine, _ = setup_database()
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Fraud Prevention API",
    description="API for fraud prevention and risk assessment",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(fraud_prevention_router)


# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "healthy"}
