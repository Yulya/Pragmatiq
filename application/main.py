#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import logging
import base64
import datetime
import hashlib
import os
import random
import string
from django.utils import simplejson as json
from google.appengine.api import users
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import RequestHandler
from logic.logic import Employee, Usr

def make_password(password):
    salt = ''.join(random.choice(
        string.ascii_uppercase
        + string.ascii_lowercase
        + string.digits) for x in range(4))
    hash = hashlib.sha1(salt + password).hexdigest()
    return salt + '$' + hash

def check_password(str_pass,hash_pass):
    salt, hash = hash_pass.split('$')
    return hash == hashlib.sha1(salt + str_pass).hexdigest()


class BaseHandler(RequestHandler):
    

    def pre_get(self):
        user = users.get_current_user()
        if user is not None:
            return user

        basic_auth = self.request.headers.get('Authorization')
        if not basic_auth:
            self.error(401)
            return

        username, password = '', ''
        try:
            user_info = base64.decodestring(basic_auth[6:])
            username, password = user_info.split(':')
        except ValueError:
            self.error(400)
            return

        user_info = Usr.gql("WHERE username = :username",
                            username = username).get()

        if user_info is None:
            self.error(401)
            return


        if not check_password(password, user_info.password):
            self.error(401)
            return

        return user_info




class MainHandler(BaseHandler):


    def get(self):

        user = self.pre_get()
        
        if user is None:
            url = users.create_login_url(self.request.uri)
            self.redirect(url)

        else:
            try:
                username = user.username
            except AttributeError:
                username = user.email()
            
            emp_query = Employee.all()
            employees = emp_query.fetch(1000)
            template_values = {'employees': employees,
                               'user': username
                               }

            path = os.path.join(os.path.dirname(__file__), 'templates/emp.html')
            self.response.out.write(template.render(path, template_values))


class CreateEmployee(BaseHandler):


    def post(self):

        user = self.pre_get()

        if not user:
            self.response.set_status(401)
            return


        data = json.loads(self.request.body)
        try:
            employee = Employee(first_name=data['first_name'],
                                 last_name=data['last_name'],
                                 e_mail = data['e_mail'],
                                 salary = int(data['salary']),
                                 first_date = datetime.datetime.strptime(
                                     data['first_date'], '%d-%m-%Y').date())

            employee.put()
        except ValueError:
           self.response.set_status(400)



class CreateUser(RequestHandler):

    def post(self):
        data = json.loads(self.request.body)
        try:
            usr = Usr(username = data['username'],
                      password = make_password(data['password']))

            usr.put()

        except Exception:
            self.response.set_status(400)


def main():
    logging.getLogger().setLevel(logging.DEBUG)
    application = webapp.WSGIApplication(
                                         [('/', MainHandler),
                                          ('/add_usr',CreateUser),
                                          ('/add_emp',CreateEmployee)],
                                         debug=True)
    util.run_wsgi_app(application)
    


if __name__ == '__main__':
    main()
