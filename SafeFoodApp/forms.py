from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, SubmitField, DecimalField, TextAreaField, FileField, FloatField, DateTimeField
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


class TemperatureCheckForm(FlaskForm):
    food_item = StringField("Food Item", validators=[DataRequired(), length(max=20)])
    temperature = StringField("Core Temperature", validators=[DataRequired()])
    employee_name = StringField("Name", validators=[DataRequired(), length(max=25)])
    comment = StringField("Comment", validators=[length(max=100)])
    submit = SubmitField("ADD RECORD")


class DeliveryTemperatureForm(FlaskForm):
    supplier_name = StringField("Supplier Name", validators=[DataRequired(), length(max=20)])
    food_item = StringField("Food Item", validators=[DataRequired(), length(max=20)])
    food_item_temperature = StringField("Food Item Core Temperature", validators=[DataRequired(), length(max=20)])
    high_risk_food_item = StringField("High-Risk Food Item", validators=[DataRequired(), length(max=20)])
    high_risk_food_item_temperature = StringField("High-Risk Food Item Temperature", validators=[DataRequired(), length(max=20)])
    employee_name = StringField("Name", validators=[DataRequired(), length(max=25)])
    comment = StringField("Comment", validators=[length(max=100)])
    submit = SubmitField("ADD RECORD")


class MenuForm(FlaskForm):
    menu_item = StringField("Menu Item", validators=[DataRequired(), length(max=20)])
    ingredients = TextAreaField("Ingredients", validators=[DataRequired()])
    method = TextAreaField("Method", validators=[DataRequired()])
    image = FileField("Add image")
    submit = SubmitField("ADD RECORD")


class WastageForm(FlaskForm):
    food_item = StringField("Food Item", validators=[DataRequired(), length(max=20)])
    quanity = FloatField("Quanity", validators=[DataRequired()])
    unit = StringField("Unit e.g (kg, g)", validators=[DataRequired()]) # maybe this should be a drop down thing
    reason = StringField("Reason", validators=[DataRequired()])
    name = StringField("Name", validators=[DataRequired()] )
    submit = SubmitField("ADD RECORD")


class CoolingForm(FlaskForm):
    food_item = StringField("Food Item", validators=[DataRequired(), length(max=20)])
    cooling_method = StringField("Cooling Method", validators=[DataRequired(), length(max=20)])
    time_started_cooling = DateTimeField("Time Started Cooling", validators=[DataRequired()])
    temperature = StringField("Temperature after 90 mins", validators=[DataRequired(), length(max=20)])
    submit = SubmitField("ADD RECORD")


class CleaningChecksForm(FlaskForm):
    pass
    
class AuditForm(FlaskForm):
    pass

class ClosingChecksForm(FlaskForm):
    pass

class OpeningChecksForm(FlaskForm):
    pass




       
