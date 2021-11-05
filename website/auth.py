from flask import Blueprint, render_template

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return "<h1>LOGIN TESTING</h1>"

@auth.route('/logout')
def logout():
    return "<h1>LOGOUT TESTING</h1>"

@auth.route('/sign-up')
def sign_up():
    return "<h1>SIGN-UP TESTING</h1>"