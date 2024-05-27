from src.models import User, TaskEstimation
import pytest
from werkzeug.security import generate_password_hash
from src.main import app, mongo, ObjectId
import os

def add_accounts_data(mongo):
    try:
        mongo.db.auth_users.insert_many(
            [
                {
                    "name": "Gokul",
                    "email": "g@g.com",
                    "password": generate_password_hash("1234", method="scrypt"),
                },
                {
                    "name": "Ravi",
                    "email": "ravi@g.com",
                    "password": generate_password_hash("5678", method="scrypt"),
                },
            ]
        )
        print("Users added!")
    except Exception as e:
        print(f"Unable to add User : {e}")


@pytest.fixture(scope="class")
def app_obj():
    app.config.update(
        {
            "TESTING": True,
            "MONGO_URI": os.getenv("MONGO_URI", "mongodb://localhost:27017/effort_estimation_proj_testing"),
            "WTF_CSRF_ENABLED": False,
        }
    )

    yield app


@pytest.fixture(scope="class")
def db_obj(app_obj):
    mongo.init_app(app_obj)
    with app_obj.app_context():
        try:
            add_accounts_data(mongo)
        except Exception as e:
            print(e)
    yield mongo
    try:
        with app_obj.app_context():
            mongo.db.auth_users.drop()
            mongo.db.task_estimate.drop()
    except Exception as e:
        print(e)
        print("unable to drop tables.")


@pytest.fixture
def test_client(app_obj):
    app = app_obj
    return app.test_client()
