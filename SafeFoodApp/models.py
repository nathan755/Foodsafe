from SafeFoodApp import db
from SafeFoodApp import login_manager
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    """
    Manage Sessions for us
    example.. 
    user1 = User()
    user1.user_temp_records
    above will return a list of the user fridge/freezer records

    """
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    """Table for website user information
    """
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    company_name = db.Column(db.String(120), unique=False, nullable=False)
    password = db.Column(db.String(60), unique=False, nullable=False)
    user_temp_records = db.relationship('FridgeFreezerTempTable', backref=db.backref('fridge_temp', lazy=True))
    user_cooking_temp_records = db.relationship("CookingTemperatureTable", backref=db.backref('cooking_temp', lazy=True))
    user_delivery_temp_records = db.relationship("DeliveryTemperatureTable", backref=db.backref('delivery_temp', lazy=True))
    hot_hold_records = db.relationship("HotHoldTable", backref=db.backref('hot_hold', lazy=True))
    menu_spec = db.relationship("MenuTable", backref=db.backref('menu_spec', lazy=True))
    wastage = db.relationship("WastageTable", backref=db.backref('wastage', lazy=True))
    menu_spec = db.relationship("FoodCoolingTable", backref=db.backref('cooling', lazy=True))
    
    def __repr__(self):
        return f"ID: {self.id}, User:{self.username} , email:{self.email}, company_name:{self.company_name}"


class FridgeFreezerTempTable(db.Model):
    """
    Fridge and Freezer Temperature table.
    company_id will return the user id. If we want to get the whole user object instead use 
    FridgeFreezerTempTable.backref 
    To accsess the users fridge/freezer records FridgeFreezerTempTable.backref.user_temp_records!
    """
    id = db.Column(db.Integer, primary_key=True)
    unit_name = db.Column(db.String(50), nullable=False)
    unit_type = db.Column(db.String(50), nullable=False)
    temperature = db.Column(db.String(10), nullable=False)
    employee_name =  db.Column(db.String(50), nullable=False)
    comment =  db.Column(db.String(100), nullable=True)
    company_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    #date_submitted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


class CookingTemperatureTable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    food_item = db.Column(db.String(20), nullable=False)
    temperature = db.Column(db.String(10), nullable=False)
    employee_name =  db.Column(db.String(50), nullable=False)
    comment =  db.Column(db.String(100), nullable=True)
    date_submitted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    company_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)


class DeliveryTemperatureTable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    food_item = db.Column(db.String(20), nullable=False)
    temperature = db.Column(db.String(10), nullable=False)
    high_risk_food_item = db.Column(db.String(20), nullable=False)
    high_risk_temperature = db.Column(db.String(10), nullable=False)
    employee_name =  db.Column(db.String(50), nullable=False)
    comment =  db.Column(db.String(100), nullable=True)
    company_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date_submitted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


class HotHoldTable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    food_item = db.Column(db.String(20), nullable=False)
    temperature = db.Column(db.String(10), nullable=False)
    employee_name =  db.Column(db.String(50), nullable=False)
    comment =  db.Column(db.String(100), nullable=True)
    date_submitted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    company_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class MenuTable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    menu_item = db.Column(db.String(20), nullable=False)
    ingredients = db.Column(db.String(100), nullable=False)
    method = db.Column(db.String(100), nullable=False)
    #image = db.Column(db.String(16), nullable=False)
    date_submitted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    company_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class WastageTable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    food_item = db.Column(db.String(20), nullable=False)
    quanitiy = db.Column(db.String(20), nullable=False)
    unit = db.Column(db.String(20), nullable=False)
    reason = db.Column(db.String(20), nullable=False)
    employee_name = db.Column(db.String(50), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class FoodCoolingTable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    food_item = db.Column(db.String(20), nullable=False)
    cooling_method = db.Column(db.String(20), nullable=False)
    time_started = food_item = db.Column(db.String(20), nullable=False)
    time_ended = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    temperature = db.Column(db.String(10), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


####To do
#MAytbe use class inhertance to make this cleaner..
#Learn how to properly use backref??

####