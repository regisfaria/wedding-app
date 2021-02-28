import mongoengine as mongo

class Users(mongo.Document):
  name = mongo.StringField(required=True)
  username = mongo.StringField(required=True)
  password = mongo.StringField(required=True)
  privileges = mongo.StringField()
  imageUrl = mongo.StringField()
  imageKey = mongo.StringField()
