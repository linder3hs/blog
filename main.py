from flask import render_template, flash, redirect, url_for, request
from flask_login import (
    LoginManager,
    logout_user,
    login_required,
    current_user,
    login_user,
)
from werkzeug.urls import url_parse
from app import create_app
from app.forms import LoginForm, PostForm, CommentForm
from app.db import db

from app.models.usuarios import AnonymousUser, User
from app.models.posts import Post
from app.models.roles import Role
from app.utils.utils import Permission
from app.utils.decorator import admin_required, permission_required


app = create_app()

login = LoginManager(app)
login.login_view = "login"
login.anonymous_user = AnonymousUser


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route("/")
@login_required
def index():
    posts = Post.query.all()
    return render_template("indexCss.html", posts=posts)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

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
            next_page = url_for("index")
        return redirect(next_page)
    return render_template("login.html", title="Sign In", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/no-existe")
def no_existe():
    return render_template("nouser.html")


@app.route("/admin")
@login_required
@admin_required
def for_admins_only():
    return "Para administradores!"


@app.route("/moderate")
@login_required
@permission_required(Permission.MODERATE)
def for_moderators_only():
    return "Para moderadores!"


@app.route("/insert")
def insert():
    u = User(username="linder2", email="linder02@gmail.com")
    u.set_password("linder340")

    role = Role(name="User", users=[u])
    role.add_permission(Permission.WRITE)

    db.session.add(u)
    db.session.commit()

    return "Insertado"


@app.route("/post", methods=["GET", "POST"])
@login_required
def post():
    post_form = PostForm()

    if current_user.can(Permission.WRITE) and post_form.validate_on_submit():
        new_post = Post(body=post_form.body.data, user_id=current_user.id)
        db.session.add(new_post)
        db.session.commit()

        return redirect(url_for("index"))

    return render_template("post.html", post_form=post_form)


@app.route("/post/<id>")
def post_detail(id):
    comment_form = CommentForm()
    
    post = Post.query.filter_by(id=id).first()

    context = {
        "comment_form": comment_form,
        "post": post
    }

    return render_template("post-detail.html", **context)


@app.route("/profile")
def profile():
    posts_by_current_user = Post.query.filter_by(user_id=current_user.id).count()
    # posts_by_user = User.query.filter_by(id=current_user.id).first()
    # print(posts_by_user.posts)
    return render_template("profile.html", post_count=posts_by_current_user)


db.init_app(app)
with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run()
