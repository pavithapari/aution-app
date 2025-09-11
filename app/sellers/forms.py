from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange,Email

class SellerReg_form(FlaskForm):
    name=StringField("Name",validators=[DataRequired()])
    email=StringField("Email",validators=[DataRequired(),Email()])
    submit=SubmitField('Register')


class SellerLog_form(FlaskForm):
    email=StringField("Email",validators=[DataRequired(),Email()])
    submit=SubmitField('Login')


class obj_form(FlaskForm):
    name = StringField("Object Name", validators=[DataRequired(), Length(min=2, max=20)])
    image = StringField("Image URL", validators=[DataRequired(), Length(max=100)])
    price = IntegerField("Base Price", validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField("Add Object")
