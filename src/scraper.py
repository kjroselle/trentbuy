#!/usr/bin/env python
 
import webapp2
import logging
 
from datetime import datetime
from lxml.cssselect import CSSSelector
from lxml.html import parse
from urllib2 import urlopen
 
from data import Fixing

class MainHandler(webapp2.RequestHandler):
  def get(self):
    url = 'http://www.targetsportsusa.com/p-646-cci-blazer-9mm-luger-115-grain-full-metal-jacket-ammunition.aspx'
    page = urlopen(url)
    doc = parse(page).getroot()
    target = doc.cssselect('#todayRates li')
    list_item = '3m'
    surrounding_text = ['3m','(']
    for item in target:
      if list_item in item.text_content().strip():
        tmp = item.text_content().strip()
        eonia_3m = tmp[tmp.index(surrounding_text[0])+len(surrounding_text[0]):tmp.index(surrounding_text[1])].strip()    
 
    if eonia_3m is None:
      logging.info('BREAK: %s' % (url))
      
    # Fixing(timestamp=datetime.utcnow(),instrument="eonia_3m",bips=eonia_3m).put()
 
 
# logging.getLogger().setLevel(logging.INFO)
# app = webapp2.WSGIApplication([('/tasks/fixing', MainHandler)], debug=True)
 
if __name__ == '__main__':
  run_wsgi_app(app)
