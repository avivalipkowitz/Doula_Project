import unittest
import api_helpers
import users
import model

class DoulaDBTest(unittest.TestCase):
	@classmethod
	def setUpClass(self):
		print "in setup class"
		a = "cat"

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

	def test_example2(self):
		# print "a is %r" % a
		self.assertEqual(1 + 1, 2)


	# test def zip_radius_search, which queries the database for doulas in that bounding box, and returns doula_list
	# def test_zip_radius_search(self):
	


	# def test_save_user_image(self):
	# 	pass



if __name__ == '__main__':
    unittest.main()