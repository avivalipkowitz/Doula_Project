import os
os.environ['DATABASE_URL'] = "sqlite:///doulahoop_tests.db"
import unittest
import api_helpers
import users
import model

class DoulaDBTest(unittest.TestCase):
	@classmethod
	def setUpClass(self):
		print "in setup class"
		model.create_db()

	@classmethod
	def tearDownClass(self):
		print "in class teardown"

class TestDBFunctions(DoulaDBTest):
	
	def setUp(self):
		print "yo dawg"

# TESTS FUNCTIONS FROM api_helpers.py
	# testing geocode_zipcode function
	# geocode_zipcode changes zipcode into coordinates
	def test_example(self):
		self.assertEqual(1 + 1, 2)

	# tests run in alphabetical order, but this needs to go first
	def test_01_create_doula(self):
		data = {
			'email': 'test@test.com',
			'password': "ssshdon'ttell",
			'firstname': 'First',
			'zipcode': '94121',
			# add more data here
		}

		d = model.Doula()
		d.parse_form_data(data)

		model.session.add(d)
		model.session.commit()

		doula_check = model.session.query(model.Doula).filter_by(email=data['email']).one()

		self.assertEqual(doula_check.email, data['email'])		
		self.assertEqual(doula_check.firstname, data['firstname'])		



	# test def zip_radius_search, which queries the database for doulas in that bounding box, and returns doula_list
	# def test_zip_radius_search(self):
	


	# def test_save_user_image(self):
	# 	pass



if __name__ == '__main__':
    unittest.main()