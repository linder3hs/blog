from app.db import db
from datetime import datetime
from wtforms import ValidationError


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def to_json(self):
        json_post = {
            "post_id": self.id,
            "body": self.body,
            "timestamp": self.timestamp,
            "author_id": self.user_id,
        }
        return json_post

    def from_json(self, json_post):
        body = json_post.get("body")
        print("bodyyyyy", body)
        if body is None or body == "":
            raise ValidationError("El post no tiene los datos necesarios")
        return Post(body=body)
