import cgi
import os
import random

from xml.dom.minidom import Document
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.ext.webapp import template

from Datastores import *

class addItem(webapp.RequestHandler):  #To show added item and option to add more
  def post(self):
      categorySelected = self.request.get('category')
      loggedInUser = self.request.get('loggedInUser')
      url = self.request.get('url')
      url_linktext = self.request.get('url_linktext')
      itemName = self.request.get('itemName')
      userItems = db.GqlQuery("SELECT * FROM Items WHERE category = :1 AND owner = :2", 
                                 categorySelected, loggedInUser)
      if itemName == None or itemName == "":
          template_values = {
            'itemEmpty':"Yes",
            'itemAlreadyExists': "",
            'itemAdded':"",
            'userItems': userItems,
            'categorySelected': categorySelected,
            'url':url,
            'url_linktext':url_linktext,
            'loggedInUser': loggedInUser
          }

          path = os.path.join(os.path.dirname(__file__), 'webpages/userItemsPage.html')
          self.response.out.write(template.render(path, template_values))
      else:
          flag="hi"
          for item in userItems:
                if item.item == itemName:
                    flag="bye"
                    
          if flag == "bye":
              template_values = {
                'itemEmpty':"",
                'itemAlreadyExists': "Yes",
                'itemAdded':"",
                'userItems': userItems,
                'categorySelected': categorySelected,
                'url':url,
                'url_linktext':url_linktext,
                'loggedInUser': loggedInUser
              }

              path = os.path.join(os.path.dirname(__file__), 'webpages/userItemsPage.html')
              self.response.out.write(template.render(path, template_values))
          else:
              newItem = Items()
              newItem.category = categorySelected
              newItem.owner = self.request.get('loggedInUser')
              newItem.item = itemName
              newItem.put()
      
              template_values = {
                'itemEmpty':"",
                'itemAlreadyExists': "",
                'itemAdded':"Yes",
                'item':itemName,
                'userItems': userItems,
                'categorySelected': categorySelected,
                'url':url,
                'url_linktext':url_linktext,
                'loggedInUser': loggedInUser
              }

              path = os.path.join(os.path.dirname(__file__), 'webpages/userItemsPage.html')
              self.response.out.write(template.render(path, template_values))
