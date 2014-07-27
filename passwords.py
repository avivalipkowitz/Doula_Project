# Password-related functions

from werkzeug.security import generate_password_hash, check_password_hash

def password_check(password, password_again):
	return password == password_again
	
def set_password(password):
	pw_hash = generate_password_hash(password)
	return pw_hash

def check_password(password):
	return check_password_hash(pw_hash, password)
