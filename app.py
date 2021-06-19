from flask import Flask, g, request, session
from flask_session import Session
from flask_migrate import Migrate
from flask_script import Manager
from scraper import do_scrape
from helpers import post_chat_to_slack
import time
import sys
import datetime
import json
import traceback
import settings
from db import *

###################
## Configuration
###################
def run_on_start():
	"""
	Run the craigslist scraper, and post data to slack
	"""
	run_scrape = True
	
	while run_scrape == True:
		zip_codes = settings.ZIP_CODES
		
		#Search what we REALLY want
		for zip_code in zip_codes:
		
			all_results = []
			all_results = do_scrape(zip_code, True)
			
			# Post each result to slack
			for result in all_results:
				message = result
				
				post_chat_to_slack(message)
		
		#Search things where the listing might just be ok
		for zip_code in zip_codes:
		
			all_results = []
			all_results = do_scrape(zip_code, False)
			
			# Post each result to slack
			for result in all_results:
				message = result
				
				post_chat_to_slack(message)
			
		time.sleep(settings.SLEEP_INTERVAL) # 20 minutes

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'false'
app.config['SQLALCHEMY_ECHO'] = True

migrate = Migrate(app, db)

app.config.from_pyfile('config.cfg')

db.init_app(app)
with app.app_context():
	db.create_all()
	
app.config['SESSION_TYPE'] = 'sqlalchemy'

try:
	app.config['SESSION_SQLALCHEMY'] = db
	Session(app)
	with app.app_context():
		db.create_all()
		print('set up db')
		run_on_start()
except:
	del app.config['SESSION_SQLALCHEMY']
	Session(app)

manager = Manager(app)
@manager.command
def running():
	app.run('0.0.0.0', 8080)
	run_on_start()

###################
## Start the app
###################

app.secret_key = app.config['SECRET_KEY']
if __name__ == "__main__":
	# app.run('0.0.0.0', 8080)
	manager.run()
	
# Command(s) to run the server:
# flask run
## ^ Prints messages to server
# python3 app.py
## ^ Does not print to the server

###################
## Debugging
###################

# import code; code.interact(local=dict(globals(), **locals()))