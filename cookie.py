#all the imports
import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from flask.ext.sqlalchemy import SQLAlchemy

#create the app
app = Flask(__name__)
app.config.from_object(__name__)
db = SQLAlchemy(app)


# Load default config and override config from an env variable
app.config.update(dict(
	DATABASE=os.path.join(app.root_path, 'paulspuns.db'),
	SQLALCHEMY_DATABASE_URI = "postgresql://adnanakil@localhost/cookiemedb",
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
	return render_template('payitforward.html')



if __name__ == '__main__':
	port = int(os.environ.get("PORT", 5000))
	app.run()




