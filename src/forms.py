from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField
from wtforms.validators import InputRequired, Email
from models import TASK_SIZES, COMPLEXITY_CHOICES, TaskType, TaskStatus


complexity_select_options = [
    (value, key.capitalize()) for key, value in COMPLEXITY_CHOICES.items()
]
task_type_select_options = [
    (t_type.value, t_type.value.capitalize()) for t_type in TaskType
]
task_status_select_options = [(status.value, status.name) for status in TaskStatus]

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[InputRequired(), Email()])
    password = PasswordField("Password", validators=[InputRequired()])


class RegisterForm(FlaskForm):
    name = StringField("Name", validators=[InputRequired()])
    email = StringField("Email", validators=[InputRequired(), Email()])
    password = PasswordField("Password", validators=[InputRequired()])


class AddTaskForm(FlaskForm):
    name = StringField("Name", validators=[InputRequired()])
    description = TextAreaField("Description", validators=[InputRequired()])
    complexity = SelectField(
        "Complexity", choices=complexity_select_options, default="easy"
    )
    size = SelectField(
        "TaskSize", choices=[(k, v) for k, v in TASK_SIZES.items()], default=2
    )
    task_type = SelectField(
        "Task Type",
        choices=task_type_select_options,
        default=TaskType.development.value,
    )
    task_status = SelectField(
        "Task Status",
        choices=task_status_select_options,
        default=TaskStatus.Pending.value,
    )


class EditTaskForm(AddTaskForm):
    pass


class DeleteTaskForm(FlaskForm):
    is_delete = SelectField(
        "Do you want to delete task? ",
        choices=[("yes", "Yes"), ("no", "No")],
        default="no",
    )
