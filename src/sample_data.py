from typing import Any
from models import COMPLEXITY_CHOICES, TASK_SIZES, TaskStatus, TaskType
from werkzeug.security import generate_password_hash

AUTH_USERS_DEMO_DATA = [
    {
        "name": "John Doe",
        "email": "john@g.com",
        "password": generate_password_hash("1234", method="scrypt"),
    },
    {
        "name": "Jame Clain",
        "email": "james@g.com",
        "password": generate_password_hash("1234", method="scrypt"),
    },
    {
        "name": "Gokul",
        "email": "g@g.com",
        "password": generate_password_hash("1234", method="scrypt"),
    },
]


TASK_ESTIMATIONS_DEMO_DATA: list[dict[str, Any]] = [
    {
        "name": "Add feature 1",
        "description": "Added feature, which need to be developed in iter 2",
        "complexity": COMPLEXITY_CHOICES["easy"],
        "size": TASK_SIZES[4],
        "task_type": TaskType.development.value,
        "task_status": TaskStatus.Done.value,
    },
    {
        "name": "Add feature 2",
        "description": "Added feature, which need to be developed in iter 2",
        "complexity": COMPLEXITY_CHOICES["medium"],
        "size": TASK_SIZES[6],
        "task_type": TaskType.development.value,
        "task_status": TaskStatus.Done.value,
    },
    {
        "name": "Add feature 2 docs",
        "description": "Add docs for feature, which need to be developed in iter 2",
        "complexity": COMPLEXITY_CHOICES["easy"],
        "size": TASK_SIZES[2],
        "task_type": TaskType.documentation.value,
        "task_status": TaskStatus.Done.value,
    },
    {
        "name": "Refactor feature 3",
        "description": "Modify according to new API, which need to be developed in iter 2",
        "complexity": COMPLEXITY_CHOICES["hard"],
        "size": TASK_SIZES[8],
        "task_type": TaskType.development.value,
        "task_status": TaskStatus.Done.value,
    },
    {
        "name": "Add postgres docker image",
        "description": "Modify according to new API, which need to be developed in iter 2",
        "complexity": COMPLEXITY_CHOICES["medium"],
        "size": TASK_SIZES[8],
        "task_type": TaskType.ops.value,
        "task_status": TaskStatus.Done.value,
    },
    {
        "name": "Add integration testcases for feature 2",
        "description": "Add integration testcases, which need to be developed in iter 2",
        "complexity": COMPLEXITY_CHOICES["medium"],
        "size": TASK_SIZES[6],
        "task_type": TaskType.testing.value,
        "task_status": TaskStatus.Done.value,
    },
]
