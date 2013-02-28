import os
import commands
import random

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.ext.webapp import template
from xml.dom.minidom import *
from datetime import *

from Datastores import *


class expiryDateInside(webapp.RequestHandler): 
  def post(self):
      url = self.request.get('url')
      url_linktext = self.request.get('url_linktext')
      loggedInUser = self.request.get('loggedInUser')
      categorySelected = self.request.get('categ')
      expDate = self.request.get('date')
      if expDate == None or expDate == "" :
          template_values = {
             'expiryEmpty' : "Yes",
             'loggedInUser' : loggedInUser,
             'categorySelected':categorySelected,
             'url' : url,
             'url_linktext': url_linktext
          }
          path = os.path.join(os.path.dirname(__file__),'webpages/expiryDate.html')
          self.response.out.write(template.render(path, template_values))

      else:    
          today = date.today()
          expYear=expDate.split('/',2)[2]
          expMonth=expDate.split('/',1)[0]
          expDay=expDate.split('/',2)[1]
          expDate1=date(int(expYear),int(expMonth),int(expDay))

          if expDate1 < today:
              template_values = {
                 'invalidExpiry' : "Yes",
                 'loggedInUser' : loggedInUser,
                 'categorySelected':categorySelected,
                 'url' : url,
                 'url_linktext': url_linktext
              }
              path = os.path.join(os.path.dirname(__file__),'webpages/expiryDate.html')
              self.response.out.write(template.render(path, template_values))
          else:
              result = db.GqlQuery("SELECT * FROM Categories where owner = :1 AND category = :2", loggedInUser,categorySelected)

              for r in result:
                  if r.category == categorySelected:
                      r.expDate =expDate1
                      r.put()
              
              template_values = {
                 'expiryDone' : "Yes",
                 'expDate' : expDate1,
                 'loggedInUser' : loggedInUser,
                 'categorySelected':categorySelected,
                 'url' : url,
                 'url_linktext': url_linktext
              }
              path = os.path.join(os.path.dirname(__file__),'webpages/editCategories.html')
              self.response.out.write(template.render(path, template_values))
