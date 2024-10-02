from fastapi import APIRouter, HTTPException
from tasks.celery_tasks import run_simulation_task

router = APIRouter()


@router.post("/run-simulation/")
async def run_simulation(simulation_name: str, count: int = 1000, seed: int = 42):
    """
    API endpoint to trigger Celery task for running simulations.

    Args:
        simulation_name (str): Name of the simulation.
        count (int): Number of simulations to run. Default is 1000.
        seed (int): Seed value for random number generation. Default is 42.

    Returns:
        dict: Celery task ID for tracking.
    """
    try:
        task = run_simulation_task.delay(simulation_name, count, seed)
        return {
            "task_id": task.id,
            "status": "Task submitted successfully.",
            "simulation_name": simulation_name,
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error submitting simulation task: {str(e)}"
        )


@router.get("/task-status/{task_id}")
async def get_task_status(task_id: str):
    """
    API endpoint to check the status of the Celery task.

    Args:
        task_id (str): The task ID of the Celery job.

    Returns:
        dict: Task status, result (if completed), or error (if failed).
    """
    try:
        task = run_simulation_task.AsyncResult(task_id)
        return {
            "task_id": task_id,
            "status": task.status,
            "result": task.result if task.status == "SUCCESS" else None,
            "error": str(task.result) if task.status == "FAILURE" else None,
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error retrieving task status: {str(e)}"
        )
