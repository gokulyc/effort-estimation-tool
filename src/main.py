import os
from flask import render_template, redirect, url_for, request, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.exceptions import NotFound, HTTPException, BadRequest
from flask_jwt_extended import (
    JWTManager,
    current_user,
    jwt_required,
    create_access_token,
    set_access_cookies,
    unset_jwt_cookies,
    get_jwt,
)
from flask_pymongo import PyMongo, ObjectId
from models import User, TaskEstimation
from forms import RegisterForm, LoginForm, AddTaskForm, EditTaskForm, DeleteTaskForm
from config import create_flask_app
from utils import calculate_estimated_metrics

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
    if request.method == "POST":
        if form.validate_on_submit():
            hashed_password = generate_password_hash(
                form.password.data, method="scrypt"
            )
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
    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    message = request.args.get("message")
    form = LoginForm()
    if request.method == "POST":
        if form.validate_on_submit():
            user_result = mongo.db.auth_users.find_one({"email": request.form["email"]})
            if user_result is None:
                raise HTTPException("User/ Password invalid.")
            user = User(**user_result)
            if check_password_hash(user.password, request.form["password"]):
                additional_claims = {**user.get_data(ignore_fields=["password"])}
                # print(f"{additional_claims=}")
                access_token = create_access_token(
                    identity={"email": user.email},
                    additional_claims=additional_claims,
                )
                response = redirect("/dashboard")
                set_access_cookies(response, access_token)
                return response
        else:
            print(form.errors)
            return render_template("login.html", form=form, message=message)
    return render_template("login.html", form=form, message=message)


@app.route("/dashboard")
@jwt_required()
def dashboard():
    jwt_payload = get_jwt()
    print(f"{jwt_payload=}")
    account: User = mongo.db.auth_users.find_one_or_404(
        {"_id": ObjectId(jwt_payload["id"])}
    )
    return render_template("dashboard.html", account=User(**account))


@app.route("/add_task", methods=["GET", "POST"])
@jwt_required()
def add_task():
    jwt_payload = get_jwt()
    form: AddTaskForm = AddTaskForm()
    if request.method == "POST":
        if form.validate_on_submit():
            form_data = form.data
            result = mongo.db.task_estimate.insert_one(
                {
                    "name": form_data["name"],
                    "description": form_data["description"],
                    "complexity": int(form_data["complexity"]),
                    "size": int(form_data["size"]),
                    "task_type": form_data["task_type"],
                    "task_status": form_data["task_status"],
                    "user_id": jwt_payload["id"],
                }
            )
            task_id = result.inserted_id
            print(f"Task added : {str(task_id)}")
            flash("Task Added")
            return redirect("/list_tasks")
        else:
            print(form.errors)
        return render_template("add_task_estimate.html", form=form, request_type="add")
    return render_template("add_task_estimate.html", form=form, request_type="add")


@app.route("/edit_task/<string:task_id>", methods=["GET", "POST"])
@jwt_required()
def edit_task(task_id):
    jwt_payload = get_jwt()
    task_result = mongo.db.task_estimate.find_one(
        {"_id": ObjectId(task_id), "user_id": jwt_payload["id"]}
    )
    if task_result is None:
        raise NotFound("Task not found.")
    task = TaskEstimation(**task_result).get_data(ignore_fields=["id", "user_id"])
    form: EditTaskForm = EditTaskForm(**task)
    if request.method == "POST":
        if form.validate_on_submit():
            form_data = form.data
            result = mongo.db.task_estimate.update_one(
                filter={"_id": ObjectId(task_id)},
                update={
                    "$set": {
                        "name": form_data["name"],
                        "description": form_data["description"],
                        "complexity": int(form_data["complexity"]),
                        "size": int(form_data["size"]),
                        "task_type": form_data["task_type"],
                        "task_status": form_data["task_status"],
                    }
                },
            )
            task_id = result.raw_result
            print(f"Task updated : {str(task_id)}")
            flash("Task updated")
            return redirect("/list_tasks")
        else:
            print(form.errors)
            return render_template(
                "add_task_estimate.html", form=form, request_type="edit"
            )
    return render_template("add_task_estimate.html", form=form, request_type="edit")


