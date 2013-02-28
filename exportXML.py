import cgi
import os
import random

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.ext.webapp import template

from Datastores import *


class exportXML(webapp.RequestHandler): 
  def post(self):
      url = self.request.get('url')
      url_linktext = self.request.get('url_linktext')
      loggedInUser = self.request.get('loggedInUser')
      categoryAndOwner = self.request.get('categ')
      if categoryAndOwner == None or categoryAndOwner == "":
          allCategories = db.GqlQuery("SELECT * FROM Categories")
          template_values = {
            'allCategories': allCategories,
            'loggedInUser': loggedInUser,
            'noOptionSelected': "Yes",
            'option5Selected':"Yes",
            'url':url,
            'url_linktext':url_linktext
          }
          path = os.path.join(os.path.dirname(__file__), 'webpages/AllCategories.html')
          self.response.out.write(template.render(path, template_values))
      else:
          categorySelected = categoryAndOwner.split('|')[0]
          owner = categoryAndOwner.split('|')[1]
          items = db.GqlQuery("SELECT * FROM Items WHERE category = :1 AND owner = :2", categorySelected, owner)
          itemCount = items.count()
          if itemCount == 0:
              allCategories = db.GqlQuery("SELECT * FROM Categories")
              template_values = {
                'allCategories': allCategories,
                'loggedInUser': loggedInUser,
                'noItemsPresent': "Yes",
                'option5Selected':"Yes",
                'categorySelected': categorySelected,
                'owner': owner,
                'url':url,
                'url_linktext':url_linktext
              }
              path = os.path.join(os.path.dirname(__file__), 'webpages/AllCategories.html')
              self.response.out.write(template.render(path, template_values))
          else:
            items = db.GqlQuery("SELECT * FROM Items WHERE category = :1 and owner = :2",categorySelected, owner);
            self.response.headers['Content-Type'] = 'text/xml'
            file_name = categorySelected + ".xml"
            self.response.headers['Content-Disposition'] = "attachment; filename = "+str(file_name)+""
            textdata = "<CATEGORY>" + "\n" + "<NAME>" + categorySelected +"</NAME>" + "\n";
            self.response.out.write(textdata)
            for item in items:
                text = "<ITEM>"+ "\n" + "<NAME>" + item.item + "</NAME>" + "\n" + "</ITEM>" + "\n";
                self.response.out.write(text)
            self.response.out.write('</CATEGORY>')    
            
