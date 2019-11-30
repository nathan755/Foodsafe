from SafeFoodApp import app
from flask import render_template, url_for, flash, redirect
from SafeFoodApp.forms import RegistrationForm



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
        flash("Account Created")
        return redirect(url_for("app_home"))

    return render_template("register.html", form=form)