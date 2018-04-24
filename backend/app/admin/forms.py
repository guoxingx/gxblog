
from flask_wtf import FlaskForm

from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length


class AdminLoginForm(FlaskForm):
    username = StringField('姓名', validators=[DataRequired(message='用户名'), Length(1, 63)])
    password = PasswordField('密码', validators=[DataRequired(message='密码不能为空'), Length(1, 31)])
    submit = SubmitField('登录')
