
from flask_wtf import FlaskForm

from wtforms import StringField, PasswordField, FloatField, IntegerField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    username = StringField('姓名', validators=[DataRequired(message='用户名'), Length(1, 63)])
    password = PasswordField('密码', validators=[DataRequired(message='密码不能为空'), Length(1, 31)])


class BetOnEtherCreateForm(FlaskForm):
    home = StringField('home', validators=[DataRequired()])
    home_image = StringField('home_image', validators=[DataRequired()])
    visiting = StringField('visiting', validators=[DataRequired()])
    visiting_image = StringField('visiting_image', validators=[DataRequired()])
    opening_time = StringField('opening_time', validators=[DataRequired()])
    league = StringField('opening_time', validators=[DataRequired()])
    round = StringField('round', validators=[DataRequired()])
    # win_odds = FloatField('win_odds', validators=[DataRequired()])
    # draw_odds = FloatField('draw_odds', validators=[DataRequired()])
    # lose_odds = FloatField('lose_odds', validators=[DataRequired()])


class BetOnEtherDeployForm(FlaskForm):
    earnest_money = IntegerField('earnest_money', validators=[DataRequired()])
    win_odds = FloatField('win_odds', validators=[DataRequired()])
    draw_odds = FloatField('draw_odds', validators=[DataRequired()])
    lose_odds = FloatField('lose_odds', validators=[DataRequired()])
