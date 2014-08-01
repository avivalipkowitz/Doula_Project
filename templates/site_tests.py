import unittest
from app import app

class TestSiteFunctions(unittest.TestCase):
	def setUp(self):
		self.app = app.test_client() #this uses flask to create test client, which allows us to GET/POST requests like a browser


	def test_index_page(self):
		resp = self.app.get('/')
		# resp is a python object

		self.assertEqual(resp.status_code, 200)