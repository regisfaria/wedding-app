from mongoengine import *

class EmbeddedUsers(EmbeddedDocument):
  name = StringField()
  imageUrl = StringField()

class Users(Document):
  name = StringField(required=True)
  username = StringField(required=True)
  password = StringField(required=True)
  privileges = StringField()
  imageUrl = StringField()
  imageKey = StringField()
