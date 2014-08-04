import os
os.environ['DATABASE_URL'] = "sqlite:///doulahoop_tests.db"
import unittest
import api_helpers
import users
import model
import passwords
import datetime



class TestDBFunctions(unittest.TestCase):
	@classmethod
	def setUpClass(self):
		print "in setup class"
		#reset test database
		model.session.execute('DELETE FROM doulas') 
		model.session.execute('DELETE FROM parents')
		model.create_db()

		# Populate some sample doula data to use in our tests

	@classmethod
	def tearDownClass(self):
		print "in class teardown"
		# delete doulas from db

	
	def setUp(self):
		pass

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
			'zipcode': '21043',
			'zipcode_lat': 39.2369558,
			'zipcode_lng': -76.79135579999999,
			'website': 'http://www.test.com',
			'price_min': 300,
			'price_max': 500,
			'background': 'I really love my job!',
			'services': "I'll make you pancakes all day long.",
			'image': 'doula_1.jpg',
			'phone': '555-555-5555'

		}
		lat = 39.2369558
		lng = -76.79135579999999

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

	def test_02_create_parent(self):
		# test set-up

		data = {
			'email': 'test@test.com',
			'password': "ssshdon'ttell",
			'firstname': 'First',
			'lastname': 'Last',
			'price_min': 300,
			'price_max': 500,
			'background': 'I really love my job!',
			'image': 'parent_1.jpg',
			'zipcode': '21043',
			'zipcode_lat': 39.2369558,
			'zipcode_lng': -76.79135579999999,
			'display_name': 'FirstLast',
			'ideal_doula_nar': "I want someone who makes pancakes",
			'visibility': 'none',
			'due_date': "2015-01-20 00:00:00.000000"
		}

		lat = 39.2369558
		lng = -76.79135579999999

		users.db_add_parent(data)

		parent_check = model.session.query(model.Parent).filter_by(email=data['email']).one()


		due_date = datetime.datetime.strptime(data.get('due_date'), "%Y-%m-%d %H:%M:%S.%f")

		# tests
		self.assertEqual(parent_check.email, data['email'])		
		self.assertTrue(passwords.check_password_hash(parent_check.password, data['password']))
		self.assertEqual(parent_check.firstname, data['firstname'])
		self.assertEqual(parent_check.lastname, data['lastname'])
		self.assertEqual(parent_check.price_min, data['price_min'])
		self.assertEqual(parent_check.price_max, data['price_max'])
		self.assertEqual(parent_check.background, data['background'])
		self.assertEqual(parent_check.image, data['image'])
		self.assertEqual(parent_check.zipcode, data['zipcode'])		
		self.assertEqual(parent_check.zipcode_lat, data['zipcode_lat'])
		self.assertEqual(parent_check.zipcode_lng, data['zipcode_lng'])	
		self.assertEqual(parent_check.display_name, data['display_name'])
		self.assertEqual(parent_check.ideal_doula_nar, data['ideal_doula_nar'])
		self.assertEqual(parent_check.visibility, data['visibility'])

		self.assertEqual(parent_check.due_date, due_date)

	def test_save_user_image(self):
		pass




	# test def zip_radius_search, which queries the database for doulas in that bounding box, and returns doula_list
	def test_02_zip_radius_search(self):


		# test set-up
	
		
		# this doula should come up in all zipcode ranges, including <=5 mi
		doula1_data = {
			'firstname': 'doula1',
			'email': 'doula1@test.com',
			'password': 'password',
			'zipcode': 94115,
		}
	 
		# this doula should come up only in searches <= 10mi
		doula2_data = {
			'firstname': 'doula2',
			'email': 'doula2@test.com',
			'password': 'password',
			'zipcode': 94965,
		}

		# this doula should come up only in searches <= 25mi
		doula3_data = {
			'firstname': 'doula3',
			'email': 'doula3@test.com',
			'password': 'password',
			'zipcode': 94563,
		}

		# this doula should not come up in any zipcode searches
		doula4_data = {
			'firstname': 'doula4',
			'email': 'doula4@test.com',
			'password': 'password',
			'zipcode': 94513,
		}

		users.db_add_doula(doula1_data)
		users.db_add_doula(doula2_data)
		users.db_add_doula(doula3_data)
		users.db_add_doula(doula4_data)

		doula_list5 = ['doula1']
		doula_list10 = ['doula1', 'doula2']
		doula_list25 = ['doula1', 'doula2', 'doula3']

		
		# set-up for search_radius = 5
		zipcode = 94121
		zip_radius_list = [5, 10, 25]
		for radius in zip_radius_list:
			min_lat, max_lat, min_lng, max_lng = api_helpers.create_bounding_box(zipcode, radius)
			doula_obj_list = api_helpers.zip_radius_search(min_lat, max_lat, min_lng, max_lng)
			doula_name_list = []
			for doula in doula_obj_list:
				doula_name_list.append(doula.firstname)

			if radius == 5:
				self.assertEqual(doula_list5, doula_name_list)
			elif radius == 10:
				self.assertEqual(doula_list10, doula_name_list)
			elif radius == 25:
				self.assertEqual(doula_list25, doula_name_list)

		


		


	



if __name__ == '__main__':
    unittest.main()