from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.v1.endpoints import rankings
from api.v1.endpoints import simulations
from api.v1.endpoints import metrics
from core.config import settings
from db.base import Base
from db.session import engine

# Create all database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.PROJECT_VERSION,
)
# CORS configuration
origins = [
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Include API routers
app.include_router(rankings.router, prefix="/api/v1/rankings", tags=["rankings"])
app.include_router(simulations.router, prefix="/api/v1/simulations", tags=["simulation tasks"])
app.include_router(metrics.router, prefix="/api/v1", tags=["metrics"])
