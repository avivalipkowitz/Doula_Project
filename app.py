from flask import Flask, request, session, render_template, g, redirect, url_for, flash
import jinja2

app = Flask(__name__)


@app.route('/')
def index():
	return render_template('base.html')


@app.route('/login')
def

if __name__ == '__main__':
	app.debug = True
	app.run()