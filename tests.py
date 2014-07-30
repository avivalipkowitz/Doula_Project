import unittest
import api_helpers
import users
import model

class TestFunctions(unittest.TestCase):
	
# TESTS FUNCTIONS FROM api_helpers.py
	# testing geocode_zipcode function
	# geocode_zipcode changes zipcode into coordinates
	def test_coordinates(self):
		zipcode = 94612
		test_coordinate = (37.811315899999997, -122.2682245)

		self.assertEqual(api_helpers.geocode_zipcode(zipcode), test_coordinate)

	# test min_max_lat_search and min_max_lng_search functions, which generate the bouding box coordinates
	def test_min_max_lat_search(self):
		lat = 37
		search_radius = 5
		min_lat = 37 - (5 * 0.01237125)
		max_lat = 37 + (5 * 0.01237125)

		min_max_lat = (min_lat, max_lat)

		self.assertEqual(api_helpers.min_max_lat_search(37, 5), min_max_lat)


	def test_min_max_lng_search(self):
		lat = -122
		search_radius = 5
		min_lng = -122 - (5 * 0.0151902)
		max_lng = -122 + (5 * 0.0151902)

		min_max_lng = (min_lng, max_lng)

		self.assertEqual(api_helpers.min_max_lng_search(-122, 5), min_max_lng)
		

	



# TESTS FUNCTIONS FROM users.py
	
	# checks file upload name to make sure it's allowed
	def test_allowed_file(self):
		ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
		filename = "profile_pic.jpg"
		bad_filename = "file.pxt"
		self.assertEqual(users.allowed_file(filename), True)
		self.assertNotEqual(users.allowed_file(bad_filename), True)

	# returns the extension string
	def test_file_extension(self):
		filename = "profile.jpg"
		bad_filename = "profile"
		self.assertEqual(users.file_extension(filename), "jpg")
		# this should also be testing to make sure that you can't submit a filename with no extension, but I have yet to write that into the function	

	# checks the role in order to query the correct database
	def test_which_database(self):
		self.assertEqual(users.which_database("doula"), model.Doula)
		self.assertEqual(users.which_database("parent"), model.Parent)
		self.assertEqual(users.which_database("asdf"), None)






if __name__ == '__main__':
    unittest.main()