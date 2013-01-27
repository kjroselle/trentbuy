from google.appengine.ext import db
import os
from google.appengine.ext.webapp import template
from data import AmmoPriceItem
import logging
import datetime
import webapp2

class MainHandler(webapp2.RequestHandler):
  def get(self):
    q = db.GqlQuery("SELECT model FROM ProductItem")
    
    # make list of models
    modelList = []
    for item in q:
      # date = str(item.date.day) + '.' + str(item.date.month) + '.' + str(item.date.year)
      # print item.sku + ", " + date
      modelList.append(item.model)
      
    # convert list to a set, one sku per plot line and sort
    modelSet = sorted(list(set(modelList)))
    
    for item in modelSet:
      logging.info(item)
    
#    q = db.GqlQuery("SELECT * FROM ProductItem WHERE model = :model ORDER BY date", model = modelSet[0])
    q = db.GqlQuery("SELECT * FROM ProductItem ORDER BY date")
    
    logging.info("current model results:")
    
    for item in q:
      date = str(item.date.day) + '.' + str(item.date.month) + '.' + str(item.date.year)
      logging.info(item.model + "," + date + ", " + str(item.saleprice))
      logging.info(str(item.date))
    
    productItems = q.run()
    
    results = {'productItems':productItems, 'modelList':modelSet}
    # skus = {'modelList':modelSet}
    # self.response.headers['Content-Type'] = 'text/plain'
    # self.response.write('Testing\n')
    logging.info("index.html should be rendered")
    
    path = os.path.join(os.path.dirname(__file__), 'html/index.html')
    self.response.out.write(template.render(path,results))
 
app = webapp2.WSGIApplication([('/.*', MainHandler)],
                              debug=True)