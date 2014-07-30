import requests
import json
import os
import model

def geocode_zipcode(zipcode):
	
	key = os.environ.get('GOOGLE_MAPS_API_KEY')
	resp =requests.get('https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s' %(zipcode, key))
	g = json.loads(resp.text) 

	# TODO: Write code to catch and report API key error

	lng = g['results'][0]['geometry']['location']['lng']
	lat = g['results'][0]['geometry']['location']['lat']

	zip_coord = (lat, lng)
	
	return zip_coord


def min_max_lat_search(lat, search_radius):
# lat is approximately 0.01237125 degrees per mile
# redo later to account for curvature of the earth
	min_lat = lat - (search_radius * 0.01237125)
	max_lat = lat + (search_radius * 0.01237125)
	return (min_lat, max_lat)

def min_max_lng_search(lng, search_radius):
# lng is approximately 0.0151902 degrees per mile
# redo later to account for curvature of the earth
	min_lng = lng - (search_radius * 0.0151902)
	max_lng = lng + (search_radius * 0.0151902)
	return (min_lng, max_lng)

# TODO: create test for this in tests.py
def create_bounding_box(search_zip, radius):
	lat, lng = geocode_zipcode(search_zip)

	min_lat, max_lat = min_max_lat_search(lat, radius)
	min_lng, max_lng = min_max_lng_search(lng, radius)

	return (min_lat, max_lat, min_lng, max_lng)

# TODO: create test for this in db_tests.py
def zip_radius_search(min_lat, max_lat, min_lng, max_lng):
	doula_list = model.session.query(model.Doula).\
		filter(model.Doula.zipcode_lat >= min_lat).\
		filter(model.Doula.zipcode_lat <= max_lat).\
		filter(model.Doula.zipcode_lng >= min_lng).\
		filter(model.Doula.zipcode_lng <= max_lng).all()

	return doula_list
