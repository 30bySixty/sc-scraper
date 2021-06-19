# from slackbot.slackclient import SlackClient
from flask import session
from sqlalchemy import func
import os
import slack
import time
import settings
from slack import WebClient
from slack.errors import SlackApiError
from db import *
import pycraigslist 

def do_scrape(zip, ideal_filters):
	"""
	Scrape scrape scrape
	"""
	
	results = []
	
	if ideal_filters == True:
		apartment_filters = {
			"has_image": True,
			"max_price": settings.MAX_PRICE,
			"min_bedrooms": 2,
			"min_bathrooms": 2,
			"zip_code": zip,
			"laundry": "w/d in unit",
			"cats_ok": True
		}
	else:
		apartment_filters = {
			"has_image": True,
			"max_price": settings.MAX_PRICE,
			"min_bedrooms": 2,
			"zip_code": zip
		}
	
	# Get apartments
	try:
		searchHomes = pycraigslist.housing.apa(site = settings.CRAIGSLIST_SITE, area = settings.AREA, filters = apartment_filters)
		homes = searchHomes.search(limit = 2000)

		# Get sublets
		searchSubs = pycraigslist.housing.sub(site = settings.CRAIGSLIST_SITE, area = settings.AREA, filters = apartment_filters)
		subs = searchSubs.search(limit = 2000)
		
		results = []
		for eachHome in homes:
			results.append(eachHome)

		for eachSub in subs:
			results.append(eachSub)
		
		# Get all listings in the database
		allListings = listings.query.all()
		
		newListing = ''
		
		result_strings = []
		
		for result in results:
			try:
				resultID = result['id']
			except:
				print('no result ID')
				continue
			
			# Don't store the listing if it already exists.
			if any(x.cl_id == resultID for x in allListings):
				print('listing already scraped')
				continue
			
			# Process listing
			print('processing new listing')
			
			# Does this match exactly what we want?
			result_string = ''
			if ideal_filters == True:
				result_string += '** EXACT MATCH ** '
				
			else:
				result_string += '(Partial Match) '
			
			result_string += 'Found an apartment on Craigslist!'
			
			# Try parsing the price.
			price = 0
			try:
				price = float(result['price'].replace("$", ""))
				result_string += ' | Price: $' + price
			except Exception:
				pass
			
			# Try parsing the bedrooms
			bedrooms = 0
			try:
				bedrooms = result['bedrooms']
				result_string += ' | Bedrooms: ' + bedrooms
			except Exception:
				pass
			
			# Try parsing the neighborhood
			neighborhood = "scz"
			try:
				neighborhood = result['neighborhood']
				result_string += ' | Neighborhood: ' + neighborhood
			except Exception:
				pass
			
			# Try parsing the sqft
			ft2 = 0
			try:
				ft2 = result['area-ft2']
				result_string += ' | Size: ' + ft2 + 'sqft'
			except Exception:
				pass
				
			result_string += ' | Link: <' + result['url'] + '>'
			
			# Create the listing object in the database			
			newListing = listings(
				link=result['url'],
				title=result['title'],
				bedrooms=bedrooms,
				neighborhood=neighborhood,
				price=price,
				cl_id=result['id'],
				ft2 = ft2,
				ideal_filters = ideal_filters
			)
			
			# Save the listing so we don't grab it again.
			db.session.add(newListing)
			
			# Add the message to the list
			result_strings.append(result_string)
				
		print('done scraping!')
		print('results length is:', len(results))
		
		if newListing != '':
			try:
				print('saving listings in db')
				db.session.commit()
				
			except Exception as e:
				print('error ' + str(e))
				session.rollback()
		
		print(result_strings)
		
		return result_strings
			
	except MaximumRequestsError:
		print("Yikes! Something's up with the network.")