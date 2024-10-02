import random

def generate_random_value(metric_name: str) -> float:
    if metric_name == "TTFT":
        return round(random.uniform(0.1, 1.0), 3)
    elif metric_name == "TPS":
        return round(random.uniform(10, 1000), 2)
    elif metric_name == "e2e_latency":
        return round(random.uniform(50, 500), 2)
    elif metric_name == "RPS":
        return round(random.uniform(1, 100), 2)
    else:
        return 0.0
