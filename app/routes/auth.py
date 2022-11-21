from flask import (
    Blueprint,
    render_template,
    url_for,
    redirect,
    flash,
    request,
)
from flask_login import login_user, current_user
from werkzeug.urls import url_parse
from app.forms import LoginForm
from app.models.usuarios import User

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index.index"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("no_existe"))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get("next")
        print(type(next_page))
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for("index.index")
        return redirect(next_page)
    return render_template("login.html", title="Sign In", form=form)
