from flask import Blueprint,Flask, render_template, flash, request, redirect, url_for
from flask_login import login_required, current_user
from .models import User, Ad
from werkzeug.utils import secure_filename
import os
from . import db

views = Blueprint('views', __name__)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@views.route('/')
def home():
    return render_template("home.html", user=current_user)

@views.route('/ads',methods=['GET', 'POST'])
#@login_required
def ads():
    adid = []
    category = []
    address = []
    contact = []
    adtype = []
    row=0
    if request.method == 'POST':
        category_filter = request.form.get('category')
        contact_filter = request.form.get('contact')
        adtype_filter = request.form.get('adtype')
        reference_filter = request.form.get('reference')
        row=0
        if adtype_filter == "" and category_filter == "":
            ads=Ad.query.all()
        elif adtype_filter != "" and category_filter !="":
            ads=Ad.query.filter_by(adtype=adtype_filter,category=category_filter).all()
        elif adtype_filter == "" and category_filter!="":
            ads=Ad.query.filter_by(category=category_filter).all()
        else:
            ads=Ad.query.filter_by(adtype=adtype_filter).all()
        for ad in ads:
            if ad.category == 'hairdresser':
                category.append('Fodrász')
            elif ad.category == 'cosmetician':
                category.append('Kozmetikus')
            else:
                category.append('Körmös')
            adid.append(ad.id)
            address.append(ad.address)
            contact.append(ad.contact.replace('fb','Facebook:').replace('insta','Instagram:').replace('snap','Snapchat:').replace('_',' '))
            if ad.adtype == 'exam':
                adtype.append('Vizsga')
            else:
                adtype.append('Gyakorlás')
            row+=1
        return render_template("ads.html",row=row, user=current_user, adtype=adtype,contact=contact, address=address, category=category, adid = adid)
    else:
        ads=Ad.query.all()
        for ad in ads:
            if ad.category == 'hairdresser':
                category.append('Fodrász')
            elif ad.category == 'cosmetician':
                category.append('Kozmetikus')
            else:
                category.append('Körmös')
            adid.append(ad.id)
            address.append(ad.address)
            contact.append(ad.contact.replace('fb','Facebook:').replace('insta','Instagram:').replace('snap','Snapchat:').replace('_',' '))
            if ad.adtype == 'exam':
                adtype.append('Vizsga')
            else:
                adtype.append('Gyakorlás')
            row+=1
        return render_template("ads.html",user=current_user,contact = contact, adtype = adtype, address=address, category=category, row=row, adid = adid)

@views.route('/ad', methods = ['GET', 'POST'])
def ad():
    if request.method == 'POST':
        button_id = request.form["ad_button"]
    ads = Ad.query.all()
    for ad in ads:
        if ad.id == int(button_id):
            current_ad = ad
    if os.path.exists('website/static/uploads/userid_'+str(current_ad.user_id)):
        hists = os.listdir('website/static/uploads/userid_'+str(current_ad.user_id))
        hists = [file for file in hists]
    else:
        hists = []
    adcategory_dict = {"hairdresser" : "Fodrász", "cosmetician" : "Kozmetikus", "manicure" : "Körmös"}
    adtype_dict = {"practice" : "Gyakorlás", "exam" : "Vizsga"}
    contact_dict = {"fb" : "", "insta" : "", "snap" : ""}
    contactlist = current_ad.contact.split(":::")
    return render_template("ad.html", ad = current_ad, user=current_user,  hists = hists, adcategory_dict = adcategory_dict , adtype_dict = adtype_dict, contactlist = contactlist, contact_dict = contact_dict)

@views.route('/create-ad',methods=['GET', 'POST'])
@login_required
def create_ad():
    if request.method == 'POST':
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
            contacttext ="..." + contactvalues[i]
            contact_to_append = ico + contacttext
            contactlist.append(contact_to_append)
        
        valami = ":::".join(contactlist)
        contact = request.form.get('contact_ico') + '...' + request.form.get('contact') + ':::' + valami

        new_ad = Ad(user_id=current_user.id,category=category,address=address, contact=contact, adtype = adtype)
        db.session.add(new_ad)
        db.session.commit()
        if request.method == 'POST':
            if 'file[]' not in request.files:
                flash('No file part')
                return redirect(request.url)
            files = request.files.getlist("file[]")
            if len(files) == 0:
                flash('No selected file')
                return redirect(request.url)
            if files:
                for file in files:
                    filename = secure_filename(file.filename)
                    if not os.path.exists('website/static/uploads/userid_'+str(current_user.id)):
                        os.mkdir('website/static/uploads/userid_'+str(current_user.id))
                    file.save(os.path.join('website/static/uploads/userid_'+str(current_user.id),filename))
        flash('Ad created!', category='success')
        return redirect(url_for('views.home'))
    return render_template("create_ad.html", user=current_user)
