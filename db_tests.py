import os
os.environ['DATABASE_URL'] = "sqlite:///doulahoop_tests.db"
import unittest
import api_helpers
import users
import model
import passwords


class DoulaDBTest(unittest.TestCase):
	@classmethod
	def setUpClass(self):
		print "in setup class"
		model.create_db()

		# Populate some sample doula data to use in our tests

	@classmethod
	def tearDownClass(self):
		print "in class teardown"
		# delete doulas from db

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
		# test set-up
		data = {
			'email': 'test@test.com',
			'password': "ssshdon'ttell",
			'firstname': 'First',
			'lastname': 'Last',
			'practice': 'DoulaTime',
			'zipcode': '94121',
			'zipcode_lat': 37.7813454,
			'zipcode_lng': -122.497668,
			'website': 'http://www.test.com',
			'price_min': 300,
			'price_max': 500,
			'background': 'I really love my job!',
			'services': "I'll make you pancakes all day long.",
			'image': 'doula_1.jpg',
			'phone': '555-555-5555'

		}
		lat = 37
		lng = -121

		users.db_add_doula(data)

		doula_check = model.session.query(model.Doula).filter_by(email=data['email']).one()

		# tests
		self.assertEqual(doula_check.email, data['email'])		
		self.assertTrue(passwords.check_password_hash(doula_check.password, data['password']))
		self.assertEqual(doula_check.firstname, data['firstname'])
		self.assertEqual(doula_check.lastname, data['lastname'])
		self.assertEqual(doula_check.practice, data['practice'])	
		self.assertEqual(doula_check.zipcode, data['zipcode'])		
		self.assertEqual(doula_check.zipcode_lat, data['zipcode_lat'])
		self.assertEqual(doula_check.zipcode_lng, data['zipcode_lng'])	
		self.assertEqual(doula_check.website, data['website'])
		self.assertEqual(doula_check.price_min, data['price_min'])
		self.assertEqual(doula_check.price_max, data['price_max'])
		self.assertEqual(doula_check.zipcode_lat, data['zipcode_lat'])
		self.assertEqual(doula_check.background, data['background'])
		self.assertEqual(doula_check.services, data['services'])
		self.assertEqual(doula_check.image, data['image'])
		self.assertEqual(doula_check.phone, data['phone'])

	# def test_save_user_image(self):
	# 	pass




	# test def zip_radius_search, which queries the database for doulas in that bounding box, and returns doula_list
	def test_02_zip_radius_search(self):


		# test set-up
		zipcode = 94607
		
		# this doula should come up in all zipcode ranges, including <=5 mi
		doula1_data = {
			'firstname': 'doula1',
			'email': 'doula1@test.com',
			'zipcode': 94607,
		}
	 
		# this doula should come up only in searches <= 10mi
		doula3_data = {
			'firstname': 'doula3',
			'zipcode': 94706,
		}

		# this doula should come up only in searches <= 25mi
		doula3_data = {
			'firstname': 'doula3',
			'zipcode': 94549,
		}

		# this doula should not come up in any zipcode searches
		doula4_data = {
			'firstname': 'doula4',
			'zipcode': 94513,
		}

		
		
		


		


	



if __name__ == '__main__':
    unittest.main()