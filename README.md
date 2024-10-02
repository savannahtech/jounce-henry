# LLM Benchmark Simulation API

This project provides a benchmarking simulation system for evaluating Large Language Models (LLMs) on different performance metrics. It supports infrastructure deployment, simulations with Celery, and API-based interaction for LLM ranking.

Features
Simulate multiple performance metrics (e.g., TTFT, TPS, e2e_latency, RPS) for various LLMs.
API-based interaction to trigger simulations and retrieve rankings.
Asynchronous task handling with Celery and Redis.
PostgreSQL as the primary database.
Supports scaling simulations and monitoring with task retry mechanisms.

## Getting Started

### Prerequisites

- Python 3.x
- Docker
- Docker Compose
- Redis
- PostgreSQL
- Node

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/Hudeh/llm-benchmark.git
   cd llm-benchmark
   ```

2. **Configure environment variables:**

   Rename env_sample to .env and update the values as needed:

   ```bash
   mv env_sample .env
   ```

### Running the Project

Using Docker Compose
The easiest way to run the project is by using Docker Compose, which will set up all services automatically

1. **Build and start services:**

   ```bash
   docker-compose up --build
   ```

   Services included in the Docker Compose setup:

   FastAPI server: Runs on <http://localhost:8000>
   PostgreSQL: For database storage
   Redis: Message broker for Celery tasks
   Celery workers: For handling asynchronous simulation tasks
   Celery Beat: For task scheduling

2. **Access the API Documentation:**

   Once the services are running, you can access the auto-generated Swagger UI documentation at:

   <http://localhost:8000/docs>

Running Locally (Without Docker)
If you prefer to run the project locally, follow these steps

1. **Set up a Python virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # For Linux/Mac
   ```

   ```bash
   python -m venv venv
   venv/Scripts/activate # For windows
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run FastAPI server:**

   ```bash
   uvicorn app.main:app --reload
   ```

4. **Start Celery workers:**

   ```bash
   celery -A app.tasks.celery_tasks worker --loglevel=info
   ```

5. **Start Celery Beat (for scheduled tasks):**

   ```bash
   celery -A app.tasks.celery_tasks beat --loglevel=info
   ```

## Database Migrations

```bash
alembic upgrade head
```

## API Endpoints

The API allows interaction with the simulation system through the following endpoints:

1. **Trigger a new simulation:**

   ```bash
   POST /run-simulation/
   ```

   Request body example:

   ```json
   {
     "simulation_name": "Test Simulation",
     "count": 1000,
     "seed": 42
   }
   ```

   Response

   ```json
   {
     "task_id": "unique_task_id",
     "status": "Task submitted successfully.",
     "simulation_name": "Test Simulation"
   }
   ```

2. **Check the status of a Celery task:**

   ```bash
   GET /task-status/{task_id}
   ```

   Response example:

   ```json
   {
     "task_id": "unique_task_id",
     "status": "SUCCESS",
     "result": "Simulation 'Test Simulation' completed successfully."
   }
   ```

3. **Get LLM rankings for a specific metric:**

   ```bash
   GET /api/v1/rankings/{metric_name}/
   ```

   Example response:

   ```json
   [
     {
       "llm": "GPT-4o",
       "mean_value": 0.523,
       "rank": 1
     },
     {
       "llm": "Llama 3.1 405",
       "mean_value": 0.612,
       "rank": 2
     },
     {
       "llm": "Mistral Large2",
       "mean_value": 0.745,
       "rank": 3
     }
   ]
   ```

## Dashboard Visualization

1. **Set Up React Project**

   ```bash
   cd llm-benchmark-dashboard
   ```

2. **Install Required Dependencies**

   ```bash
   npm install
   ```

3. **Run Your Application**

   Finally, start your React application

   ```bash
   npm start
   ```

## Monitoring and Logging

1. **Monitoring with Prometheus and Grafana**
    Install Prometheus and Grafana using Helm:

    ```bash
    helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
    helm repo update

    # Install Prometheus
    helm install prometheus prometheus-community/prometheus --namespace monitoring

    # Install Grafana
    helm install grafana grafana/grafana --namespace monitoring
    ```

2. **Logging with ELK Stack**
    Install the ELK stack (Elasticsearch, Logstash, Kibana) using Helm:

    ```bash
    helm repo add elastic https://helm.elastic.co
    helm repo update
    ```

    Install Elasticsearch

    ```bash
    helm install elasticsearch elastic/elasticsearch --namespace logging
    ```

    Install Kibana

    ```bash
    helm install kibana elastic/kibana --namespace logging
    ```
