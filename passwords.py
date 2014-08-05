# Password-related functions

from werkzeug.security import generate_password_hash, check_password_hash

def password_check(password, password_again):
	return password == password_again
	
def set_password(password):
	if password:
		pw_hash = generate_password_hash(password)
		return pw_hash

	return ""
