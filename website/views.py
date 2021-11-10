from flask import Blueprint, render_template

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("home.html")

@views.route('/ads')
def ads():
    return "<h1>ADS TESTING</h1>"

@views.route('/create-ad')
def create_ad():
    return "<h1>CREATE-AD TESTING</h1>"
