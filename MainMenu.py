import cgi
import os
import random

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.ext.webapp import template

from Datastores import *


class MainMenu(webapp.RequestHandler):
    def post(self):
        loggedInUser = self.request.get('loggedInUser')
        url = self.request.get('url')
        url_linktext = self.request.get('url_linktext')
        choice = self.request.get('choice')
        if choice == None or choice == "":
            template_values = {
                'url': url,
                'noOptionSelected':"Yes",
                'categoryEmpty' : "",
                'categoryAdded' : "",
                'categoryNotAdded' : "",
                'categoryName' : "",
                'user' :loggedInUser,
                'url_linktext': url_linktext
            }

            path = os.path.join(os.path.dirname(__file__), 'webpages/index1.html')
            self.response.out.write(template.render(path, template_values))
        else:
            if choice == "option1":    # Call the form createCategory
                userCategories = db.GqlQuery("SELECT * FROM Categories where owner = :1", loggedInUser)
                category=userCategories.get()
                if category != None:
                    template_values = {
                        'url':url,
                        'userCategories':userCategories,
                        'url_linktext':url_linktext,
                        'loggedInUser': loggedInUser
                    }

                    path = os.path.join(os.path.dirname(__file__),'webpages/createCategory.html')
                    self.response.out.write(template.render(path, template_values))
                else:
                    template_values = {
                        'url':url,
                        'userCategories':"",
                        'url_linktext':url_linktext,
                        'loggedInUser': loggedInUser
                    }

                    path = os.path.join(os.path.dirname(__file__),'webpages/createCategory.html')
                    self.response.out.write(template.render(path, template_values))
                
            if choice == "option2":    # Add items to a category
                userCategories = db.GqlQuery("SELECT * FROM Categories where owner = :1", loggedInUser)
                count=userCategories.count()
                if count == 0:  #no categories present
                    template_values = {
                        'url': url,
                        'noCategoriesPresent':"Yes",
                        'user' :loggedInUser,
                        'url_linktext': url_linktext
                    }

                    path = os.path.join(os.path.dirname(__file__), 'webpages/index1.html')
                    self.response.out.write(template.render(path, template_values))
                    
                else:    
                    template_values = {
                        'userCategories': userCategories,
                        'url':url,
                        'url_linktext':url_linktext,
                        'loggedInUser': loggedInUser
                    }

                    path = os.path.join(os.path.dirname(__file__), 'webpages/userCategories.html')
                    self.response.out.write(template.render(path, template_values))

            if choice == "option8": # Edit Category - rename,delete category or item
                userCategories = db.GqlQuery("SELECT * FROM Categories where owner = :1", loggedInUser)
                count=userCategories.count()
                if count == 0:  #no categories present
                    template_values = {
                        'url': url,
                        'noCategoriesPresent':"Yes",
                        'user' :loggedInUser,
                        'url_linktext': url_linktext
                    }

                    path = os.path.join(os.path.dirname(__file__), 'webpages/index1.html')
                    self.response.out.write(template.render(path, template_values))
                    
                else:
                    template_values = {
                        'url':url,
                        'url_linktext':url_linktext,
                        'loggedInUser': loggedInUser
                    }

                    path = os.path.join(os.path.dirname(__file__), 'webpages/editCategories.html')
                    self.response.out.write(template.render(path, template_values))
              
            if choice == "option3":    # Vote on a category
                allCategories = db.GqlQuery("SELECT * FROM Categories")
                count=allCategories.count()
                if count == 0:  #no categories present
                    template_values = {
                        'url': url,
                        'noCategoriesPresent':"Yes",
                        'user' :loggedInUser,
                        'url_linktext': url_linktext
                    }

                    path = os.path.join(os.path.dirname(__file__), 'webpages/index1.html')
                    self.response.out.write(template.render(path, template_values))
                    
                else:
                    template_values = {
                        'allCategories': allCategories,
                        'loggedInUser': loggedInUser,
                        'url':url,
                        'url_linktext':url_linktext
                    }

                    path = os.path.join(os.path.dirname(__file__), 'webpages/AllCategories.html')
                    self.response.out.write(template.render(path, template_values))
          
            if choice == "option4":    # View Results of a Category  
                allCategories = db.GqlQuery("SELECT * FROM Categories")
                count=allCategories.count()
                if count == 0:  #no categories present
                    template_values = {
                        'url': url,
                        'noCategoriesPresent':"Yes",
                        'user' :loggedInUser,
                        'url_linktext': url_linktext
                    }

                    path = os.path.join(os.path.dirname(__file__), 'webpages/index1.html')
                    self.response.out.write(template.render(path, template_values))
                    
                else:
                    template_values = {
                        'allCategories': allCategories,
                        'loggedInUser': loggedInUser,
                        'option4Selected':"Yes",
                        'url':url,
                        'url_linktext':url_linktext
                    }

                    path = os.path.join(os.path.dirname(__file__), 'webpages/AllCategories.html')
                    self.response.out.write(template.render(path, template_values))
                
            if choice == "option5":    # Export category to a XML
                allCategories = db.GqlQuery("SELECT * FROM Categories")
                count=allCategories.count()
                if count == 0:  #no categories present
                    template_values = {
                        'url': url,
                        'noCategoriesPresent':"Yes",
                        'user' :loggedInUser,
                        'url_linktext': url_linktext
                    }

                    path = os.path.join(os.path.dirname(__file__), 'webpages/index1.html')
                    self.response.out.write(template.render(path, template_values))
                    
                else:
                    template_values = {
                        'allCategories': allCategories,
                        'loggedInUser': loggedInUser,
                        'option5Selected':"Yes",
                        'url':url,
                        'url_linktext':url_linktext
                    }

                    path = os.path.join(os.path.dirname(__file__), 'webpages/AllCategories.html')
                    self.response.out.write(template.render(path, template_values))
                
            if choice == "option7":    # Import category into a XML
                template_values = {
                    'url':url,
                    'url_linktext':url_linktext,
                    'loggedInUser': loggedInUser
                }

                path = os.path.join(os.path.dirname(__file__),'webpages/importXML.html')
                self.response.out.write(template.render(path, template_values))

            if choice == "option9":    # The search feature
                template_values = {
                    'url':url,
                    'url_linktext':url_linktext,
                    'loggedInUser': loggedInUser
                }

                path = os.path.join(os.path.dirname(__file__),'webpages/search.html')
                self.response.out.write(template.render(path, template_values))    
                
            if choice == "option6":    # Create a new Caregory
               userCategories = db.GqlQuery("SELECT * FROM Categories where owner = :1", loggedInUser)
               flag="hi"
               categoryName = self.request.get('category')
               if categoryName == None or categoryName == "":
                   template_values = {
                     'categoryEmpty' : "Yes",
                     'noOptionSelected':"",
                     'categoryAdded' : "",
                     'categoryNotAdded' : "",
                     'userCategories':userCategories,
                     'categoryName' : categoryName,
                     'loggedInUser' : loggedInUser,
                     'url' : url,
                     'url_linktext': url_linktext
                   }
                   path = os.path.join(os.path.dirname(__file__),'webpages/createCategory.html')
                   self.response.out.write(template.render(path, template_values))
               else:
                   for category in userCategories:
                       if category.category == categoryName:
                           flag="bye"
                   if flag == "bye":
                       template_values = {
                         'categoryEmpty' : "",
                         'noOptionSelected':"",
                         'categoryAdded' : "",
                         'userCategories':userCategories,
                         'categoryNotAdded' : "Yes",
                         'categoryName' : categoryName,
                         'loggedInUser' : loggedInUser,
                         'url' : url,
                         'url_linktext': url_linktext
                       }
                       path = os.path.join(os.path.dirname(__file__),'webpages/createCategory.html')
                       self.response.out.write(template.render(path, template_values))

                   else:    
                       newCategory = Categories()
                       self.response.headers['Content-Type'] = 'text/html'
                       url = users.create_logout_url(self.request.uri)
                       url_linktext = 'Logout'
                       newCategory.owner = loggedInUser
                       newCategory.category = categoryName
                       newCategory.put()
                       template_values = {
                         'categoryEmpty' : "",
                         'noOptionSelected':"",
                         'userCategories':userCategories,
                         'categoryAdded' : "Yes",
                         'categoryNotAdded' : "",
                         'categoryName' : categoryName,
                         'loggedInUser' : loggedInUser,
                         'url' : url,
                         'url_linktext': url_linktext
                       }
                       path = os.path.join(os.path.dirname(__file__),'webpages/createCategory.html')
                       self.response.out.write(template.render(path, template_values))


 
