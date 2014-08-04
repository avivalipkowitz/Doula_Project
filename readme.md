DoulaHoop Version 1.0 08/05/14

What is it?
--------------
DoulaHoop is a web app that connects soon-to-be parents to practicing doulas (non-medical childbirth assistants). DoulaHoop helps parents search for doulas based on location, experience, services, availability, and pricing. Doulas benefit from the service through increased web-visibility and access to a wider pool of potential clients. It is built in Python with a Flask framework, and uses a SQLite database.


The latest version
-------------------------
The latest version is 1.0, and was last updated August 5, 2014.





Getting started
--------------------
First, clone this directory to your computer. Then
- Create and activate a new, empty virtual environment.
- Install the packages listed in requirements.txt
- Start the application by running python app.py.
- Head to localhost:5000 to see the app in your browser

What’s inside?
--------------------
-	app.py: This runs the program, and contains all of the Flask app routes.
-	model.py: This sets up and creates the database and user classes. It also contains methods related specifically to adding users to the database.
-	Doulahoop.db: database that stores user information
-	Static folder includes:
o	Templates: these are html templates that use Jinja to render pages to the browser.
o	Images: including webpage images, and user profile pictures (in the Uploads file)
o	Libraries (Jquery, Bootstrap)
o	Custom CSS styles
-	Tests
o	tests.py: unit-tests
o	db_tests.py: tests functions that query the database or store information in the database
o	site_tests.py: tests the Flask framework
-	Helpers: contains files with functions that are imported into app.py to facilitate readability
o	api_helpers.py: methods related specifically to the Google geocoding API
o	forms.py: methods related to creating and processing form information
o	passwords.py: methods related to hashing, storing, and calling passwords
o	users.py: methods related to creating user accounts, and displaying profile pages




Contact information
------------------------
Email: avivalipkowitz@gmail.com

