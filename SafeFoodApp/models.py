from SafeFoodApp import db
from SafeFoodApp import login_manager
from flask_login import UserMixin
from datetime import datetime
#find out what to do if you query and the record doesnt exist.. errorpages..
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
    user_temp_records = db.relationship('FridgeFreezerTempTable', backref=db.backref('user', lazy=True))
    user_cooking_temp_records = db.relationship("CookingTemperatureTable", backref=db.backref('user', lazy=True))
    user_delivery_temp_records = db.relationship("DeliveryTemperatureTable", backref=db.backref('user', lazy=True))
    hot_hold_records = db.relationship("HotHoldTable", backref=db.backref('user', lazy=True))
    menu_spec = db.relationship("MenuTable", backref=db.backref('user', lazy=True))
    wastage = db.relationship("WastageTable", backref=db.backref('user', lazy=True))
    cooling_records = db.relationship("FoodCoolingTable", backref=db.backref('user', lazy=True))
    
    def __repr__(self):
        return f"ID: {self.id}, User:{self.username} , email:{self.email}, company_name:{self.company_name}"

class Base(db.Model):
    __abstract__ = True
    employee_name =  db.Column(db.String(50), nullable=False)
    date_submitted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    comment =  db.Column(db.String(100), nullable=True)


class FridgeFreezerTempTable(Base):
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
    company_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)


class CookingTemperatureTable(Base):
    id = db.Column(db.Integer, primary_key=True)
    food_item = db.Column(db.String(20), nullable=False)
    temperature = db.Column(db.String(10), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)


class DeliveryTemperatureTable(Base):
    id = db.Column(db.Integer, primary_key=True)
    food_item = db.Column(db.String(20), nullable=False)
    temperature = db.Column(db.String(10), nullable=False)
    high_risk_food_item = db.Column(db.String(20), nullable=False)
    high_risk_temperature = db.Column(db.String(10), nullable=False)
    supplier_name =  db.Column(db.String(20), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class HotHoldTable(Base):
    id = db.Column(db.Integer, primary_key=True)
    food_item = db.Column(db.String(20), nullable=False)
    temperature = db.Column(db.String(10), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class MenuTable(Base):
    id = db.Column(db.Integer, primary_key=True)
    menu_item = db.Column(db.String(20), nullable=False)
    ingredients = db.Column(db.String(100), nullable=False)
    method = db.Column(db.String(100), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class WastageTable(Base):
    id = db.Column(db.Integer, primary_key=True)
    food_item = db.Column(db.String(20), nullable=False)
    quanitiy = db.Column(db.String(20), nullable=False)
    unit = db.Column(db.String(20), nullable=False)
    reason = db.Column(db.String(20), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class FoodCoolingTable(Base):
    id = db.Column(db.Integer, primary_key=True)
    food_item = db.Column(db.String(20), nullable=False)
    cooling_method = db.Column(db.String(20), nullable=False)
    time_started = db.Column(db.DateTime, nullable=False)
    temperature = db.Column(db.String(10), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)



def query_records():
    pass
