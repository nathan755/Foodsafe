from SafeFoodApp import app, db, bcrypt
from flask import render_template, url_for, flash, redirect
from SafeFoodApp.forms import RegistrationForm, LoginForm, FridgeFreezerTempForm, TemperatureCheckForm, DeliveryTemperatureForm, WastageForm, MenuForm, CoolingForm
from SafeFoodApp.models import User, FridgeFreezerTempTable, CookingTemperatureTable, DeliveryTemperatureTable, HotHoldTable, MenuTable, WastageTable,FoodCoolingTable
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
        temperature=form.temperature.data, employee_name=form.employee_name.data, comment=form.comment.data, user=current_user)
        db.session.add(record)
        db.session.commit()
        flash("Record Submitted")
        return redirect(url_for("fridge_freezer_temps"))   
    return render_template("unit_temperatures.html", form=form)

@app.route("/cooking_temp", methods=["GET", "POST"])
def cooking_temps():
    form = TemperatureCheckForm()
    if form.validate_on_submit():
        record = CookingTemperatureTable(food_item=form.food_item.data, temperature=form.temperature.data, employee_name=form.employee_name.data,
        comment=form.comment.data, user=current_user)
        db.session.add(record)
        db.session.commit()
        flash("record submitted")
        return redirect(url_for("cooking_temps"))         
    return render_template("cooking_temp.html", form=form)

@app.route("/delivery_temp", methods=["GET", "POST"])
def delivery():
    form =  DeliveryTemperatureForm()
    if form.validate_on_submit():
        record = DeliveryTemperatureTable(food_item=form.food_item.data, temperature=form.food_item_temperature.data,
        high_risk_food_item=form.high_risk_food_item.data, high_risk_temperature=form.high_risk_food_item_temperature.data,
        employee_name=form.employee_name.data, comment=form.comment.data, user=current_user)
        db.session.add(record)
        db.session.commit()
        flash("record submitted")
        return redirect(url_for("delivery"))
    return render_template("delivery_temp.html", form=form)

@app.route("/hot_hold", methods=["GET", "POST"])
def hot_hold():
    form = TemperatureCheckForm()
    if form.validate_on_submit():
        record = HotHoldTable(food_item=form.food_item.data, temperature=form.temperature.data, employee_name=form.employee_name.data,
        comment=form.comment.data, user=current_user)
        db.session.add(record)
        db.session.commit()
        flash("Record Submitted")
        return redirect(url_for("hot_hold"))
    return render_template("hot_hold.html", form=form)

@app.route("/menu", methods=["GET", "POST"])
def menu():
    form = MenuForm()
    if form.validate_on_submit():
        record = MenuTable(menu_item=form.menu_item.data, ingredients=form.ingredients.data, method=form.method.data, menu_spec=current_user)
        db.session.add(record)
        db.session.commit()
        flash("Record Submitted")
        return redirect(url_for("menu"))
    return render_template("menu.html", form = form)

@app.route("/wastage", methods=["GET", "POST"])
def wastage():
    form = WastageForm()
    if form.validate_on_submit():
        record = WastageTable(food_item=form.food_item.data, quanitiy=form.quanity.data, unit=form.unit.data, reason=form.reason.data,
        employee_name=form.name.data, user=current_user)
        db.session.add(record)
        db.session.commit()
        flash("Record Submitted")
        return redirect(url_for("wastage"))
    return render_template("wastage.html", form=form)

@app.route("/cooling", methods=["GET", "POST"])
def food_cooling():
    form = CoolingForm()
    if form.validate_on_submit():
        record = FoodCoolingTable(food_item=form.food_item.data, cooling_method=form.cooling_method.data, time_started=form.time_started.data,
        temperature=form.temperature.data, user=current_user)
        db.session.add(record)
        db.session.commit()
        flash("Record Submmited")
        return redirect(url_for("food_cooling"))
    return render_template("cooling.html", form=form)

@app.route("/unit_temp_records/<int:page_number>")
def unit_records(page_number):
    """
    records = pagiantion object
    page number = the current page
    page is sent to the html file this allows the user ..
    """
    table = FridgeFreezerTempTable.query.filter_by(user=current_user)
    
    records = FridgeFreezerTempTable.query.filter_by(user=current_user).paginate(per_page=5, page=page_number, error_out=True)
    
    
    return render_template("unit_temp_records.html", user_records=records, table=table)


@app.route("/cooking_temp_records/<int:page_number>")
def cooking_records(page_number):
    
    records = CookingTemperatureTable.query.filter_by(user=current_user).paginate(per_page=5, page=page_number, error_out=True)
    return render_template("cooking_temp_records.html", user_records=records)

@app.route("/cooling_temp_records/<int:page_number>")
def cooling_records(page_number):
    
    records = FoodCoolingTable.query.filter_by(user=current_user).paginate(per_page=5, page=page_number, error_out=True)
    return render_template("cooling_temp_records.html", user_records=records)

@app.route("/delivery_temp_records/<int:page_number>")
def delivery_records(page_number):
    
    records = DeliveryTemperatureTable.query.filter_by(user=current_user).paginate(per_page=5, page=page_number, error_out=True)
    return render_template("delivery_temp_records.html", user_records=records)

@app.route("/hot_hold_temp_records/<int:page_number>")
def hothold_records(page_number):
    
    records = HotHoldTable.query.filter_by(user=current_user).paginate(per_page=5, page=page_number, error_out=True)
    return render_template("hot_hold_temp_records.html", user_records=records)

@app.route("/menu_records/<int:page_number>")
def menu_records(page_number):
    
    records = MenuTable.query.filter_by(user=current_user).paginate(per_page=5, page=page_number, error_out=True)
    return render_template("menu_records.html", user_records=records)

@app.route("/wastage_records/<int:page_number>")
def wastage_records(page_number):
    
    records = WastageTable.query.filter_by(user=current_user).paginate(per_page=5, page=page_number, error_out=True)
    return render_template("wastage_records.html", user_records=records)








#################################################################################
@app.route("/audits", methods=["GET", "POST"])
def audits():
    return render_template("audits.html")

@app.route("/cleaning", methods=["GET", "POST"])
def cleaning():
    return render_template("cleaning.html")

@app.route("/closing_checks", methods=["GET", "POST"])
def closing():
    return render_template("closing_checks.html")

@app.route("/opening_checks", methods=["GET", "POST"])
def opening_checks():
    return render_template("opening_checks.html")

@app.route("/end_day", methods=["GET", "POST"])
def end_of_day():
    return render_template("end_day.html")







@app.route("/test")
def test():
    """Test route for testing and displaying database data
    """
    record = FridgeFreezerTempTable.query.filter_by(company_id=current_user.id).first()
   
    if record == None:
        return render_template("app_home.html")

    return render_template("test.html",record=record)





    