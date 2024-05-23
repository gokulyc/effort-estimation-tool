
class User:
    def __init__(self, email, name, password, _id = None) -> None:
        self._id = _id
        self.email = email
        self.name = name
        self.password = password

    def get_data(self, ignore_fields=["_id", "password"]):
        di = {
            "id": str(self._id),
            "name": self.name,
            "email": self.email,
            "password": self.password,
        }
        for key in ignore_fields:
            di.pop(key)
        return di
