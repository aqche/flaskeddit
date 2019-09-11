from flask import flash, redirect, render_template, session, url_for
from flask_login import current_user, login_required

from flaskeddit.auth import auth_blueprint, auth_service
from flaskeddit.auth.forms import LoginForm, RegisterForm


@auth_blueprint.route("/register", methods=["GET", "POST"])
def register():
    """Route for registering new users."""
    if current_user.is_authenticated:
        return redirect(url_for("feed.feed"))
    form = RegisterForm()
    if form.validate_on_submit():
        auth_service.register_user(form.username.data, form.password.data)
        flash("Successfully registered.", "primary")
        return redirect(url_for("auth.login"))
    return render_template("register.jinja2", form=form)


@auth_blueprint.route("/login", methods=["GET", "POST"])
def login():
    """Route for logging in users."""
    if current_user.is_authenticated:
        return redirect(url_for("feed.feed"))
    form = LoginForm()
    if form.validate_on_submit():
        login_successful = auth_service.log_in_user(
            form.username.data, form.password.data
        )
        if login_successful:
            flash("Successfully logged in.", "primary")
            if session.get("next"):
                return redirect(session.get("next"))
            return redirect(url_for("feed.feed"))
        else:
            flash("Login Failed", "danger")
            return redirect(url_for("auth.login"))
    return render_template("login.jinja2", form=form)


@auth_blueprint.route("/logout", methods=["POST"])
@login_required
def logout():
    """Route for logging out users."""
    auth_service.log_out_user()
    flash("Successfully logged out.", "primary")
    return redirect(url_for("auth.login"))
