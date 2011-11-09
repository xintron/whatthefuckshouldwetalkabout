from flask import Flask
from mongoengine import connect

app = Flask(__name__)
app.config.from_object('flaskr.settings')

connect(app.config['DATABASE_NAME'])

import flaskr.views
