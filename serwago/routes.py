from flask import redirect, render_template, url_for, flash, request
from serwago.models import DBConnection
from flask_login import login_user, logout_user, login_required, current_user
from serwago import app

db = DBConnection()


@app.route("/")
@app.route("/home")
def home_page():
    return render_template("home.html")

