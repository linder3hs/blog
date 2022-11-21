from flask import Blueprint, render_template, url_for, redirect
from flask_login import login_required, logout_user
from app.models.posts import Post

index_p = Blueprint("index", __name__)


@index_p.route("/")
@login_required
def index():
    posts = Post.query.all()
    return render_template("indexCss.html", posts=posts)


@index_p.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index.index"))
