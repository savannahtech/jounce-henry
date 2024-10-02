from sqlalchemy.orm import Session
from models.models import Metric, Ranking, LLM, SimulationResult
from schemas.schemas import RankingResponse
from sqlalchemy import func

def get_rankings_by_metric(db: Session, metric_name: str):
    metric = db.query(Metric).filter(Metric.name == metric_name).first()
    if not metric:
        return None

    # Calculate mean values
    mean_values = (
        db.query(
            SimulationResult.llm_id,
            func.avg(SimulationResult.value).label("mean_value")
        )
        .filter(SimulationResult.metric_id == metric.id)
        .group_by(SimulationResult.llm_id)
        .all()
    )

    if not mean_values:
        return None

    # Determine sorting order based on metric
    ascending = metric_name in ["TTFT", "e2e_latency"]

    # Sort and assign ranks
    sorted_mean = sorted(mean_values, key=lambda x: x.mean_value, reverse=not ascending)
    rankings = []
    for rank, item in enumerate(sorted_mean, start=1):
        llm = db.query(LLM).filter(LLM.id == item.llm_id).first()
        rankings.append(RankingResponse(
            llm=llm.name,
            mean_value=round(item.mean_value, 3),
            rank=rank
        ))

        # Update or create Ranking entry
        db.query(Ranking).filter(
            Ranking.metric_id == metric.id,
            Ranking.llm_id == llm.id
        ).update({"mean_value": item.mean_value, "rank": rank}, synchronize_session=False)

    db.commit()
    return rankings
