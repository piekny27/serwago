from importlib.resources import path
from unicodedata import name
from flask import redirect, render_template, url_for, flash, request 
from serwago.models import DBConnection, User, UserProfile
from flask_login import login_user, logout_user, login_required, current_user
from serwago import app
from serwago.forms import LoginForm, RegisterForm, ProfileForm, CartForm, ProductForm
db = DBConnection()


@app.route("/")
@app.route("/welcome")
def welcome_page():
    return render_template("welcome.html")

@app.route("/login", methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            user = User.query.filter_by(email=form.username.data).first()
        if user and user.check_password_correction(attempted_password = form.password.data):
            login_user(user)
            return redirect(url_for('welcome_page'))
    return render_template("login.html", form=form)
    
    
@app.route("/register", methods=['GET', 'POST'])
def register_page():
    if(current_user.is_authenticated):
        return redirect(url_for('welcome_page'))
    form = RegisterForm()
    if form.validate_on_submit():
        new_profile = UserProfile()
        db.session.add(new_profile)
        db.session.commit()
        new_user = User(username=form.username.data,
                        email=form.email_address.data,
                        password=form.password1.data,
                        role_id = 1, profile_id = new_profile.id)
        db.session.add(new_user)
        db.session.commit()     

        login_user(new_user)                            
        return redirect(url_for('welcome_page'))

    return render_template("register.html", form=form)    

@app.route("/logout")
def logout_page():
    logout_user()
    return render_template("welcome.html")    

@app.route("/account", methods=['GET', 'POST'])
def account_page():
    if current_user.is_authenticated:
        form = ProfileForm()
        if form.validate_on_submit():

            if request.form.get('next') == 'check_dk':
                current_user_ID = current_user.id
                logout_user()
                db.session.delete(User.query.filter_by(id=current_user_ID).first())
                db.session.commit()
                return redirect(url_for('welcome_page'))

            newProfile = UserProfile(first_name = form.first_name.data,
                            last_name = form.last_name.data,
                            gender = form.gender.data,
                            nationality = form.nationality.data,
                            avatarName = "avatar12",
                            phone_number = form.phone_number.data,
                            street_number = form.street_number.data,
                            street_name = form.street_name.data,
                            zip_code = form.zip_code.data)
            current_profile_ID = current_user.profile_id
            db.session.add(newProfile)
            db.session.commit()
            current_user.profile_id = newProfile.id
            db.session.delete(UserProfile.query.filter_by(id=current_profile_ID).first())
            db.session.commit()
            return redirect(url_for('account_page'))
        currentProfile = UserProfile.query.filter_by(id=current_user.profile_id).first()
        form.first_name.data = currentProfile.first_name
        form.last_name.data = currentProfile.last_name
        form.gender.data = currentProfile.gender
        form.nationality.data = currentProfile.nationality
        form.phone_number.data = currentProfile.phone_number
        form.street_number.data = currentProfile.street_number
        form.street_name.data = currentProfile.street_name
        form.zip_code.data = currentProfile.zip_code

        


        return render_template("account.html", form=form)
    else: 
        return redirect(url_for('welcome_page'))


@app.route("/aboutus")
def aboutus_page():
    return render_template("aboutus.html")    

@app.route("/products")
def products_page():
    return render_template("products.html")    

@app.route("/cart")
def cart_page():
    if current_user.is_authenticated:
        cart_form = CartForm()
        product_form = ProductForm(name="Olek",qty=10,total=3,price=2.50)
        cart_form.products.append_entry(CartForm())
    return render_template("cart.html") 


@app.route("/reset_pwd")
def resetpwd_page():
    return render_template("reset_pwd.html")
