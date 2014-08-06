import os
os.environ['DATABASE_URL'] = "sqlite:///doulahoop_tests.db"

import model
import passwords
import unittest
from app import app
from pyquery import PyQuery as pq




class TestSiteFunctions(unittest.TestCase):
	@classmethod
	def seUpClass(self):
		print os.environ['DATABASE_URL']
		model.create_db()

	def setUp(self):
		#this uses flask to create test client, which allows us to GET/POST requests like a browser
		self.app = app.test_client() 
		
		


	def test_index_page(self):
		# resp is a python object
		resp = self.app.get('/')
		

		
		# make sure page loads
		self.assertEqual(resp.status_code, 200)

		q = pq(resp.data)

		#looks for jumbotron and returns text, not html
		jumbotext = q('.jumbotron').text() 

		assert "I'm a parent" in jumbotext
		assert "I'm a doula" in jumbotext

	def test_load_signup_doula(self):
		resp = self.app.get('/signup_doula')

		# check that page loads
		self.assertEqual(resp.status_code, 200)

		# check that important pieces are in place
		q = pq(resp.data)

		doula_form = q('#signup_table')
		submit = q('#doula_signup')

		# checking that the form exists
		assert doula_form 
		
		# checking that there is only one form on the page
		self.assertEqual(len(doula_form), 1) 
		# checking that the button exists
		assert submit 
		# checking that the text in the button is correct
		self.assertEqual(submit[0].value, "Sign Up") 

	def test_submit_signup_doula(self):
		data = {}
		resp = self.app.post('/signup_doula', data=data, follow_redirects=True)

		self.assertEqual(resp.status_code, 200)

		# Pt1: Test that the response page shows the flash error message
		q = pq(resp.data)

		flashes = q('.flashes').text()

		assert "email address" in flashes


		# Pt2: Test what happens when I post real data
		data = {
			'email': 'test@test.com',
			'password': 'password',
			'password_again': 'password',
			'zipcode': '94607',
			'image': 'pic.jpg'

		}	

		resp = self.app.post('/signup_doula', data = data)

		# test that successful post leads to redirect
		self.assertEqual(resp.status_code, 302)



		# Pt3: Test that the test database has the test info test
	
		# test that only one record exists in the test database
		doula_list = model.session.query(model.Doula).filter_by(email="test@test.com").all()

		self.assertEqual(len(doula_list), 1)

		# test that attributes of the database record match the attributes listed in the dictionary
		doula = doula_list[0]

		self.assertEqual(doula.email, data['email'])
		self.assertEqual(passwords.check_password_hash(doula.password, data['password']), True)
		self.assertEqual(doula.zipcode, data['zipcode'])
		self.assertEqual(doula.image, data['image'])

		# Repeat above tests for parent case

if __name__ == '__main__':
    unittest.main()