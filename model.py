#from ratings model.py
import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref

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


class User(Base):
	__tablename__ = "users"

	id = Column(Integer, primary_key = True) #does this need to be in the child class?
	email = Column(String(64), nullable = False)
	password = Column(String(64), nullable = False)
	firstname = Column(String(64), nullable = True)
	lastname = Column(String(64), nullable = True)
	price_min = Column(Integer, nullable = True)
	price_max = Column(Integer, nullable = True)
	background = Column(Text, nullable = True)
	image = Column(String(64), nullable = True)
	zipcode = Column(String(64), nullable = True)

	doula = relationship("Doula", backref=backref("users", order_by=id))

	parent = relationship("Parent", backref=backref("users", order_by=id))

class Doula(Base):
	__tablename__ = "doulas"


	id = Column(Integer, primary_key = True)
	practice = Column(String(64), nullable = True)
	phone = Column(String(20), nullable = True)
	website = Column(String(100), nullable = True)
	services = Column(Text, nullable = True)
	reviews = Column(String(200), nullable = True)
	user_id = Column(Integer, ForeignKey('users.id'), nullable = False)

	


	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		return unicode(self.id)


class Parent(Base):
	__tablename__ = "parents"

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		return unicode(self.id)


	id = Column(Integer, primary_key = True) 
	display_name = Column(String(64), nullable = True)
	ideal_doula_nar = Column(Text, nullable = True)
	visibility = Column(String(64), nullable = True)
	due_date = Column(DateTime, nullable = True)
	user_id = Column(Integer, ForeignKey('users.id'), nullable = False)




def main():
    """In case we need this for something"""
    pass

if __name__ == "__main__":
    main()


