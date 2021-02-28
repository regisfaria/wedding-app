from mongoengine import *

from .Users import Users

class Comments(EmbeddedDocument):
  identifier = StringField()
  content = StringField()
  author = ReferenceField(Users)
  authorName = StringField()
  imageUrl = StringField()