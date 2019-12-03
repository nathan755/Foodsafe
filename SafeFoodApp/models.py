from SafeFoodApp import db
from SafeFoodApp import login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    """
    Manage Sessions for us
    """
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    company_name = db.Column(db.String(120), unique=False, nullable=False)
    password = db.Column(db.String(60), unique=False, nullable=False)

    def __repr__(self):
        return f"ID: {self.id}, User:{self.username} , email:{self.email}, company_name:{self.company_name}"

    
    