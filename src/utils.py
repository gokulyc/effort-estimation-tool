TOTAL_TASK_TIME_AVAILABLE = 15 * 8 # In Hrs
K = TOTAL_TASK_TIME_AVAILABLE / (40 * 8) 


def calculate_task_estimate(complexity: int, size: int):
    return round(K * complexity * size,2)
