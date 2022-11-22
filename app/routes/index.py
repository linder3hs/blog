from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.utils.decorator import admin_required, permission_required
from app.db import db
from app.models.usuarios import User
from app.models.posts import Post
from app.models.roles import Role
from app.utils.utils import Permission


index_router = Blueprint("index", __name__)


@index_router.route("/")
@login_required
def index():
    posts = Post.query.all()
    return render_template("indexCss.html", posts=posts)


@index_router.route("/no-existe")
def no_existe():
    return render_template("nouser.html")


@index_router.route("/admin")
@login_required
@admin_required
def for_admins_only():
    return "Para administradores!"


@index_router.route("/moderate")
@login_required
@permission_required(Permission.MODERATE)
def for_moderators_only():
    return "Para moderadores!"


@index_router.route("/insert")
def insert():
    u = User(username="linder2", email="linder02@gmail.com")
    u.set_password("linder340")

    role = Role(name="User", users=[u])
    role.add_permission(Permission.WRITE)

    db.session.add(u)
    db.session.commit()

    return "Insertado"


@index_router.route("/profile")
def profile():
    posts_by_current_user = Post.query.filter_by(user_id=current_user.id).count()
    # posts_by_user = User.query.filter_by(id=current_user.id).first()
    # print(posts_by_user.posts)
    return render_template("profile.html", post_count=posts_by_current_user)
