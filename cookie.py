#all the imports
import os
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from flask.ext.sqlalchemy import SQLAlchemy
from requests.auth import HTTPBasicAuth
import requests
#from flask.ext.heroku import Heroku

#create the app
app = Flask(__name__)
app.config.from_object(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)


# Load default config and override config from an env variable
app.config.update(dict(
	DATABASE=os.path.join(app.root_path, 'paulspuns.db'),
	#SQLALCHEMY_DATABASE_URI = "postgresql://adnanakil@localhost/cookiemedb",
	SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL","postgresql://adnanakil@localhost/cookiemedb"),
	DEBUG=True,
	SECRET_KEY = 'development key',
	USERNAME = 'admin',
	PASSWORD = 'default'
))

#app.config.from_envvar('PAULSPUNS_SETTINGS', silent=True)

class CookieMe(db.Model):
    __tablename__ = 'orders'
    id = db.Column('id', db.Integer, primary_key=True)
    address = db.Column(db.String(60))
 
    def __init__(self, address):
        self.address = address

@app.route('/')
def cookieme():
	return render_template('showme.html')

@app.route('/payitforward', methods=['POST'])
def payitforward():
	todo = CookieMe(request.form['text'])
	db.session.add(todo)
	db.session.commit()
	data = {"manifest":"a box of cookies",
	"pickup_name":"Cookie House",
	"pickup_address":"410 Shrader St. Apt 3, San Francisco, CA",
	"pickup_phone_number":"201-757-0419",
	"pickup_notes":"Optional note that this is Invoice #123",
	"dropoff_name":"Santas Helper",
	"dropoff_address":request.form['text'],
	"dropoff_phone_number":"619-940-4352"}
	#r = requests.post('https://api.postmates.com/v1/customers/'+ os.environ.get('PMATES_CUSTOMERID') +'/deliveries', data = data, auth=HTTPBasicAuth(os.environ.get('PMATES_TESTAPIKEY'), ''))
	r = requests.post('https://api.postmates.com/v1/customers/'+ os.environ.get('PMATES_CUSTOMERID') +'/deliveries', data = data, auth=HTTPBasicAuth(os.environ.get('PMATES_PROD_APIKEY'), ''))
	return render_template('payitforward.html')



if __name__ == '__main__':
	port = int(os.environ.get("PORT", 5000))
	app.run()




