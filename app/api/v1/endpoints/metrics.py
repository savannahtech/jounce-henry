from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from db.session import SessionLocal
from models.models import Metric

router = APIRouter()


@router.get("/metrics/")
async def get_metrics():
    """
    API endpoint to retrieve all available metrics.

    Returns:
        List[Metric]: A list of metrics.
    """
    db: Session = SessionLocal()
    try:
        metrics = db.query(Metric).all()
        if not metrics:
            raise HTTPException(status_code=404, detail="No metrics found.")
        return metrics
    finally:
        db.close()
