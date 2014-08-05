#from ratings model.py

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import ForeignKey
from werkzeug.security import generate_password_hash, check_password_hash
import os
import passwords
import datetime
import time

ENGINE = None
Session = None

# print "[model] DATABASE_URL: ", os.environ.get('DATABASE_URL')
engine = create_engine(os.environ.get('DATABASE_URL', "sqlite:///doulahoop.db"), echo = False)

session = scoped_session(sessionmaker(bind = engine,
									  autocommit = False,
									  autoflush = False))

Base = declarative_base()
Base.query = session.query_property()

def connect_db(db):
	engine = create_engine(db, echo = False)
	session = scoped_session(sessionmaker(bind = engine,
									  autocommit = False,
									  autoflush = False))
	print "[model] DATABASE_URL: ", os.environ.get('DATABASE_URL')

def create_db():
	Base.metadata.create_all(engine)

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

	def parse_form_data(self, data):
		self.email = data.get('email')
		self.firstname = data.get('firstname')
		self.lastname = data.get('lastname')
		self.price_min = data.get('price_min')
		self.price_max = data.get('price_max')
		self.background = data.get('background')
		self.image = data.get('image')
		self.zipcode = data.get('zipcode')
		self.practice = data.get('practice')
		self.phone = data.get('phone')
		self.website = data.get('website')
		self.services = data.get('services')

		password = data.get('password')
		hashed_pw = passwords.set_password(password)
		self.password = hashed_pw

	def store_coordinates(self, lat, lng):
		self.zipcode_lat = lat
		self.zipcode_lng = lng

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


	def parse_parent_form_data(self, data):
		self.email = data.get('email')
		self.firstname = data.get('firstname')
		self.lastname = data.get('lastname')
		self.price_min = data.get('price_min')
		self.price_max = data.get('price_max')
		self.background = data.get('background')
		self.image = data.get('image')
		self.zipcode = data.get('zipcode')
		self.practice = data.get('practice')
		self.display_name = data.get('display_name')
		self.ideal_doula_nar = data.get('ideal_doula_nar')
		self.visibility = data.get('visibility')

		password = data.get('password')
		hashed_pw = passwords.set_password(password)
		self.password = hashed_pw

		unicode_due_date = data.get('due_date')
		self.due_date = datetime.datetime.strptime(data.get('due_date'), "%Y-%m-%d")

	def store_coordinates(self, lat, lng):
		self.zipcode_lat = lat
		self.zipcode_lng = lng

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