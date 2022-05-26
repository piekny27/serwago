from flask import redirect, render_template, url_for, flash, request
from serwago.models import DBConnection
from flask_login import login_user, logout_user, login_required, current_user
from serwago import app
from serwago.forms import LoginForm 

db = DBConnection()


@app.route("/")
@app.route("/base")
def base_page():
    return render_template("base.html")

@app.route("/login", methods=['GET', 'POST'])
def login_page():
    form = LoginForm
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            user = User.query.filter_by(email=form.username.data).first()
        if user and user.check_password_correction(attemted_password = form.password.data):
            login_user(user)
            return redirect(url_for('welcome.html'))
    return render_template("login.html", form=form)
    
    
@app.route("/register")
def register_page():
    return render_template("register.html")    

@app.route("/logout")
def logout_page():
    logout_user()
    return render_template("home.html")    

@app.route("/account")
def account_page():
    return render_template("account.html")


@app.route("/aboutus")
def aboutus_page():
    return render_template("aboutus.html")    

@app.route("/products")
def products_page():
    return render_template("products.html")    
    
    
@app.route("/welcome")
def welcome_page():
    return render_template("welcome.html")

@app.route("/reset_pwd")
def resetpwd_page():
    return render_template("reset_pwd.html")
