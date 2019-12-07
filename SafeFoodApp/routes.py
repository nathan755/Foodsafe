from SafeFoodApp import app, db, bcrypt
from flask import render_template, url_for, flash, redirect
from SafeFoodApp.forms import RegistrationForm, LoginForm, FridgeFreezerTempForm
from SafeFoodApp.models import User, FridgeFreezerTempTable
from flask_login import login_user, current_user, logout_user


@app.route('/home')
def landing_page():
    return render_template("home.html")


@app.route('/apphome')
def app_home():
    return render_template("app_home.html", title="foobar")

@app.route('/register', methods= ["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(username=form.username.data, email=form.email.data, company_name=form.company_name.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash("Account Created")
        return redirect(url_for("login"))

    return render_template("register.html", form=form)


@app.route('/login', methods= ["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash("Login Succsessful")
            return redirect(url_for("app_home"))


        flash("Login Unsuccsessful")
    return render_template("login.html", form=form)

@app.route("/logout")
def logout():
    logout_user()
    flash("Logged Out Successfully")
    return redirect(url_for('landing_page'))


@app.route("/unit_temperatures", methods=["GET", "POST"])
def fridge_freezer_temps():
    form = FridgeFreezerTempForm()
    if form.validate_on_submit():
        record = FridgeFreezerTempTable(unit_name=form.unit_name.data, unit_type=form.unit_type.data,
        temperature=form.temperature.data, employee_name=form.employee_name.data, comment=form.comment.data, company=current_user)
        db.session.add(record)
        db.session.commit()
        flash("Record Submitted")
        
        
        return redirect(url_for("fridge_freezer_temps"))   
    return render_template("unit_temperatures.html", form=form)

@app.route("/test")
def test():
    record = FridgeFreezerTempTable.query.filter_by(company_id=current_user.id).first()
    if record == None:
        return render_template("app_home.html")

    return render_template("test.html",record=record)





    