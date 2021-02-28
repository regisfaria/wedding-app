from flask_mongoengine import MongoEngine

class Database:
  def __init__(self, app):
    app.config["MONGODB_SETTINGS"] = {"db": "wedding_app", "host": "localhost", "port": 27017}
    
    self.db = MongoEngine()
    self.db.init_app(app)