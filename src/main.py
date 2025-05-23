from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routes.fraud_prevention import router as fraud_prevention_router
from src.database.database import engine, Base

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Fraud Prevention API",
    description="API for fraud prevention and risk assessment",
    version="1.0.0"
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