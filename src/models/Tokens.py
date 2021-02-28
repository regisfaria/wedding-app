from mongoengine import *

from .Users import Users

class Tokens(Document):
  token = StringField()
  createdAt = StringField()
  user = ReferenceField(Users)
