from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField
from wtforms.validators import DataRequired


class SelectYear(FlaskForm):
    year = SelectField(label="选择年份", validators=[DataRequired()], choices=[(0,'请选择年份'),(2014,'2014'), (2015,'2015')
        , (2016,'2016'), (2017,'2017'), (2018,'2018'), (2019,'2019')],coerce=int)
    submit = SubmitField('提交')
