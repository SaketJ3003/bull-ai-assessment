from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.upload import router as upload_router


app = FastAPI(
    title="Bull AI Research Report Generator",
    description="AI-powered financial research report generator",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(upload_router)


@app.get("/")
def root():
    return {
        "message": "Bull AI Research Report Generator API is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }