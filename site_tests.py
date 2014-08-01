import unittest
from app import app
from pyquery import PyQuery as pq

class TestSiteFunctions(unittest.TestCase):
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

	def test_signup_doula_page(self):
		resp = self.app.get('/signup_doula')

		# check that page loads
		self.assertEqual(resp.status_code, 200)

		# check that important pieces are in place
		q = pq(resp.data)

		doula_form = q('#login_table').text()
		submit = q('#doula_signup').text()

		assert "First name" in doula_form
		assert "submit" in submit


		




if __name__ == '__main__':
    unittest.main()