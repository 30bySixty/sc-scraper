from flask_sqlalchemy import SQLAlchemy, event
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy import func
import time

db = SQLAlchemy(session_options={"expire_on_commit": False})

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
TABLES
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
class listings(db.Model):
	id = db.Column('id', db.Integer, primary_key=True)
	time = db.Column(db.Integer, default=time.time)
	link = db.Column(db.Text)
	title = db.Column(db.Text)
	price = db.Column(db.Integer)
	cl_id = db.Column(db.Text, unique=True)
	neighborhood = db.Column(db.Text)
	bedrooms = db.Column(db.Integer)
	ft2 = db.Column(db.Integer)
	ideal_filters = db.Column(db.Boolean)
	
	def __init__(self, link, title, price, neighborhood, bedrooms, cl_id, ft2, ideal_filters):
		self.link = link
		self.title = title
		self.price = price
		self.cl_id = cl_id
		self.neighborhood = neighborhood
		self.bedrooms = bedrooms
		self.ft2 = ft2
		self.ideal_filters = ideal_filters