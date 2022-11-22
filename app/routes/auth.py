from flask import Blueprint, redirect, flash, url_for, request, render_template
from flask_login import current_user, login_user, logout_user
from app.models.usuarios import User
from app.forms import LoginForm
from werkzeug.urls import url_parse

auth_router = Blueprint("auth", __name__)


@auth_router.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index.index"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("index.no_existe"))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get("next")
        print(type(next_page))
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for("index.index")
        return redirect(next_page)
    return render_template("login.html", title="Sign In", form=form)


@auth_router.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index.index"))
