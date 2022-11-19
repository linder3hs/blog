from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField("Nombre de usuario", validators=[DataRequired()])
    password = PasswordField("Contraseña", validators=[DataRequired()])
    remember_me = BooleanField("Recuérdame")
    submit = SubmitField("Ingresar")


class PostForm(FlaskForm):
    body = TextAreaField("Texto de blog", validators=[DataRequired()])
    submit = SubmitField("Crear blog")


class CommentForm(FlaskForm):
    comment = TextAreaField("Escribe tu comentario", validators=[DataRequired()])
    submit = SubmitField("Enviar comentario")
