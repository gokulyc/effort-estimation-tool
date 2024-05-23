from flask import Flask
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/effort_estimation_proj")


def create_flask_app():
    app = Flask(__name__)
    app.config["MONGO_URI"] = MONGO_URI
    app.config["SECRET_KEY"] = "secret123!@#"
    app.config["JWT_SECRET_KEY"] = "jwt-secret-string-!@#"
    app.config["JWT_TOKEN_LOCATION"] = ["headers", "cookies", "json", "query_string"]
    app.config["JWT_COOKIE_CSRF_PROTECT"] = False
    return app