@app.route("/delete_task/<string:task_id>", methods=["GET", "POST"])
@jwt_required()
def delete_task(task_id):
    jwt_payload = get_jwt()
    task_result = mongo.db.task_estimate.find_one(
        {"_id": ObjectId(task_id), "user_id": jwt_payload["id"]}
    )
    if task_result is None:
        raise NotFound("Task not found.")
    form: DeleteTaskForm = DeleteTaskForm()
    if request.method == "POST":
        if form.validate_on_submit():
            form_data = form.data
            if form_data["is_delete"] == "yes":
                result = mongo.db.task_estimate.delete_one(
                    filter={"_id": ObjectId(task_id), "user_id": jwt_payload["id"]}
                )
                deleted_count = result.deleted_count
                print(f"Task deleted count : {deleted_count}")
                flash("Task deleted")
                return redirect("/list_tasks")
            else:
                flash("Task deletion cancelled.")
                return redirect("/list_tasks")
        else:
            print(form.errors)
    return render_template("delete_task_estimate.html", form=form)


@app.route("/list_tasks", methods=["GET"])
@jwt_required()
def list_tasks():
    jwt_payload = get_jwt()
    list_tasks_result = mongo.db.task_estimate.find({"user_id": jwt_payload["id"]})
    list_tasks = [
        TaskEstimation(**task).get_data(ignore_fields=[], convert_task_complexity=True)
        for task in list_tasks_result
    ]
    # print(list_tasks)
    return render_template("list_task_estimate.html", tasks=list_tasks)


@app.route("/fetch_time_estimate", methods=["POST"])
def fetch_time_estimate():
    json_data = request.json
    task_size = json_data.get("task_size")
    task_type = json_data.get("task_type")

    if task_size is None or task_type is None:
        raise BadRequest("task_size/ task_type has invalid value.")

    records = mongo.db.task_estimate.find(
        {"size": int(task_size), "task_type": task_type}
    )
    list_tasks = [
        TaskEstimation(**rec).get_data(
            ignore_fields=["id", "name", "description", "complexity", "task_estimate"]
        )
        for rec in records
    ]
    list_tasks_length = len(list_tasks)
    if list_tasks_length == 0:
        return jsonify({"message": "Not enough data"})
    avg_task_size = round(
        sum(map(lambda x: x["size"], list_tasks)) / len(list_tasks), 2
    )
    print(f"{list_tasks=}")
    print(f"{avg_task_size=}")
    result = calculate_estimated_metrics(task_type, int(task_size))
    # result = {}
    return jsonify({"message": "ok", "data": result})


@app.route("/logout", methods=["GET"])
def logout_with_cookies():
    response = redirect("/")
    unset_jwt_cookies(response)
    return response


if __name__ == "__main__":
    from sample_data import AUTH_USERS_DEMO_DATA, TASK_ESTIMATIONS_DEMO_DATA

    mongo.init_app(app)
    # mongo.db.auth_users.drop()
    # mongo.db.task_estimate.drop()
    try:
        ...
        # mongo.db.auth_users.create_index("email", unique=True)
        # result = mongo.db.auth_users.insert_many(AUTH_USERS_DEMO_DATA)
        # print(f"{result.inserted_ids}")

        # user = mongo.db.auth_users.find_one({"email": "g@g.com"})
        # print(user)
        # TASK_DATA_W_User = map(
        #     lambda x: {**x, **{"user_id": str(user["_id"])}}, TASK_ESTIMATIONS_DEMO_DATA
        # )
        # result = mongo.db.task_estimate.insert_many(TASK_DATA_W_User)
        # print(f"{result.inserted_ids}")
    except Exception as e:
        print(e)
    app.run(host=os.getenv("BACKEND_FLASK_HOST", "127.0.0.1"), debug=True)
