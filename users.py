from flask import Flask, Response, request, session, render_template, g, redirect, url_for, flash
from flask.ext.login import LoginManager, login_required, logout_user, login_user, current_user
import model
import os

# Following code is from flask.pocoo.org/docs/patterns/fileuploads
UPLOAD_FOLDER = 'static/images/uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

# TODO: make private
def allowed_file(filename):
	return '.' in filename and \
		filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

# TODO: make private
def file_extension(filename):
	return filename.split('.')[-1]

def which_database(role):
	# TODO: explain why this is here wrt to database
	if role == "doula":
		return model.Doula
	else:
		return model.Parent		

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

