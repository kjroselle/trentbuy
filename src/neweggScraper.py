import webapp2
import logging
import re
import datetime
from data import ProductItem
from lxml.cssselect import CSSSelector
from lxml.html import parse
import urllib2

class MainPage(webapp2.RequestHandler):
  def get(self):
      self.response.headers['Content-Type'] = 'text/plain'
      self.response.write('Running Newegg crawler\n')
      
      # read in URLs to visit from external file
      fd = open('neweggUrl.txt')
      
      urlList = []
      # urlList = [line.strip() for line in fd]
      for line in fd:
        # if line isn't a comment or blank (doesn't begin with '#')
        line = line.strip();
        if(len(re.findall('^#',line)) == 0 and len(line) != 0):
          urlList.append(line)
      fd.close()
      
      # visit each url and extract product data
      for url in urlList:
        try:
          productPage = urllib2.urlopen(url)
        except urllib2.URLError as err:
          logging.info(err.reason)
        logging.info('visiting productPage:' + url)
        neweggId = re.findall("Item=(.*)", url)[0]
        
        # in order to get the price we must go to another URL using the Id
        # from the first URL
        priceUrl = "http://www.newegg.com/Product/MappingPrice.aspx?Item=" + neweggId 
        try:
          pricePage = urllib2.urlopen(priceUrl)
        except urllib2.URLError as err:
          logging.info(err.reason)
        logging.info('visiting pricePage: '+ priceUrl)
#        self.response.write(page.read())
#        self.response.write(productPage.read())
#        logging.info(page.read())

        # the model number element is a little buried
        productDoc = parse(productPage).getroot()
        idTarget = productDoc.cssselect('#Specs')
        modelNum = idTarget[0].getchildren()[0].getchildren()[3].getchildren()[1].text.strip()

        doc = parse(pricePage).getroot()
#        target = doc.cssselect('.price-current ')
#        target = doc.cssselect('#singleFinalPrice')
        target = doc.cssselect('.final')
        saleprice = target[0].text_content().strip()
#        tp = target[0].getchildren()[0].text_content()

        saleprice = re.findall("[+-]? *(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?", saleprice)
        saleprice = float(saleprice[0])

        now = datetime.date.today()
        
        logging.info("sku: ")
        logging.info(neweggId)
        
        logging.info("model: ")
        logging.info(modelNum)

        logging.info("saleprice: ")
        logging.info(saleprice)
        
        ProductItem(sku=neweggId, saleprice=saleprice, model=modelNum, date=now).put()
          
        self.response.write(modelNum + '\n')

      self.response.write('Finished Newegg crawler')
      
app = webapp2.WSGIApplication([('/newegg/', MainPage)],
        debug=True)