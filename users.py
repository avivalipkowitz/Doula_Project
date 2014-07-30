from flask import Flask, Response, request, session, render_template, g, redirect, url_for, flash
from flask.ext.login import LoginManager, login_required, logout_user, login_user, current_user
import model
import os
from random import randint

# Following code is from flask.pocoo.org/docs/patterns/fileuploads
UPLOAD_FOLDER = 'static/images/uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

# TODO: make private
def allowed_file(filename):
	return '.' in filename and \
		filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

# TODO: make private
# need to make sure that this won't accept filenames without extensions
def file_extension(filename):
	return filename.split('.')[-1]

def which_database(role):
	# TODO: explain why this is here wrt to database
	if role == "doula":
		return model.Doula
	elif role == "parent":
		return model.Parent

	return None		

def save_user_image(user, pic, role):
	if pic and allowed_file(pic.filename):
		filename = "%s_%s.%s" % (role, user.id, file_extension(pic.filename))
		# TODO: check to see if this way of pointing to the 'upload_folder' is correct
		pic.save(os.path.join(UPLOAD_FOLDER, filename))

		user.image = filename
		model.session.commit()	

# TODO: get this to work
# def current_user_check(role, email):
# 	return model.session.query(which_database(role)).get('email', None) 

# TODO: needs a test
def suggest_doulas():
	doula_list = model.session.query(model.Doula).all()
	suggested_doula_list = []
	for i in range(1,4):
		doula = doula_list.pop(randint(0, len(doula_list) - 1))
		suggested_doula_list.append(doula)
	return suggested_doula_list

# TODO: needs a test
def parse_doula_form_data(f):
	doula_data_dict = {}

	password = f.get('password')
	password_again = f.get('password_again')
	email = f.get('email')
	first_name = f.get('firstname')
	last_name = f.get('lastname')
	practice_name = f.get('practice')
	phone_number = f.get('phone')
	website = f.get('website')
	price_min = f.get('price_min')
	price_max = f.get('price_max')
	background_nar = f.get('background_nar')
	services_nar = f.get('services')
	zipcode = f.get('zip')


