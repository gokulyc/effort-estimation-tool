TOTAL_TASK_TIME_AVAILABLE = 15 * 8  # In Hrs
TASK_UNIT = TOTAL_TASK_TIME_AVAILABLE / (40 * 8)


def calculate_task_time(complexity: int, size: int):
    task_time = round(TASK_UNIT * complexity * size, 2)
    return task_time


# TASK_ESTIMATED_TIME = {
#     "development": {"size": {2: 4, 4: 16, 6: 32, 8: 64}},
#     "testing": {"size": {2: 4, 4: 16, 6: 32, 8: 64}},
#     "documentation": {"size": {2: 4, 4: 8, 6: 16, 8: 32}},
#     "maintenence": {"size": {2: 4, 4: 8, 6: 32, 8: 64}},
#     "admin": {"size": {2: 2, 4: 4, 6: 8, 8: 16}},
#     "ops": {"size": {2: 8, 4: 32, 6: 64, 8: 96}},
# }


# def calculate_estimated_metrics(task_type, task_size):
#     size_dict = TASK_ESTIMATED_TIME[task_type]["size"]
#     min_time = min(list(size_dict.values()))
#     max_time = max(list(size_dict.values()))
#     unit_time = (max_time - min_time) / max_time
#     range_slice = 5 * unit_time

#     max_time_range = round(size_dict[task_size] + range_slice, 2)
#     min_time_range = round(size_dict[task_size] - range_slice, 2)

#     confidence_level = None
#     high_confidence_level = round(75 * unit_time, 2)
#     medium_confidence_level = round(40 * unit_time, 2)
#     if task_size >= high_confidence_level:
#         confidence_level = "High"
#     elif task_size >= medium_confidence_level and task_size < high_confidence_level:
#         confidence_level = "Medium"
#     else:
#         confidence_level = "Low"
#     print(f"{high_confidence_level=} {medium_confidence_level=}")
#     return {
#         "range": f"{min_time_range} - {max_time_range}",
#         "confidence_level": confidence_level,
#         "estimated_effort": size_dict[task_size],
#     }

TASK_ESTIMATED_TIME = {
    "development": {"high": 120, "low": 4},
    "testing": {"high": 100, "low": 4},
    "documentation": {"high": 40, "low": 2},
    "maintenence": {"high": 80, "low": 4},
    "admin": {"high": 40, "low": 2},
    "ops": {"high": 120, "low": 4},
}


def calculate_estimated_metrics(task_type, task_size):
    size_max_min = TASK_ESTIMATED_TIME[task_type]

    unit_time = (size_max_min["high"] - size_max_min["low"]) / size_max_min["high"]
    range_slice = 0.05 * unit_time # 5%

    max_time_range = round(task_size * unit_time + range_slice, 2)
    min_time_range = round(task_size * unit_time - range_slice, 2)
    estimated_effort = round(task_size * unit_time, 2)
    confidence_level = None
    high_confidence_level = round(75 * unit_time, 2)
    medium_confidence_level = round(40 * unit_time, 2)
    if task_size >= high_confidence_level:
        confidence_level = "High"
    elif task_size >= medium_confidence_level and task_size < high_confidence_level:
        confidence_level = "Medium"
    else:
        confidence_level = "Low"
    print(f"{high_confidence_level=} {medium_confidence_level=}")
    return {
        "range": f"{min_time_range} - {max_time_range}",
        "confidence_level": confidence_level,
        "estimated_effort": estimated_effort,
    }


# if __name__ == "__main__":
#     result = calculate_estimated_metrics(TASK_ESTIMATED_TIME["development"]["size"], 6)
#     print(result)
