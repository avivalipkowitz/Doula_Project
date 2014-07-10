from flask import Flask, request, session, render_template, g, redirect, url_for, flash
import jinja2
import model

app = Flask(__name__)
SECRET_KEY = "fish"
app.config.from_object(__name__)


@app.route('/')
def index():
	return render_template('base.html')

@app.route('/index')
def home_page():
	return render_template('index.html')


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
		print "invalid login"
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



@app.route('/signup', methods = ['GET'])
def process_signup():
	return render_template('sign-up.html')


@app.route('/signup', methods = ['POST'])
def signup():
	f = request.form

	user_email = f.get('email')
	user_password = f.get('password')

	user_login = model.session.query(model.Doula).filter_by(email = user_email).filter_by(password = user_password).first()

	print "*******************"
	print "user_login is", user_login

	if not user_login:
		print "invalid login"
	else:
		session['email'] = user_email
		flash("You succesfully logged in!")

	return redirect('/')





if __name__ == '__main__':
	app.debug = True
	app.run()