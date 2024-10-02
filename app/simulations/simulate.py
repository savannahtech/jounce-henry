import random
from datetime import datetime
from sqlalchemy.orm import Session
from models.models import LLM, Metric, SimulationResult, Simulation
from db.session import SessionLocal
from core.config import settings


def generate_metric_value(metric_name: str) -> float:
    """Dynamically generate values based on the metric name."""
    if metric_name == "TTFT":
        return round(random.uniform(0.1, 1.0), 3)  # Time to First Token
    elif metric_name == "TPS":
        return round(random.uniform(10, 1000), 2)  # Tokens Per Second
    elif metric_name == "e2e_latency":
        return round(random.uniform(50, 500), 2)  # End-to-End Latency
    elif metric_name == "RPS":
        return round(random.uniform(1, 100), 2)  # Requests Per Second
    else:
        return round(random.uniform(0, 100), 2)  # Default value for unknown metrics


def run_simulation(simulation_name: str, count: int = 1000, seed: int = None):
    if seed is not None:
        random.seed(seed)

    db: Session = SessionLocal()

    try:
        # Create a new Simulation record
        simulation = Simulation(
            name=simulation_name, timestamp=datetime.utcnow(), seed=seed
        )
        db.add(simulation)
        db.flush()

        # Ensure LLMs and Metrics exist, allowing dynamic addition of new ones
        for name in settings.LLM_NAMES:
            llm = db.query(LLM).filter(LLM.name == name).first()
            if not llm:
                llm = LLM(name=name)
                db.add(llm)

        for name in settings.METRICS_NAMES:
            metric = db.query(Metric).filter(Metric.name == name).first()
            if not metric:
                metric = Metric(name=name)
                db.add(metric)

        db.commit()

        # Retrieve LLMs and Metrics from the database
        llms = db.query(LLM).all()
        metrics = db.query(Metric).all()

        simulation_results = []
        for llm in llms:
            for metric in metrics:
                for _ in range(count):
                    value = generate_metric_value(metric.name)
                    simulation_result = SimulationResult(
                        llm_id=llm.id,
                        metric_id=metric.id,
                        value=value,
                        timestamp=datetime.utcnow(),
                        simulation_id=simulation.id,
                    )
                    simulation_results.append(simulation_result)

        # Bulk save the simulation results
        db.bulk_save_objects(simulation_results)
        db.commit()

        print(
            f"Successfully generated {count * len(llms) * len(metrics)} simulation results."
        )
    except Exception as e:
        db.rollback()
        print(f"An error occurred: {e}")
    finally:
        db.close()
