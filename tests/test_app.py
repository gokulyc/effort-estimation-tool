from src.models import User, TaskEstimation
from flask import Response
from werkzeug.http import parse_cookie
from jwt import decode
from flask_pymongo import PyMongo


class TestEstimateToolApp:
    def test_example(self, app_obj, db_obj: PyMongo):
        app = app_obj
        with app.app_context():
            users_count = db_obj.db.auth_users.count_documents({})
            assert users_count == 2

    def test_account_register(self, app_obj, test_client, db_obj: PyMongo):
        app = app_obj
        account_data = {
            "name": "Gokul",
            "email": "gcy@gmail.com",
            "password": "1234",
        }
        with app.app_context():
            response: Response = test_client.post("/register", data=account_data)
            # print(response.data)
            assert response.status_code == 302
            acc = db_obj.db.auth_users.find_one({"email": "gcy@gmail.com"})
            assert acc is not None
            assert acc["name"] == "Gokul"

    def test_account_login(self, app_obj, test_client, db_obj: PyMongo):
        app = app_obj
        acc_login = {
            "email": "g@g.com",
            "password": "1234",
        }
        with app.app_context():
            response: Response = test_client.post("/login", data=acc_login)
            assert response.status_code == 302
            cookies = response.headers.getlist("Set-Cookie")
            cookie_attrs = parse_cookie(cookies[0])
            # print(cookie_attrs)
            access_token_cookie = cookie_attrs["access_token_cookie"]
            decoded_jwt = decode(
                access_token_cookie, "jwt-secret-string-!@#", ["HS256"]
            )
            # print(decoded_jwt)
            assert decoded_jwt["email"] == "g@g.com"

    def test_add_task_estimate(self, app_obj, test_client, db_obj: PyMongo):
        app = app_obj
        acc_login = {
            "email": "g@g.com",
            "password": "1234",
        }
        task_data = {
            "name": "Add feat 1",
            "description": "for iter 2",
            "complexity": 40,
            "size": 4,
            "task_type": "development",
            "task_status": "pending",
        }
        with app.app_context():
            response: Response = test_client.post("/login", data=acc_login)
            # print(response.data)

            response: Response = test_client.post("/add_task", data=task_data)
            # print(response.data)

            assert response.status_code == 302
            task_estimate = db_obj.db.task_estimate.find_one({"name": "Add feat 1"})
            # assert task_estimate is not None

            assert task_estimate["description"] == "for iter 2"
            assert task_estimate["complexity"] == 40
            assert task_estimate["size"] == 4
            assert task_estimate["task_type"] == "development"
            assert task_estimate["task_status"] == "pending"

    def test_edit_task_estimate(self, app_obj, test_client, db_obj: PyMongo):
        app = app_obj
        acc_login = {
            "email": "g@g.com",
            "password": "1234",
        }
        task_edit_data = {
            "name": "Add feat 1",
            "description": "for iter 2",
            "complexity": 40,
            "size": 6,
            "task_type": "development",
            "task_status": "pending",
        }
        with app.app_context():
            response: Response = test_client.post("/login", data=acc_login)
            # print(response.data)
            result = db_obj.db.task_estimate.find_one({"name": "Add feat 1"})
            task_id = str(result["_id"])
            print(task_id)
            assert result["size"] == 4
            response: Response = test_client.post(
                f"/edit_task/{task_id}", data=task_edit_data
            )
            # print(response.data)

            assert response.status_code == 302
            task_estimate = db_obj.db.task_estimate.find_one({"name": "Add feat 1"})
            # assert task_estimate is not None

            assert task_estimate["description"] == "for iter 2"
            assert task_estimate["complexity"] == 40
            assert task_estimate["size"] == 6
            assert task_estimate["task_type"] == "development"
            assert task_estimate["task_status"] == "pending"

    def test_delete_task_estimate(self, app_obj, test_client, db_obj: PyMongo):
        app = app_obj
        acc_login = {
            "email": "g@g.com",
            "password": "1234",
        }
        task_delete_data = {"is_delete": "yes"}

        task_delete_data_no = {"is_delete": "no"}
        with app.app_context():
            response: Response = test_client.post("/login", data=acc_login)
            # print(response.data)
            result = db_obj.db.task_estimate.find_one({"name": "Add feat 1"})
            task_id = str(result["_id"])
            print(task_id)
            assert result["description"] == "for iter 2"

            # For No
            response: Response = test_client.post(
                f"/delete_task/{task_id}", data=task_delete_data_no
            )
            # print(response.data)
            assert response.status_code == 302
            task_estimate = db_obj.db.task_estimate.find_one({"name": "Add feat 1"})
            assert task_estimate is not None
            assert result["description"] == "for iter 2"

            # For Yes
            response: Response = test_client.post(
                f"/delete_task/{task_id}", data=task_delete_data
            )
            # print(response.data)
            assert response.status_code == 302

            task_estimate = db_obj.db.task_estimate.find_one({"name": "Add feat 1"})
            assert task_estimate is None
