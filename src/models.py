from enum import Enum

TASK_SIZES = {2: 2, 4: 4, 6: 6, 8: 8}
COMPLEXITY_CHOICES = {"easy": 10, "medium": 20, "hard": 40}


class TaskType(Enum):
    development = "dev"
    testing = "testing"
    documentation = "documentation"
    maintenence = "maintenence"
    admin = "admin"
    ops = "ops"


class User:
    def __init__(self, email, name, password, _id=None) -> None:
        self._id = _id
        self.email = email
        self.name = name
        self.password = password

    def get_data(self, ignore_fields=["id", "password"]):
        di = {
            "id": str(self._id),
            "name": self.name,
            "email": self.email,
            "password": self.password,
        }
        for key in ignore_fields:
            di.pop(key)
        return di


class TaskEstimation:
    def __init__(
        self, name, description, complexity, size, task_type, user_id, _id=None
    ) -> None:
        self._id = _id
        self.name = name
        self.description = description
        self.complexity = complexity
        self.size = size
        self.task_type = task_type
        self.user_id = user_id

    def get_data(self, ignore_fields=["id"]):
        di = {
            "id": str(self._id),
            "name": self.name,
            "description": self.description,
            "complexity": self.complexity,
            "size": self.size,
            "task_type": self.task_type,
            "user_id": self.user_id,
        }
        for key in ignore_fields:
            di.pop(key)
        return di
