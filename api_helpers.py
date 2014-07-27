import requests
import json
import os

def geocode_zipcode(zipcode):
	
	key = os.environ.get('GOOGLE_MAPS_API_KEY')
	resp =requests.get('https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s' %(zipcode, key))
	g = json.loads(resp.text) 

	# TODO: Write code to catch and report API key error

	lng = g['results'][0]['geometry']['location']['lng']
	lat = g['results'][0]['geometry']['location']['lat']

	zip_coord = (lat, lng)
	
	return zip_coord