import webapp2
import logging
import re
import datetime
from data import AmmoPriceItem
from lxml.cssselect import CSSSelector
from lxml.html import parse
import urllib2

class MainPage(webapp2.RequestHandler):
  def get(self):
      self.response.headers['Content-Type'] = 'text/plain'
      self.response.write('Running Target Sports USA crawler\n')
      
      # read in URLs to visit from external file
      fd = open('tsusaUrl.txt')
      
      urlList = []
      # urlList = [line.strip() for line in fd]
      for line in fd:
        # if line isn't a comment or blank (doesn't begin with '#')
        line = line.strip();
        if(len(re.findall('^#',line)) == 0 and len(line) != 0):
          urlList.append(line)
      fd.close()
      
      for url in urlList:
        page = urllib2.urlopen(url)
        logging.info('visiting:'+url)
        # self.response.write(page.read())
        
        doc = parse(page).getroot()
        target = doc.cssselect('.RegularPrice')
        for item in target:
          
          name = (item.getparent().getparent().getparent().getparent().getchildren()[1].getchildren()[0].getchildren()[0].text).strip()
          
          stock = (item.getparent().getparent().getparent().getparent().getchildren()[1].getchildren()[0].getchildren()[0].getchildren()[0].getchildren()[0].text).strip()
          
          sku = re.split(":", (item.getparent().getparent().getparent().getparent().getchildren()[2].getchildren()[0].getchildren()[0].text).strip())[1]
          
          price = float(re.findall("[+-]? *(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?", item.text)[0])
          
          saleprice = float(re.findall("[+-]? *(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?", item.getparent().getchildren()[2].text)[0])
          
          now = datetime.datetime.now()
          date = str(now.month) + '.' + str(now.day) + '.' + str(now.year)
          
          # alpha find amount
          amount = int(re.findall("of ([0-9]+)",name)[0])
          
          logging.info("name: ")
          logging.info(name)
          
          logging.info("amount: ")
          logging.info(amount)
          
          logging.info("stock: ")
          logging.info(stock)
          
          logging.info("sku: ")
          logging.info(sku)
          
          logging.info("price: ")
          logging.info(price)
          
          logging.info("saleprice: ")
          logging.info(saleprice)
          
          AmmoPriceItem(name=name, stock=stock, sku=sku, regprice=price, saleprice=saleprice, date=now, amount=amount).put()
          
          self.response.write(name + '\n')
          
      self.response.write('Finished Target Sports USA crawler')
      
app = webapp2.WSGIApplication([('/tsusa/', MainPage)],
        debug=True)