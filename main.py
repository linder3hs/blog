from flask import render_template
from flask_login import (
    LoginManager,
    login_required,
    current_user,
)
from app import create_app
from app.db import db

from app.models.usuarios import AnonymousUser, User
from app.models.posts import Post
from app.models.roles import Role
from app.utils.utils import Permission


app = create_app()


login = LoginManager(app)
login.login_view = "auth.login"
login.anonymous_user = AnonymousUser


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route("/no-existe")
def no_existe():
    return render_template("nouser.html")


@app.route("/admin")
@login_required
# @admin_required
def for_admins_only():
    return "Para administradores!"


@app.route("/moderate")
@login_required
# @permission_required(Permission.MODERATE)
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
