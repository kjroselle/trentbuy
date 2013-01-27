import datetime
from google.appengine.ext import db

class AmmoPriceItem(db.Model):
  name = db.StringProperty()
  sku = db.StringProperty()
  caliber = db.StringProperty()
  amount = db.IntegerProperty()
  regprice = db.FloatProperty()
  saleprice = db.FloatProperty()
  date = db.DateTimeProperty()
  stock = db.StringProperty()

class ProductItem(db.Model):
  name = db.StringProperty()
  sku = db.StringProperty()
  model = db.StringProperty()
  regprice = db.FloatProperty()
  saleprice = db.FloatProperty()
  date = db.DateProperty()
  stock = db.StringProperty()