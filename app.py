from flask import Flask, Response, request, session, render_template, g, redirect, url_for, flash
from flask.ext.login import LoginManager, login_required, logout_user, login_user, current_user
from flask.ext.principal import Principal, Permission, RoleNeed
from werkzeug.security import generate_password_hash, check_password_hash

import requests
import json
import jinja2
import model
import os
from werkzeug.utils import secure_filename
import datetime

import api_helpers 
import helpers

SECRET_KEY = "fish"

# Following code is from flask.pocoo.org/docs/patterns/fileuploads
UPLOAD_FOLDER = 'static/images/uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

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



# for file uploads (for profile picture)
# from flask tutorial on file uploads
def allowed_file(filename):
	return '.' in filename and \
		filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def file_extension(filename):
	return filename.split('.')[-1]

# from password salt tutorial
def set_password(password):
	return generate_password_hash(password)


#only setting this up for doulas at the moment
@login_manager.user_loader
def load_user(user_id):
	# query user database (user id has to be unicode)
	# except that i think i'm getting the email, so i'll probably have to add a step where 
	# I'm getting the user_id (or Doula_id, as the case may be)
	# fix to be clearer on the exceptions to raise specific errors

	# have to pass in the role here so that the function knows to return one user type or the other
	# try:
	role = session.get('role', None)
	if role == 'doula':
		return model.session.query(model.Doula).get(user_id)
	elif role == 'parent':
		return model.session.query(model.Parent).get(user_id)


	return None
	# except:
	# 	return None




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

	user_email = f.get('email')
	user_password = f.get('password')
	role = f.get('role')

	if role == 'doula':
		user = model.session.query(model.Doula).filter_by(email = user_email).filter_by(password = user_password).first()

		if not user:
			flash("invalid login")
			return redirect('/login')
		else:
			session['role'] = 'doula'
			login_user(user) # this saves the user info in the session
			flash("You succesfully logged in!")
			id = user.id

			return redirect(request.args.get('next')  or ('/'))

	elif role == 'parent':
		user = model.session.query(model.Parent).filter_by(email = user_email).filter_by(password = user_password).first()

		if not user:
			flash("invalid login")
			return redirect('/login')
		else:
			session['role'] = 'parent'
			login_user(user) # this saves the user info in the session
			flash("You succesfully logged in!")

			return redirect(request.args.get('next')  or ('/user/' + str(user.id)))

	else:
		flash("invalid role--check the user type, fool")
		return redirect('/login')


@app.route('/logout')
@login_required
# i'm adding the login_required thing so this should obviate the
# error thingy
def logout():
	## FIX THIS SO YOU CAN'T BREAK IT BY LOGGING OUT
	## WHEN YOU HAVEN'T LOGGED IN!
	### except i just adjusted this with the flask login package, so maybe problem fixed?
	### so add a button that redirects to '/logout'
	logout_user()
	return redirect('/')


@app.route('/signup_doula', methods = ['GET'])
def signup_doula():
	return render_template('sign-up-doula.html')


@app.route('/signup_doula', methods = ['POST'])
def process_signup_doula():
	# code loosely taken from judgement.py on github
	# form is coming from sign-up-doula.html
	# is this where I should be checking that the password entries match?
	# Should also check to make sure that user doesn't already exist
	f = request.form
	
	# JUST FOR PROFILE PICTURE
	# Will have to move this code to below the commit, so that i can save the 
	# user first before saving as (usertype/id#) 


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

	# check that passwords match
	if password != password_again:
		flash("Passwords do not match. Please enter your password again.")
		return redirect('/signup_doula')


	# check to see if user already exists
	if model.session.query(model.Doula).get('email') != None:
		flash("Email already exists. Login with that email, or sign up with a different email.")
		return redirect('/signup_doula')

	else:
		hashed_password = model.set_password(password)
		print "hashed pw is %r" %hashed_password 
		doula = model.Doula(email = email, 
							password = hashed_password, 
							firstname = first_name,
							lastname = last_name,
							practice = practice_name,
							phone = phone_number,
							website = website,
							price_min = price_min,
							price_max = price_max,
							background = background_nar,
							services = services_nar,
							zipcode = zipcode
							)

		


		model.session.add(doula)
		model.session.commit()
		
		# save filename as combo of usertype and id. have to save this for the end so that the id is generated
		file = request.files['image']
		
		if file and allowed_file(file.filename):
			filename = "%s_%s.%s" % ("doula", doula.id, file_extension(file.filename))
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

			doula.image = filename
			model.session.commit()	

		return redirect('/')

@app.route('/signup_parent', methods = ['GET'])
def signup_parent():
	return render_template('sign-up-parent.html')


@app.route('/signup_parent', methods = ['POST'])
def process_signup_parent():
	# code loosely taken from judgement.py on github
	# form is coming from sign-up-doula.html
	# is this where I should be checking that the password entries match?
	f = request.form
	
	# JUST FOR PROFILE PICTURE

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

	# this is coming in as unicode--change to DateTime
	unicode_due_date = f.get('due_date')
	due_date = datetime.datetime.strptime(unicode_due_date, "%Y-%m-%d")

	# geocode API
	lat, lng = api_helpers.geocode_zipcode(zipcode)
	print "lat: %r, lng: %r" %(lat, lng)



	#check that passwords match
	if not helpers.password_check(password, password_again):
		flash("Passwords do not match. Please enter your password again.")
		return redirect('/signup_doula')
			
	# if password != password_again:
	# 	flash("Passwords do not match. Please enter your password again.")
	# 	return redirect('/signup_doula')

	
	# check to see if user already exists
	elif model.session.query(model.Parent).get('email') != None:
		flash("Email already exists. Login with that email, or sign up with a different email.")
		return redirect('/signup_parent')


	else:
		parent = model.Parent(email = email, 
							password = password, 
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


		# save filename as combo of usertype and id. have to save this for the end so that the id is generated
		file = request.files['image']
		
		if file and allowed_file(file.filename):
			filename = "%s_%s.%s" % ("parent", parent.id, file_extension(file.filename))
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

			parent.image = filename
			model.session.commit()	

		return redirect('/login')

@app.route('/doula/<int:id>') #change this route to include the doula's <int:id> in the url
# @login_required
def display_doula_profile(id):
	doula = model.session.query(model.Doula).get(id)

	return render_template('doula-profile.html', doula = doula)


@app.route('/user/<int:id>') #change this route to include the parents's <int:id> in the url
@login_required
def display_user_profile(id):

	parent = model.session.query(model.Parent).get(id)

	# set permissions
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

	doula_zip = f.get('doula_zip_search')
	zip_radius = f.get('zip_radius')

	if zip_radius == "5mi":
	# 	lat_min = ??
		doula_list = model.session.query(model.Doula).filter_by(zipcode = doula_zip).all()
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