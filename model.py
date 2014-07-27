#from ratings model.py
import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from werkzeug.security import generate_password_hash, check_password_hash

#from ratings tutorial
ENGINE = None
Session = None

# from ratings model.py
engine = create_engine("sqlite:///doulahoop.db", echo = False)
session = scoped_session(sessionmaker(bind = engine,
									  autocommit = False,
									  autoflush = False))

# from ratings model.py
Base = declarative_base()
Base.query = session.query_property()


# From ratings model.py
# Class declarations
# Add a User(Base) class that has all common attributes between 
# Parent and Doula, so that this doesn't have to be replicated

# Methods from salty passwords tutorial. I don't think they should be class methods though, so I pulled them out here.
# def set_password(password):
# 	pw_hash = generate_password_hash(password)
# 	return pw_hash

# def check_password(password):
# 	return check_password_hash(pw_hash, password)

class Doula(Base):
	__tablename__ = "doulas"


	id = Column(Integer, primary_key = True)
	email = Column(String(64), nullable = False)
	password = Column(String(64), nullable = False)
	firstname = Column(String(64), nullable = True)
	lastname = Column(String(64), nullable = True)
	price_min = Column(Integer, nullable = True)
	price_max = Column(Integer, nullable = True)
	background = Column(Text, nullable = True)
	image = Column(String(64), nullable = True)
	zipcode = Column(String(64), nullable = True)
	zipcode_lat = Column(Integer, nullable = True)
	zipcode_lng = Column(Integer, nullable = True)
	practice = Column(String(64), nullable = True)
	phone = Column(String(20), nullable = True)
	website = Column(String(100), nullable = True)
	services = Column(Text, nullable = True)
	reviews = Column(String(200), nullable = True)
	

	# From flask password salt turtorial


	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		return unicode(self.id)

	def is_doula(self):
		return True


class Parent(Base):
	__tablename__ = "parents"


	id = Column(Integer, primary_key = True) 
	email = Column(String(64), nullable = False)
	password = Column(String(64), nullable = False)
	firstname = Column(String(64), nullable = True)
	lastname = Column(String(64), nullable = True)
	price_min = Column(Integer, nullable = True)
	price_max = Column(Integer, nullable = True)
	background = Column(Text, nullable = True)
	image = Column(String(64), nullable = True)
	zipcode = Column(String(64), nullable = True)
	zipcode_lat = Column(Integer, nullable = True)
	zipcode_lng = Column(Integer, nullable = True)
	display_name = Column(String(64), nullable = True)
	ideal_doula_nar = Column(Text, nullable = True)
	visibility = Column(String(64), nullable = True)
	due_date = Column(DateTime, nullable = True)


	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		return unicode(self.id)

	def is_doula(self):
		return False


def main():
    """In case we need this for something"""
    pass

if __name__ == "__main__":
    main()


