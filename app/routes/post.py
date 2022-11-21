from flask import Blueprint, render_template, url_for, redirect, g, jsonify, request
from flask_login import login_required, current_user
from app.models.posts import Post
from app.forms import PostForm, CommentForm
from app.db import db
from app.utils.utils import Permission

post_router = Blueprint("post", __name__)


@post_router.route("/post", methods=["GET", "POST"])
@login_required
def post():
    post_form = PostForm()

    if current_user.can(Permission.WRITE) and post_form.validate_on_submit():
        new_post = Post(body=post_form.body.data, user_id=current_user.id)
        db.session.add(new_post)
        db.session.commit()

        return redirect(url_for("index.index"))

    return render_template("post.html", post_form=post_form)


@post_router.route("/post/<id>")
def post_detail(id):
    comment_form = CommentForm()

    post = Post.query.filter_by(id=id).first()

    context = {"comment_form": comment_form, "post": post}

    return render_template("post-detail.html", **context)


@post_router.route("/postJson/", methods=["POST"])
def new_post():
    post = request.json
    new_post = Post(body=post["body"], user_id=post["user_id"])
    db.session.add(new_post)
    db.session.commit()
    return (
        jsonify(new_post.to_json()),
        201,
        {"Location": url_for("post.post_detail", id=post["user_id"])},
    )
