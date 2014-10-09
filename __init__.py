import os
from flask import Flask


app = Flask(__name__)
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'events.db'),
    DEBUG=True,
    SECRET_KEY='workingkey',
    USE_EMAIL=True,
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 465,
    MAIL_USE_TLS = False,
    MAIL_USE_SSL = True,
    MAIL_USERNAME = 'request.calendar.noreply@gmail.com',
    MAIL_PASSWORD = 'Request30Calendar'
))

## Admin setup

## Email setup
if app.config['USE_EMAIL']:
	from flask.ext.mail import Mail, Message
	mail = Mail(app)

## Shared resource setup




import RequestCalendar.webapp