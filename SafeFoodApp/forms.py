import datetime
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, SubmitField, DecimalField, TextAreaField, FileField, FloatField, DateTimeField, IntegerField, TimeField
from wtforms.validators import DataRequired, length, Email, EqualTo, ValidationError
from SafeFoodApp.models import User


def validate_unit_type(form, field):
    
    if field.data.lower() != "fridge":
        if field.data.lower() != "freezer":
            raise ValidationError("Unit type must be a 'fridge', or 'freezer'")

def check_time(time_1,  time_2, duration):
    """
    time_1 = datetime object 
    time_2 = datetime object
    duration = float (hours duration to be checked)
    Function returns True if the difference between time_1 and time_2 is < duration.
    """
    difference = time_1 - time_2
    difference_in_hours = difference.total_seconds()/3600
	
    if difference_in_hours > duration:
        return False

    else:
        return True


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
    unit_type = StringField("Unit Type", validators=[DataRequired(), length(max=15), validate_unit_type])
    temperature = IntegerField("Temperature", validators=[DataRequired()])
    employee_name = StringField("Name", validators=[DataRequired(), length(max=25)])
    comment = StringField("Comment", validators=[length(max=100)])
    submit = SubmitField("ADD RECORD")

    def validate(self):

        """
        Overides validate in Form (allows us to check multiple fields for validation.)
        returns False if the form does not pass validation.
        else returns True.
        """
        if not FlaskForm.validate(self):
            # If the default validation fails, this returns False
            return False
        
        if self.unit_type.data.lower() == "fridge":
            if not self.comment.data:
                if self.temperature.data > 8:
                    self.temperature.errors.append("Temp too high, check again shortly. Alternativly, submit form with a comment")
                    return False

        elif self.unit_type.data.lower() == "freezer":
            if not self.comment.data:
                if self.temperature.data > -18:
                    self.temperature.errors.append("Temp too high, check again shortly. Alternativly, submit form with a comment")
                    return False
        
        return True


class TemperatureCheckForm(FlaskForm):
    food_item = StringField("Food Item", validators=[DataRequired(), length(max=20)])
    temperature = StringField("Core Temperature", validators=[DataRequired()])
    employee_name = StringField("Name", validators=[DataRequired(), length(max=25)])
    comment = StringField("Comment", validators=[length(max=100)])
    submit = SubmitField("ADD RECORD")


class DeliveryTemperatureForm(FlaskForm):
    supplier_name = StringField("Supplier Name", validators=[DataRequired(), length(max=20)])
    food_item = StringField("Food Item", validators=[DataRequired(), length(max=20)])
    food_item_temperature = IntegerField("Food Item Core Temperature", validators=[DataRequired()])
    high_risk_food_item = StringField("High-Risk Food Item", validators=[DataRequired(), length(max=20)])
    high_risk_food_item_temperature = IntegerField("High-Risk Food Item Temperature", validators=[DataRequired()])
    employee_name = StringField("Name", validators=[DataRequired(), length(max=25)])
    comment = StringField("Comment", validators=[length(max=100)])
    submit = SubmitField("ADD RECORD")

    def validate(self):

        """
        same as custom validation in FrideFreezerTempForm.
        """

        if not FlaskForm.validate(self):
            # If the default validation fails, this returns False
            return False
        
        if self.food_item_temperature.data > 8:
            if not self.comment.data:
                self.food_item_temperature.errors.append("Temperature too high, reject delivery and add a comment")
                return False
        
        elif self.high_risk_food_item_temperature.data > 8:
            if not self.comment.data:
                self.high_risk_food_item_temperature.errors.append("Temperature too high, reject delivery and add a comment")
                return False
        
        return True


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
    time_started = DateTimeField("Time Started Cooling", validators=[DataRequired()])
    temperature = IntegerField("Temperature after 90 mins", validators=[DataRequired()])
    comment = StringField("Comment", validators=[length(max=100)])
    submit = SubmitField("ADD RECORD")

    def validate(self):

        """
        Overides validate in Form (allows us to check multiple fields for validation.)
        returns False if the form does not pass validation.
        else returns True. 
        """
        if not FlaskForm.validate(self):
            # If the default validation fails, this returns False
            return False
        current_time = datetime.datetime.now()

        if not check_time(current_time, self.time_started.data, 1.5) and not self.comment.data:
            self.temperature.errors.append("Food must be cooled to less than 8 degrees within 90 mins, enter a comment to submit record")
            return False

        elif check_time(current_time, self.time_started.data, 1.5) and self.temperature.data > 8:
            self.temperature.errors.append("Temperature too high, check again later")
            return False
        
        else:
            return True
            
        
            

        
        


class CleaningChecksForm(FlaskForm):
    pass
    
class AuditForm(FlaskForm):
    pass

class ClosingChecksForm(FlaskForm):
    pass

class OpeningChecksForm(FlaskForm):
    pass




       
