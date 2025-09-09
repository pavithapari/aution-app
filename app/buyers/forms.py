from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from app.models import Buyers  # Replace with your actual model import

class BuyerReg_form(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    con_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_name(self, field):
        existing_user = Buyers.query.filter_by(username=field.data).first()
        if existing_user:
            raise ValidationError("Username already exists. Please choose another.")

    def validate_email(self, field):
        existing_email = Buyers.query.filter_by(email=field.data).first()
        if existing_email:
            raise ValidationError("Email already registered. Try logging in.")




class BuyerLog_form(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField('Login')

    def validate_email(self, field):
        buyer = Buyers.query.filter_by(email=field.data).first()
        if not buyer:
            raise ValidationError("Email not found. Please register first.")