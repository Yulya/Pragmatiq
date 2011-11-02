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
from logic.web_handlers.check_form_content_handler import CheckFormContent
from logic.web_handlers.get_eaf_handler import GetEmployeeForm
from logic.web_handlers.get_maf_handler import GetManagerForm
from logic.web_handlers.handlers import MainHandler, CreateUser,\
	Authentication, UpdateData,\
    AddData, CreateRoles, GetPrs, UserTable, CreatePR,\
    GetSelfPR, GetManagers, CheckDate, HR,\
    UploadHandler, ServeHandler, UrlHandler, GetAllEmployees, UpdatePR, \
    ManagerFormSubmit, EmployeeFormSubmit, RegisterPerformanceReview,\
    ManagerFormApprove, GetDetailedReport, GetSummaryReport, UpdateEvent, \
    GetSettings, AutomaticPerformanceReview
from logic.postdeploy import PostDeploy
from logic.web_handlers.hr_maf_handler import HRManagerForm
from logic.web_handlers.add_maf_handler import AddForm

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
                                          ('/pr/get/self', GetSelfPR),
                                          ('/pr/get/manager/(.*)', GetManagerForm),
                                          ('/pr/get/employee/(.*)', GetEmployeeForm),
                                          ('/pr/add/(.*)/(.*)', AddForm),
                                          ('/pr/data/add', AddData),
                                          ('/pr/manager/submit/(.*)', ManagerFormSubmit),
                                          ('/pr/manager/approve/(.*)', ManagerFormApprove),
                                          ('/pr/employee/submit/(.*)', EmployeeFormSubmit),
                                          ('/hr/report/detailed', GetDetailedReport),
                                          ('/hr/report/summary', GetSummaryReport),
                                          ('/pr/register', RegisterPerformanceReview),
                                          ('/pr/data/update/(.*)', UpdateData),
                                          ('/hr/get/(.*)', HRManagerForm),
                                          ('/pr/manager/check/(.*)', CheckFormContent),
                                          ('/manager',GetPrs),
                                          ('/hr', GetAllEmployees),
                                          ('/new_period', HR),
                                          ('/upload', UploadHandler),
                                          ('/serve/([^/]+)?', ServeHandler)

                                         ],
                                         debug=True)

    application = Authentication(application)
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()
