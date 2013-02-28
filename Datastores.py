from google.appengine.ext import db

class Categories(db.Model):
  category = db.StringProperty()
  owner = db.StringProperty()
  expDate = db.DateProperty()

class Items(db.Model):
  category = db.StringProperty()
  owner = db.StringProperty()
  item = db.StringProperty()
  
class Votes(db.Model):
  category = db.StringProperty()
  owner = db.StringProperty()
  winner = db.StringProperty()
  loser = db.StringProperty()

class Results(db.Model):
  category = db.StringProperty()
  owner = db.StringProperty()
  item = db.StringProperty()
  winCount = db.IntegerProperty()
  lossCount = db.IntegerProperty()
  winPercent = db.IntegerProperty()
  

