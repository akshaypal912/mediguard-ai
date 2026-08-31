from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import Base, engine
from .ml import load_model
from .routers import patients, assessment, medications, reports

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    load_model()
    yield

app = FastAPI(
    title="MediGuardAI Backend",
    description="AI-powered healthcare risk and patient-safety decision support API.",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(patients.router)
app.include_router(assessment.router)
app.include_router(medications.router)
app.include_router(reports.router)

@app.get("/")
def root():
    return {
        "name": "MediGuardAI",
        "status": "online",
        "docs": "/docs",
    }

@app.get("/health")
def health():
    return {"status": "healthy"}
