import datetime

from flask import request
from mongoengine import *

class Topic(Document):
    topic = StringField(max_length=200, required=True, unique=True)
    date_added = DateTimeField(default=datetime.datetime.now)
    ip = StringField(required=True)

    def save(self, **kwargs):
        if self.ip is None and request:
            self.ip = request.remote_addr
        super(Topic, self).save(**kwargs)

class Votes(Document):
    rating = IntField(min_value=-1, max_value=1, required=True)
    ip = StringField(required=True, unique_with='topic')
    topic = ReferenceField(Topic, required=True)
