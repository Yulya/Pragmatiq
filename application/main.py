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
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from logic.handlers import MainHandler, CreateUser, CreateEmployee, Authentication, AddAssessmentForm, ShowAssessmentForm


def main():
    logging.getLogger().setLevel(logging.DEBUG)
    #url structure
    #/user/add
    #/employee/add
    #/assessment_form/add
    #/assessment_form/get
    #/assessment_form/goals/get
    #/assessment_form/goals/add
    #/assessment_form/goals/update
	#/assessment_form/challengers/get
    #/assessment_form/challengers/add
    #/assessment_form/challengers/update
    application = webapp.WSGIApplication([('/', MainHandler),
                                          ('/add_usr', CreateUser),
                                          ('/add_emp', CreateEmployee),
                                          ('/add_info', AddAssessmentForm),
                                          ('/as_form', ShowAssessmentForm)],
                                         debug=True)

    application = Authentication(application)
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()
