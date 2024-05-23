from flask_pymongo import PyMongo, ObjectId


class User:
    def __init__(self, email, name, password, id = None) -> None:
        if self.id:
            self.id = ObjectId(id)
        self.email = email
        self.name = name
        self.password = password

    def get_data(self, ignore_fields=["id", "password"]):
        di = {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "password": self.password,
        }
        for key in ignore_fields:
            di.pop(key)
        return di


# class DB_Ops:
#     def __init__(self, mongo_client: PyMongo) -> None:
#         self.mongo= mongo_client

#     def insert_record(self,collection,data, mongo: PyMongo):
#         mongo.db.auth_users.insert_one({"email":})
