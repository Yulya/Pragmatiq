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
import datetime
from django.utils import simplejson as json

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext import db
from google.appengine.ext.webapp import RequestHandler


class MainHandler(webapp.RequestHandler):
    def get(self):
        self.response.out.write('Hello world!')

class Employee(db.Model):
    first_name = db.StringProperty()
    last_name = db.StringProperty()
    e_mail = db.StringProperty()
    salary = db.IntegerProperty()
    first_date = db.DateProperty()

class CreateEmployee(RequestHandler):
    def post(self):
        data = json.loads(self.request.body)

        employee = Employee(
            first_name=data['first_name'],
            last_name=data['last_name'],
            e_mail = data['e_mail'],
            salary = data['salary'],
            first_date = datetime.datetime.strptime(data['first_data'], '%D-%M-%Y'))

        employee.put()
        
        


def main():
    application = webapp.WSGIApplication([
            ('/', MainHandler),
            ('/createemployee',CreateEmployee)
            ],
        debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
