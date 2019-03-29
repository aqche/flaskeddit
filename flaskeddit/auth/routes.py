from flask import flash, redirect, render_template
from flask_login import current_user, login_required, login_user, logout_user

from flaskeddit import bcrypt, db
from flaskeddit.auth import auth_blueprint
from flaskeddit.auth.forms import LoginForm, RegisterForm
from flaskeddit.models import User


@auth_blueprint.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect("/")
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        user = User(username=form.username.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash("Successfully Registered", "primary")
        return redirect("/login")
    return render_template("register.jinja2", form=form)


@auth_blueprint.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect("/")
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash("Successfully Logged In", "primary")
            return redirect("/")
        else:
            flash("Login Failed", "danger")
            return redirect("/login")
    return render_template("login.jinja2", form=form)


@auth_blueprint.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return redirect("/login")
