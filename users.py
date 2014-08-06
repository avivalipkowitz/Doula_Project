from flask import Flask, Response, request, session, render_template, g, redirect, url_for, flash
from flask.ext.login import LoginManager, login_required, logout_user, login_user, current_user
import model
import api_helpers
import os
from random import randint
import passwords
import pdb

# Following code is from flask.pocoo.org/docs/patterns/fileuploads
UPLOAD_FOLDER = 'static/images/uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
	return '.' in filename and \
		filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


# TODO: make sure that this won't accept filenames without extensions
def file_extension(filename):
	return filename.split('.')[-1]

def which_database(role):
	# Because of the database structure (two user classes) there are no unique identifiers without also including the user type. This step is necessary in order to determine whice database to query.
	if role == "doula":
		return model.Doula
	elif role == "parent":
		return model.Parent

	return None		


def db_add_doula(doula_dict):
	d = model.Doula()
	
	d.parse_form_data(doula_dict)
	lat, lng = api_helpers.geocode_zipcode(doula_dict['zipcode'])
	d.store_coordinates(lat, lng)

	model.session.add(d)
	model.session.commit()

def db_add_parent(parent_dict):
	d = model.Parent()
	
	d.parse_parent_form_data(parent_dict)
	lat, lng = api_helpers.geocode_zipcode(parent_dict['zipcode'])
	d.store_coordinates(lat, lng)

	model.session.add(d)
	model.session.commit()

def save_user_image(user, pic, role):
	if pic and allowed_file(pic.filename):
		filename = "%s_%s.%s" % (role, user.id, file_extension(pic.filename))
		pic.save(os.path.join(UPLOAD_FOLDER, filename))

		user.image = filename
		model.session.commit()	

# todo: needs a test
def suggest_doulas():
	doula_list = model.session.query(model.Doula).all()
	if len(doula_list) > 4:
		suggested_doula_list = []
		for i in range(1,4):
			doula = doula_list.pop(randint(0, len(doula_list) - 1))
			suggested_doula_list.append(doula)
		return suggested_doula_list
	return None

# todo: needs a test
def suggest_parents():
	parent_list = model.session.query(model.Parent).all()
	if len(parent_list) > 4:
		suggested_parent_list = []
		for i in range(1,4):
			parent = parent_list.pop(randint(0, len(parent_list) - 1))
			suggested_parent_list.append(parent)
		return suggested_parent_list
	return None

# todo: needs a unit test
def validate_doula_signup(data):
	password = data.get('password', "")
	password_again = data.get('password_again', "")
	email = data.get('email', "")
	zipcode = data.get('zipcode', "")
	image = data.get('image', "")

	if email == "":
		flash("Please enter an email address")
		return False

	if password == "":
		flash("Please enter your password")
		return False
	if password_again == "":
		flash("Please confirm your password")
		return False

	if not passwords.password_check(password, password_again):
		flash("Passwords do not match. Please enter your password again.")
		return False

	existing_user_list = model.session.query(model.Doula).filter_by(email = email).all()
	if len(existing_user_list) > 0:
		flash("Email already exists. Login with that email, or sign up with a different email.")
		return False

	if zipcode == "":
		flash("Please enter your zipcode below.")
		return False

	if image == "":
		flash("Please upload a profile picture")
		return False

	return True

