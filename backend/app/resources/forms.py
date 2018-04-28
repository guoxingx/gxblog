
from flask_wtf import FlaskForm

from wtforms import StringField, FloatField
from wtforms.validators import DataRequired


class BetOnEtherCreateForm(FlaskForm):
    home = StringField('home', validators=[DataRequired()])
    visiting = StringField('visiting', validators=[DataRequired()])
    opening_time = StringField('opening_time', validators=[DataRequired()])
    league = StringField('opening_time', validators=[DataRequired()])
    round = StringField('round', validators=[DataRequired()])
    win_odds = FloatField('win_odds', validators=[DataRequired()])
    draw_odds = FloatField('draw_odds', validators=[DataRequired()])
    lose_odds = FloatField('lose_odds', validators=[DataRequired()])
