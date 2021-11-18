from flask import Blueprint, render_template, flash, request, redirect, url_for
from flask_login import login_required, current_user
from .models import User, Ad
from . import db

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("home.html")

@views.route('/ads')
@login_required
def ads():
    return "<h1>ADS TESTING</h1>"

@views.route('/create-ad',methods=['GET', 'POST'])
@login_required
def create_ad():
    if request.method == 'POST':
        #user_id TODO
        category = request.form.get('category')
        address = request.form.get('address')
        adtype = request.form.get('adtype')
        contactvalues = []
        contacticovalues = []
        for key in request.form:
            if key.startswith('contacts.'):
                id_ = key.partition('.')[-1]
                value = request.form[key]
                contactvalues.append(value)
        for key in request.form:
            if key.startswith('contacts_ico.'):
                id_ = key.partition('.')[-1]
                value = request.form[key]
                contacticovalues.append(value)
        contactlist = []
        for i in range(0, len(contacticovalues)):
            ico = contacticovalues[i]
            contacttext = contactvalues[i]
            contactlist.append(ico)
            contactlist.append(contacttext)
        
        valami = "_".join(contactlist)
        contact = request.form.get('contact_ico') + '_' + request.form.get('contact') + '_' + valami

        new_ad = Ad(user_id=current_user.id,category=category,address=address, contact=contact, adtype = adtype)
        db.session.add(new_ad)
        db.session.commit()
        flash('Ad created!', category='success')
        return redirect(url_for('views.home'))
    return render_template("create_ad.html", user=current_user)
