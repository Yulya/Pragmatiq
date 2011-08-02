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
import os
from django.utils import simplejson as json
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import RequestHandler
from logic.emp import Employee


class MainHandler(webapp.RequestHandler):
    def get(self):
        emp_query = Employee.all()
        employees = emp_query.fetch(10)
        template_values = {'employees': employees}
        
        path = os.path.join(os.path.dirname(__file__), 'templates/emp.html')
        self.response.out.write(template.render(path, template_values))
            


class CreateEmployee(RequestHandler):
    def post(self):
        errors = []
        data = json.loads(self.request.body)
        try:
            employee = Employee(first_name=data['first_name'],
                                 last_name=data['last_name'],
                                 e_mail = data['e_mail'],
                                 salary = int(data['salary']),
                                 first_date = datetime.datetime.strptime(data['first_date'], '%d-%m-%Y').date())
            employee.put()

        except:
            errors.append ('uncorrect data')
        
        


def main():
    application = webapp.WSGIApplication([
            ('/', MainHandler),
            ('/add_emp',CreateEmployee)
            ],
        debug=True)
    util.run_wsgi_app(application)
    


if __name__ == '__main__':
    main()
