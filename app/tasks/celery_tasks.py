from celery import Celery
from celery import shared_task
from core.config import settings
from simulations.simulate import run_simulation
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

celery_app = Celery(__name__, broker=settings.REDIS_URL, backend=settings.REDIS_URL)
celery_app.autodiscover_tasks()
celery_app.conf.broker_connection_retry_on_startup = True


@shared_task(name="simulation-queue", bind=True, max_retries=3)
def run_simulation_task(self, simulation_name: str, count: int = 1000, seed: int = 42):
    try:
        logger.info(
            f"Running simulation: {simulation_name} with count {count} and seed {seed}"
        )
        run_simulation(simulation_name=simulation_name, count=count, seed=seed)
        return f"Simulation '{simulation_name}' completed successfully."

    except Exception as exc:
        logger.error(f"Simulation '{simulation_name}' task failed with error: {exc}")
        if self.request.retries >= self.max_retries:
            logger.error(
                f"Max retries reached for task {self.request.id}. Marking as failed."
            )
            return f"Simulation '{simulation_name}' failed after {self.max_retries} retries."

        raise self.retry(exc=exc, countdown=60)
