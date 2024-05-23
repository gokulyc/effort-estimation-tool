from flask import render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.exceptions import NotFound
from flask_jwt_extended import (
    JWTManager,
    current_user,
    jwt_required,
    create_access_token,
    set_access_cookies,
    unset_jwt_cookies,
)

from models import User
from forms import RegisterForm
from config import create_flask_app
import os
from flask_pymongo import PyMongo

app = create_flask_app()

mongo = PyMongo()

jwt = JWTManager(app)


@jwt.unauthorized_loader
def custom_unauthorized_response(_err):
    return redirect(url_for("login", message="AnonymousUser"))


@jwt.expired_token_loader
def my_expired_token_callback(jwt_header, jwt_payload):
    return redirect(url_for("login", message="TokenExpired"))


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter(User.email == identity["email"]).one_or_none()

@app.route("/")
def index():
    return render_template("home.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    # print(form.data)
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method="scrypt")
        result = mongo.db.auth_users.insert_one({"name": form.name.data,
                                        "email": form.email.data,
                                        "password": hashed_password})
        user_id = result.inserted_id
        print(f"User added : {str(user_id)}")
        flash("User registered..., Please login.")
        return redirect(url_for("dashboard"))
    else:
        print(form.errors)
    return render_template("register.html", form=form)

@app.route("/dashboard")
# @jwt_required()
def dashboard():
    # account: User = User.query.filter(User.email == current_user.email).one().to_dict()
    # return render_template("dashboard.html", account=account)
    return render_template("dashboard.html")

if __name__ == "__main__":
    mongo.init_app(app)
    app.run(debug=True)