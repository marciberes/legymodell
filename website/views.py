from flask import Blueprint, render_template
from flask_login import login_required

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("home.html")

@views.route('/ads')
@login_required
def ads():
    return "<h1>ADS TESTING</h1>"

@views.route('/create-ad')
@login_required
def create_ad():
    return render_template("create_ad.html")
