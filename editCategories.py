import cgi
import os
import random

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.ext.webapp import template

from Datastores import *


class editCategories(webapp.RequestHandler):
    def post(self):
        loggedInUser = self.request.get('loggedInUser')
        url = self.request.get('url')
        url_linktext = self.request.get('url_linktext')
        choice = self.request.get('choice')
        if choice == None or choice == "":
            template_values = {
                'url': url,
                'noOptionSelected':"Yes",
                'loggedInUser' :loggedInUser,
                'url_linktext': url_linktext
            }

            path = os.path.join(os.path.dirname(__file__), 'webpages/editCategories.html')
            self.response.out.write(template.render(path, template_values))
        else:
            if choice == "option1":    # rename the category
                userCategories = db.GqlQuery("SELECT * FROM Categories where owner = :1", loggedInUser)
                template_values = {
                    'userCategories': userCategories,
                    'renameCategory':"Yes",
                    'url':url,
                    'url_linktext':url_linktext,
                    'loggedInUser': loggedInUser
                }

                path = os.path.join(os.path.dirname(__file__), 'webpages/userCategories.html')
                self.response.out.write(template.render(path, template_values))
            if choice == "option2":    # delete the category
                userCategories = db.GqlQuery("SELECT * FROM Categories where owner = :1", loggedInUser)
                template_values = {
                    'userCategories': userCategories,
                    'deleteCategory':"Yes",
                    'url':url,
                    'url_linktext':url_linktext,
                    'loggedInUser': loggedInUser
                }

                path = os.path.join(os.path.dirname(__file__), 'webpages/userCategories.html')
                self.response.out.write(template.render(path, template_values))

            if choice == "option3":    # delete item from the category
                userCategories = db.GqlQuery("SELECT * FROM Categories where owner = :1", loggedInUser)
                template_values = {
                    'userCategories': userCategories,
                    'deleteItem':"Yes",
                    'url':url,
                    'url_linktext':url_linktext,
                    'loggedInUser': loggedInUser
                }

                path = os.path.join(os.path.dirname(__file__), 'webpages/userCategories.html')
                self.response.out.write(template.render(path, template_values)) 
                
            if choice == "option5":    # create a expiration date
                userCategories = db.GqlQuery("SELECT * FROM Categories where owner = :1", loggedInUser)
                template_values = {
                    'userCategories': userCategories,
                    'expiryDate':"Yes",
                    'url':url,
                    'url_linktext':url_linktext,
                    'loggedInUser': loggedInUser
                }

                path = os.path.join(os.path.dirname(__file__), 'webpages/userCategories.html')
                self.response.out.write(template.render(path, template_values))
                
            if choice == "option4":    # rename item in the category
                userCategories = db.GqlQuery("SELECT * FROM Categories where owner = :1", loggedInUser)
                template_values = {
                    'userCategories': userCategories,
                    'renameItem':"Yes",
                    'url':url,
                    'url_linktext':url_linktext,
                    'loggedInUser': loggedInUser
                }

                path = os.path.join(os.path.dirname(__file__), 'webpages/userCategories.html')
                self.response.out.write(template.render(path, template_values))
