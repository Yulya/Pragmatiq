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
from logic.handlers import MainHandler, CreateUser,\
	Authentication, UpdateData,\
    AddData, CreateRoles, GetPrs, UserTable, CreatePR,\
    GetPreviousGoals, GetSelfPR, GetManagers, CheckDate, HR, Show,\
    UploadHandler, ServeHandler, UrlHandler, GetAllEmployees, UpdatePR, \
    GetManagerForm, GetEmployeeForm, AddManagerForm, AddEmployeeForm, \
    ManagerFormSubmit, EmployeeFormSubmit, RegisterPerformanceReview, ManagerFormApprove, GetDetailedReport, GetSummaryReport, UpdateEvent, GetSettings, AutomaticPerformanceReview
from logic.postdeploy import PostDeploy

def main():
    #run post deploy scripts
    PostDeploy().post_deploy_routines()

    logging.getLogger().setLevel(logging.DEBUG)
    application = webapp.WSGIApplication([('/', MainHandler),
                                          ('/add_emp', CreateUser),
                                          ('/logout', UrlHandler),
                                          ('/users', UserTable),
                                          ('/create_role', CreateRoles),
                                          ('/new_user', GetManagers),
                                          ('/check', CheckDate),
                                          ('/pr/automatic', AutomaticPerformanceReview),
                                          ('/event/update', UpdateEvent),
                                          ('/hr/settings', GetSettings),
                                          ('/pr/create', CreatePR),
                                          ('/pr/update', UpdatePR),
                                          ('/pr/prev_goals/(.*)',GetPreviousGoals),
                                          ('/pr/get/self', GetSelfPR),
                                          ('/pr/get/manager/(.*)', GetManagerForm),
                                          ('/pr/get/employee/(.*)', GetEmployeeForm),
                                          ('/pr/add/manager/(.*)', AddManagerForm),
                                          ('/pr/add/employee/(.*)', AddEmployeeForm),
                                          ('/pr/data/add', AddData),
                                          ('/pr/manager/submit/(.*)', ManagerFormSubmit),
                                          ('/pr/manager/approve/(.*)', ManagerFormApprove),
                                          ('/pr/employee/submit/(.*)', EmployeeFormSubmit),
                                          ('/hr/report/detailed', GetDetailedReport),
                                          ('/hr/report/summary', GetSummaryReport),
                                          ('/pr/register/(.*)', RegisterPerformanceReview),
                                          ('/pr/data/update/(.*)', UpdateData),
                                          ('/manager',GetPrs),
                                          ('/hr', GetAllEmployees),
                                          ('/new_period', HR),
                                          ('/upload', UploadHandler),
                                          ('/serve/([^/]+)?', ServeHandler),
                                          ('/show',Show)

                                         ],
                                         debug=True)

    application = Authentication(application)
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()
