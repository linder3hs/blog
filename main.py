from flask_login import LoginManager
from app import create_app
from app.db import db
from app.models.usuarios import AnonymousUser, User

app = create_app()

login = LoginManager(app)
login.login_view = "auth.login"
login.anonymous_user = AnonymousUser


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


db.init_app(app)
with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run()
