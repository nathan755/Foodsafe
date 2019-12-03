from SafeFoodApp import app, db, bcrypt
from flask import render_template, url_for, flash, redirect
from SafeFoodApp.forms import RegistrationForm, LoginForm
from SafeFoodApp.models import User
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