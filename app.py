from flask import Flask, Response, request, session, render_template, g, redirect, url_for, flash
from flask.ext.login import LoginManager, login_required, logout_user, login_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash


import requests
import json
import jinja2
import model
import os
import datetime

import api_helpers 
import passwords
import users

import pdb
# import forms

SECRET_KEY = 'FISH'
UPLOAD_FOLDER = 'static/images/uploads'

app = Flask(__name__)
app.config.from_object(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER #from flask fileuploads tutorial

# Flask login package turtorial 
login_manager = LoginManager() #from flask-login tutorial
login_manager.init_app(app)
login_manager.login_view = '/login'


@login_manager.user_loader
def load_user(user_id):

	role = session.get('role', None)
	if role == 'doula':
		return model.session.query(model.Doula).get(user_id)
	elif role == 'parent':
		return model.session.query(model.Parent).get(user_id)

	return None

@app.route('/')
def home_page():
	return render_template('index.html')

@app.route('/base_template')
def index():
	return render_template('base.html')

@app.route('/login', methods = ['GET'])
def show_login():
	print "LOGIN ARGS:", request.args
	next = request.args.get('next')
	return render_template('login.html', next = next)

@app.route('/login', methods = ['POST'])
def process_login():
	f = request.form

	email = f.get('email')
	password = f.get('password')
	role = f.get('role')

	user = model.session.query(users.which_database(role)).filter_by(email = email).first()

	if not user:
		flash("Invalid login")
		return redirect('/login')

	if not passwords.check_password_hash(user.password, password):
		flash("Invalid login")
		return redirect('/login')
	else:
		session['role'] = role
		login_user(user) # this saves the user info in the session
		flash("You successfully logged in!")
		id = user.id

		return redirect(request.args.get('next')  or ('/%s/%s') %(role, id))

@app.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect('/')


@app.route('/signup_doula', methods = ['GET'])
def signup_doula():
	return render_template('sign-up-doula.html')


@app.route('/signup_doula', methods = ['POST'])
def process_signup_doula():
	f = request.form
	password = f.get('password')
	password_again = f.get('password_again')
	email = f.get('email')
	zipcode = f.get('zipcode')
	image = f.get('image')

	if users.validate_doula_signup(f):
		lat, lng = api_helpers.geocode_zipcode(zipcode)
		hashed_password = passwords.set_password(password)

		doula = model.Doula()
		doula.parse_form_data(request.form)
		doula.store_coordinates(lat, lng)
		model.session.add(doula)

		model.session.commit()
		
		users.save_user_image(doula, request.files['image'], 'doula')		

		return redirect('/')

	else:
		return redirect('/signup_doula')


@app.route('/signup_parent', methods = ['GET'])
def signup_parent():
	return render_template('sign-up-parent.html')


@app.route('/signup_parent', methods = ['POST'])
def process_signup_parent():
	# form is coming from sign-up-parent.html
	f = request.form
	password = f.get('password')
	password_again = f.get('password_again')
	email = f.get('email')
	zipcode = f.get('zipcode')
	image = f.get('image')

	if not passwords.password_check(password, password_again):
		flash("Passwords do not match. Please enter your password again.")
		return redirect('/signup_parent')

	existing_parent_list = model.session.query(model.Parent).filter_by(email='email').all()
	if len(existing_parent_list) > 0:
		flash("Email already exists. Login with that email, or sign up with a different email.")
		return redirect('/signup_parent')

	else:
		hashed_password = passwords.set_password(password)
		lat, lng = api_helpers.geocode_zipcode(zipcode)
		
		parent = model.Parent()
		parent.parse_parent_form_data(request.form)
		parent.store_coordinates(lat, lng)		

		model.session.add(parent)
		model.session.commit()

		users.save_user_image(parent, request.files['image'], 'parent')

		return redirect('/login')

@app.route('/doula/<int:id>') #change this route to include the doula's <int:id> in the url
def display_doula_profile(id):
	doula = model.session.query(model.Doula).get(id)
	suggested_doula_list = users.suggest_doulas()

	return render_template('doula-profile.html', doula = doula,
												suggested_doula_list = suggested_doula_list)


@app.route('/parent/<int:id>') #change this route to include the parents's <int:id> in the url
@login_required
def display_user_profile(id):

	parent = model.session.query(model.Parent).get(id)

	if parent.visibility == "doulas" and not current_user.is_doula() and current_user.id != parent.id:
		flash('This user has chosen to be visible to doulas only')
		return render_template('blank.html')

	elif parent.visibility == 'none' and current_user.id != parent.id:
		flash('This user has chosen to be invisible')
		return render_template('blank.html')
		

	due_date = parent.due_date.strftime("%m/%d/%y")

	suggested_parent_list = users.suggest_parents()

	return render_template('user-profile.html', parent = parent,
												due_date = due_date,
												suggested_parent_list = suggested_parent_list)


@app.route('/search', methods = ['GET'])
def search():
	return render_template('search.html')

@app.route('/search', methods = ['POST'])
def display_search_results():
	f = request.form

	search_zip = f.get('doula_zip_search')
	search_radius = int(f.get('zip_radius'))
	
	min_lat, max_lat, min_lng, max_lng = api_helpers.create_bounding_box(search_zip, search_radius)

 	doula_list = api_helpers.zip_radius_search(min_lat, max_lat, min_lng, max_lng)
		
	return render_template('search-results.html', doula_list = doula_list)

@app.route('/list_all', methods = ['POST'])
def list_all_doulas():
	all_doula_list = model.session.query(model.Doula).all()

	return render_template('search-results.html', doula_list = all_doula_list)

@app.route('/doula_edit', methods = ['POST'])
def apply_doula_edits():
	f = request.form

	id = f.get('pk')
	field = f.get('name')
	new_value = f.get('value')

	doula = model.session.query(model.Doula).get(id)
	if field == 'firstname':
		doula.firstname = new_value

	if field == 'lastname':
		doula.lastname = new_value

	if field == 'website':
		doula.website = new_value

	if field == 'phone':
		doula.phone = new_value

	if field == 'price_min':
		doula.price_min = new_value
	
	if field == 'price_max':
		doula.price_max = new_value

	if field == 'background':
		doula.background = new_value

	if field == 'services':
		doula.services = new_value

	if field == 'zipcode':
		doula.zipcode = new_value

	model.session.commit()

	return( 'success!')

@app.route('/parent_edit', methods = ['POST'])
def apply_parent_edits():
	f = request.form

	id = f.get('pk')
	field = f.get('name')
	new_value = f.get('value')

	parent = model.session.query(model.Parent).get(id)
	if field == 'firstname':
		parent.firstname = new_value

	if field == 'lastname':
		parent.lastname = new_value

	if field == 'zipcode':
		parent.zipcode = new_value

	if field == 'price_min':
		parent.price_min = new_value
	
	if field == 'price_max':
		parent.price_max = new_value

	if field == 'background':
		parent.background = new_value

	if field == 'ideal_nar':
		parent.ideal_doula_nar = new_value

	model.session.commit()

	return( 'success!')

if __name__ == '__main__':
	app.debug = True
	app.run()