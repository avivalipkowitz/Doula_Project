from flask import Flask, Response, request, session, render_template, g, redirect, url_for, flash
from flask.ext.login import LoginManager, login_required, logout_user, login_user, current_user
from flask.ext.principal import Principal, Permission, RoleNeed
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

SECRET_KEY = "fish"
UPLOAD_FOLDER = 'static/images/uploads'

app = Flask(__name__)
app.config.from_object(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER #from flask fileuploads tutorial

# Flask login package turtorial (aka Rob) (so far just doing one user type "Doula")
login_manager = LoginManager() #from flask-login tutorial
login_manager.init_app(app)
login_manager.login_view = '/login'

# From Flask Principal tutorial
# load the extension
principals = Principal(app)
#create a permission with a single Need, in this case a RoleNeed.
doula_permission = Permission(RoleNeed('doula'))
admin_permission = Permission(RoleNeed('admin'))

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

	# TODO: json, son
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
	# TODO: parse form response in separate method
	# TODO: maybe fix with method that takes unspecified # of args
	# TODO, stretch: return form data in a json
	f = request.form

	password = f.get('password')
	password_again = f.get('password_again')
	email = f.get('email')
	zipcode = f.get('zip')

	if not passwords.password_check(password, password_again):
		flash("Passwords do not match. Please enter your password again.")
		return redirect('/signup_doula')


	# TODO: verify how to query database to see if an email is already registered
	if model.session.query(model.Doula).get(email) != None:
		print model.session.query(model.Doula).get(email)
		flash("Email already exists. Login with that email, or sign up with a different email.")
		return redirect('/signup_doula')

	else:
		lat, lng = api_helpers.geocode_zipcode(zipcode)
		hashed_password = passwords.set_password(password)

		doula = model.Doula()
		doula.parse_form_data(request.form)
		doula.store_coordinates(lat, lng)
		model.session.add(doula)
		model.session.commit()
		
		users.save_user_image(doula, request.files['image'], 'doula')		

		return redirect('/')

@app.route('/signup_parent', methods = ['GET'])
def signup_parent():
	return render_template('sign-up-parent.html')


@app.route('/signup_parent', methods = ['POST'])
def process_signup_parent():
	# code loosely taken from judgement.py on github
	# form is coming from sign-up-doula.html
	f = request.form

	# TODO: parse form response in a separate method
	email = f.get('email')
	password = f.get('password')
	password_again = f.get('password_again')
	first_name = f.get('firstname')
	last_name = f.get('lastname')
	display_name = f.get('display_name')
	zipcode = f.get('zip')
	price_min = f.get('price_min')
	price_max = f.get('price_max')
	background_nar = f.get('background')
	ideal_doula_nar = f.get('ideal_nar')
	visibility = f.get('visibility')

	unicode_due_date = f.get('due_date')
	due_date = datetime.datetime.strptime(unicode_due_date, "%Y-%m-%d")

	if not passwords.password_check(password, password_again):
		flash("Passwords do not match. Please enter your password again.")
		return redirect('/signup_parent')
	
	# TODO: implement check to see if an account w/ this email already exists
	# TODO: make this a separate function with arg "model.<User>" and store in module users
	elif model.session.query(model.Parent).get('email') != None:
		flash("Email already exists. Login with that email, or sign up with a different email.")
		return redirect('/signup_parent')


	else:
		hashed_password = passwords.set_password(password)
		lat, lng = api_helpers.geocode_zipcode(zipcode)
		parent = model.Parent(email = email, 
							password = hashed_password, 
							firstname = first_name,
							lastname = last_name,
							zipcode = zipcode,
							zipcode_lat = lat,
							zipcode_lng = lng,
							price_min = price_min,
							price_max = price_max,
							background = background_nar,
							display_name = display_name,
							due_date = due_date,
							ideal_doula_nar = ideal_doula_nar,
							visibility = visibility
							)

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

	# set permissions
	# TODO: for testing purposes, put this in a users module method
	if parent.visibility == "doulas" and not current_user.is_doula() and current_user.id != parent.id:
		flash('This user has chosen to be visible to doulas only')
		return render_template('blank.html')

	elif parent.visibility == 'none' and current_user.id != parent.id:
		flash('This user has chosen to be invisible')
		return render_template('blank.html')
		

	due_date = parent.due_date.strftime("%m/%d/%y")

	

	return render_template('user-profile.html', parent = parent,
												due_date = due_date)


@app.route('/search', methods = ['GET'])
def search():
	return render_template('search.html')

@app.route('/search', methods = ['POST'])
def display_search_results():
	f = request.form

	# TODO LOCATOR: api_helpers method 
	doula_zip = f.get('doula_zip_search')
	search_radius = int(f.get('zip_radius'))
	
	# put next three lines in function in helper
	lat, lng = api_helpers.geocode_zipcode(doula_zip)

	min_lat, max_lat = api_helpers.min_max_lat_search(lat, search_radius)
	min_lng, max_lng = api_helpers.min_max_lng_search(lng, search_radius)

 	doula_list = api_helpers.zip_radius_search(min_lat, max_lat, min_lng, max_lng)
		
	return render_template('search-results.html', doula_list = doula_list)

# TODO: def list_all_users(role)
@app.route('/list_all', methods = ['POST'])
def list_all_doulas():
	all_doula_list = model.session.query(model.Doula).all()

	return render_template('search-results.html', doula_list = all_doula_list)


# TODO: create def apply_user_edits(*args)
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