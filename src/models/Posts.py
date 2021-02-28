from mongoengine import *

from .Users import Users
from .Comments import Comments

class Posts(Document):
  imageUrl = StringField()
  imageKey = StringField()
  author = ReferenceField(Users)
  description = StringField()
  title = StringField()
  comments = ListField(EmbeddedDocumentField(Comments))
  active = BooleanField(default=False)
  likes = IntField(default=0)