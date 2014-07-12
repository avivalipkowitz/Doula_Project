from flask import Flask, request, session, render_template, g, redirect, url_for, flash
import jinja2
import model
import os
from werkzeug.utils import secure_filename


SECRET_KEY = "fish"

# Following code is from flask.pocoo.org/docs/patterns/fileuploads
UPLOAD_FOLDER = 'static/images/uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config.from_object(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER #from flask fileuploads tutorial



# for file uploads (for profile picture)
# from flask tutorial on file uploads
def allowed_file(filename):
	return '.' in filename and \
		filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS





@app.route('/')
def home_page():
	return render_template('index.html')

@app.route('/base_template')
def index():
	return render_template('base.html')

@app.route('/login', methods = ['GET'])
def show_login():
	return render_template('login.html')

@app.route('/login', methods = ['POST'])
def process_login():
	f = request.form

	user_email = f.get('email')
	user_password = f.get('password')

	user_login = model.session.query(model.Doula).filter_by(email = user_email).filter_by(password = user_password).first()

	print "*******************"
	print "user_login is", user_login

	if not user_login:
		flash("invalid login")
		return redirect('/login')
	else:
		session['email'] = user_email
		flash("You succesfully logged in!")
		print "###############"
		print "session is", session
		return redirect('/')

		

@app.route('/logout')
def logout():
	## FIX THIS SO YOU CAN'T BREAK IT BY LOGGING OUT
	## WHEN YOU HAVEN'T LOGGED IN!
	if not session['email']:
		flash("You have to log in before you log out")
		return redirect('/')
	else:
		del session['email']
	print "###############"
	print "you succesfully logged out"
	print "session is", session
	return redirect('/')



@app.route('/signup_doula', methods = ['GET'])
def signup_doula():
	return render_template('sign-up-doula.html')


@app.route('/signup_doula', methods = ['POST'])
def process_signup_doula():
	# code loosely taken from judgement.py on github
	# form is coming from sign-up-doula.html
	# is this where I should be checking that the password entries match?
	f = request.form
	
	# JUST FOR PROFILE PICTURE
	# Will have to move this code to below the commit, so that i can save the 
	# user first before saving as (usertype/id#) 

	file = request.files['image']
	if file and allowed_file(file.filename):
		filename = secure_filename(file.filename)
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))


	email = f.get('email')
	password = f.get('password')
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



	doula = model.Doula(email = email, 
						password = password, 
						firstname = first_name,
						lastname = last_name,
						practice = practice_name,
						phone = phone_number,
						website = website,
						price_min = price_min,
						price_max = price_max,
						background = background_nar,
						services = services_nar,
						image = filename,
						zipcode = zipcode
						)

	model.session.add(doula)
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
	file = request.files['image']
	if file and allowed_file(file.filename):
		filename = secure_filename(file.filename)
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

	email = f.get('email')
	password = f.get('password')
	first_name = f.get('firstname')
	last_name = f.get('lastname')
	display_name = f.get('display_name')
	zipcode = f.get('zip')
	due_date = f.get('due_date')
	price_min = f.get('price_min')
	price_max = f.get('price_max')
	background_nar = f.get('background_nar')
	ideal_doula_nar = f.get('services')
	visibility = f.get('visibility')
	profile_pic = f.get('image')

	parent = model.Parent(email = email, 
						password = password, 
						firstname = first_name,
						lastname = last_name,
						display_name = display_name,
						due_date = due_date,
						zipcode = zipcode,
						price_min = price_min,
						price_max = price_max,
						background = background_nar,
						ideal_doula_nar = ideal_doula_nar,
						image = filename
						)

	model.session.add(parent)
	model.session.commit()

	return redirect('/')


@app.route('/doula') #change this route to include the doula's <int:id> in the url
def display_doula_profile():
	return render_template('doula-profile.html')


@app.route('/user') #change this route to include the parents's <int:id> in the url
def display_user_profile():
	return render_template('user-profile.html')






if __name__ == '__main__':
	app.debug = True
	app.run()