import os
os.environ['DATABASE_URL'] = "sqlite:///doulahoop_tests.db"

import unittest
from app import app
from pyquery import PyQuery as pq




class TestSiteFunctions(unittest.TestCase):
	@classmethod
	def seUpClass(self):
		print os.environ['DATABASE_URL']
		model.create_db()

	def setUp(self):
		self.app = app.test_client() #this uses flask to create test client, which allows us to GET/POST requests like a browser
		


	def test_index_page(self):
		resp = self.app.get('/')
		# resp is a python object

		
		# make sure page loads
		self.assertEqual(resp.status_code, 200)

		q = pq(resp.data)

		jumbotext = q('.jumbotron').text() #looks for jumbotron and returns text, not html
		
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

		assert doula_form # checking that the form exists
		self.assertEqual(len(doula_form), 1) # checking that there is only one form on the page
		assert submit # checking that the button exists
		self.assertEqual(submit[0].value, "Sign Up") # checking that the text in the button is correct

	def test_submit_signup_doula(self):
		data = {}
		resp = self.app.post('/signup_doula', data=data, follow_redirects=True)

		self.assertEqual(resp.status_code, 200)

		# Test that the response page shows the flash error message
		q = pq(resp.data)

		flashes = q('.flashes').text()

		assert "email address" in flashes


		# Test what happens when I post real data
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

		# test that the test database has the test info test
		# maybe copy the setup stuff from the test_db.py so that I'm using the right db

		#query database filter_by email address=test@test.com .all(), should get one record back check length

		#for that record, match the different attributes to the dictionary fields

		








		




if __name__ == '__main__':
    unittest.main()