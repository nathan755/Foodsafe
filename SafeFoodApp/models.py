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
    user_temp_records = db.relationship('FridgeFreezerTempTable', backref=db.backref('company', lazy=True))

    def __repr__(self):
        return f"ID: {self.id}, User:{self.username} , email:{self.email}, company_name:{self.company_name}"


class FridgeFreezerTempTable(db.Model):
    """
    Fridge and Freezer Temperature table.
    company_id will return the user id. If we want to get the whole user object instead use 
    FridgeFreezerTempTable.backref
    """
    id = db.Column(db.Integer, primary_key=True)
    unit_name = db.Column(db.String(50), nullable=False)
    unit_type = db.Column(db.String(50), nullable=False)
    temperature = db.Column(db.String(10), nullable=False)
    employee_name =  db.Column(db.String(50), nullable=False)
    comment =  db.Column(db.String(100), nullable=True)
    company_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
