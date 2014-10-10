import os
from flask import Flask

## Config is set up from a default file that loads every time

##User Admin can edit custom settings file which overwrites is necessary

print "INITALISING APP"
app = Flask(__name__)

##Default config
app.config.from_object('RequestCalendar.defaultSettings')


##User config
app.config.from_object

## Email setup
if app.config['USE_EMAIL']:
	from flask.ext.mail import Mail
	mail = Mail(app)

## Shared resource setup




import RequestCalendar.webapp