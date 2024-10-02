from fastapi import APIRouter, HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session
from crud.crud import get_rankings_by_metric
from schemas.schemas import RankingResponse
from db.session import get_db

router = APIRouter()

@router.get("/{metric_name}", response_model=List[RankingResponse])
def get_rankings(metric_name: str, db: Session = Depends(get_db)):
    rankings = get_rankings_by_metric(db, metric_name=metric_name)
    if not rankings:
        raise HTTPException(status_code=404, detail="Metric not found or no rankings available.")
    return rankings
