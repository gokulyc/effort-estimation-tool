from flask import render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.exceptions import NotFound, HTTPException
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
from flask_pymongo import PyMongo, ObjectId

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
    user = mongo.db.auth_users.find_one({"email": identity["email"]})
    return user


@app.route("/")
def index():
    return render_template("home.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    # print(form.data)
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method="scrypt")
        result = mongo.db.auth_users.insert_one(
            {
                "name": form.name.data,
                "email": form.email.data,
                "password": hashed_password,
            }
        )
        user_id = result.inserted_id
        print(f"User added : {str(user_id)}")
        flash("User registered..., Please login.")
        return redirect(url_for("dashboard"))
    else:
        print(form.errors)
    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    message = request.args.get("message")
    if request.method == "POST":
        user_result = mongo.db.auth_users.find_one({"email": request.form["email"]})
        if user_result is None:
            raise HTTPException("User/ Password invalid.")
        user = User(**user_result)
        if check_password_hash(user.password, request.form["password"]):
            additional_claims = {**user.get_data(ignore_fields=["password"])}
            print(f"{additional_claims=}")
            access_token = create_access_token(
                identity={"email": user.email},
                additional_claims=additional_claims,
            )
            response = redirect("/dashboard")
            set_access_cookies(response, access_token)
            return response
    return render_template("login.html", message=message)


@app.route("/dashboard")
@jwt_required()
def dashboard():
    account: User = mongo.db.auth_users.find_one_or_404(
        {"_id": ObjectId("664ed9f5df4b803e7381907d")}
    )
    return render_template("dashboard.html", account=User(**account))


@app.route("/logout", methods=["GET"])
def logout_with_cookies():
    response = redirect("/")
    unset_jwt_cookies(response)
    return response


if __name__ == "__main__":
    mongo.init_app(app)
    app.run(debug=True)
