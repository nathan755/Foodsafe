from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, SubmitField, DecimalField
from wtforms.validators import DataRequired, length, Email, EqualTo, ValidationError
from SafeFoodApp.models import User

class RegistrationForm(FlaskForm):

    username = StringField("Username", validators=[DataRequired(), length(max=20)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    company_name = StringField("Company Name", validators=[DataRequired(), length(max=50)])
    password = PasswordField("Password", validators= [DataRequired(), length(min=6)])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(),EqualTo("password")])
    submit = SubmitField("Register")
    
    def validate_username(self, username):
        """
        username:
        User : User table of the database form models.py
        Returns: Validation message underneath form field
        """
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Username Unavailable")

class LoginForm(FlaskForm):

    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators= [DataRequired(), length(min=6)])
    submit = SubmitField("Login")
    
class FridgeFreezerTempForm(FlaskForm):
    
    unit_name = StringField("Fridge/Freezer Name",validators=[DataRequired(), length(max=15)])
    unit_type = StringField("Unit Type", validators=[DataRequired(), length(max=15)])
    temperature = StringField("Temperature", validators=[DataRequired()])
    employee_name = StringField("Name", validators=[DataRequired(), length(max=25)])
    comment = StringField("Comment", validators=[length(max=100)])
    submit = SubmitField("ADD RECORD")

    def validate_unit_type(self, unit_type):
        #find out why we cant check fridge and freezer
        if unit_type.data.lower() != "fridge":
            raise ValidationError("Unit type must be a 'fridge', or 'freezer'")
    
    def validate_temperature(self,temperature):
        pass

    







       
