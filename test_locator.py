import unittest
import api_helpers

class TestLocatorFunctions(unittest.TestCase):
	
	def setUp(self):
		zipcode = 94612
		self.coordinates = api_helpers.geocode_zipcode(zipcode)

	def test_coordinates(self):
		test_coordinate = (37.811315899999997, -122.2682245)
		self.assertEqual(self.coordinates, test_coordinate)

	# def test_generate_zipcode(self):
	# 	pass

	# def test_api_key(self):
	# 	pass

if __name__ == '__main__':
    unittest.main()