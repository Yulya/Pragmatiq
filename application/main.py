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
from logic.authentication_middleware import Authentication
from logic.web_handlers.add_data_handler import AddData
from logic.web_handlers.add_form_handler import AddEmployeeForm
from logic.web_handlers.add_manager_form_handler import AddManagerForm
from logic.web_handlers.autocomplete_users import GetJSONUsers
from logic.web_handlers.automatic_creation_pr_handler import AutomaticPerformanceReview
from logic.web_handlers.check_form_content_handler import CheckFormContent
from logic.web_handlers.check_pr_date import CheckDate
from logic.web_handlers.close_period import ClosePeriod
from logic.web_handlers.create_pr_handler import CreatePR
from logic.web_handlers.create_roles_handler import CreateRoles
from logic.web_handlers.edit_user import EditUser
from logic.web_handlers.delete_comment import DeleteComment
from logic.web_handlers.delete_pr import DeletePR
from logic.web_handlers.detailed_report_handler import GetDetailedReport
from logic.web_handlers.employee_form_draft import EmployeeFormDraft
from logic.web_handlers.employee_form_submit_handler import EmployeeFormSubmit
from logic.web_handlers.employee_home import EmployeeHome
from logic.web_handlers.get_all_departments import HR
from logic.web_handlers.get_department_prs import GetDepartmentPrs
from logic.web_handlers.get_eaf_handler import GetEmployeeForm
from logic.web_handlers.get_maf_handler import GetManagerForm
from logic.postdeploy import PostDeploy
from logic.web_handlers.get_period_prs import GetPeriodPrs
from logic.web_handlers.hr_home import HRHome
from logic.web_handlers.hr_maf_handler import HRManagerForm
from logic.web_handlers.lock_form import LockFormHandler
from logic.web_handlers.main_handler import MainHandler
from logic.web_handlers.manager_comments import ManagerComments
from logic.web_handlers.manager_eaf_form import ManagerEmployeeForm
from logic.web_handlers.manager_form_approve_handler import ManagerFormApprove
from logic.web_handlers.manager_form_draft import ManagerFormDraft
from logic.web_handlers.manager_form_register import ManagerFormRegister
from logic.web_handlers.manager_form_submit_handler import ManagerFormSubmit
from logic.web_handlers.manager_home import ManagerHome
from logic.web_handlers.manager_settings import ManagerSettings
from logic.web_handlers.parse_xml_form import ParseXml
from logic.web_handlers.register_performance_review import RegisterPerformanceReview
from logic.web_handlers.reopen_period import ReopenPeriod
from logic.web_handlers.request_comment import RequestComment
from logic.web_handlers.save_comment import SaveComment
from logic.web_handlers.serve_handler import ServeHandler
from logic.web_handlers.summary_report_handler import GetSummaryReport
from logic.web_handlers.system_settings_handler import GetSettings
from logic.web_handlers.update_data_handler import UpdateData
from logic.web_handlers.update_event_handler import UpdateEvent
from logic.web_handlers.update_manager_settings import UpdateManagerSettings
from logic.web_handlers.update_pr_handler import UpdatePR
from logic.web_handlers.upload_file import UploadFile
from logic.web_handlers.upload_handler import UploadHandler
from logic.web_handlers.upload_xls_handler import UploadXlsHandler
from logic.web_handlers.upload_xml import UploadXml
from logic.web_handlers.url_handler import UrlHandler
from logic.web_handlers.user_data import UserData
from logic.web_handlers.user_table_handler import UserTable
from logic.web_handlers.xls_parsing_handler import XlsParseHandler
from logic.web_handlers.first_date_parse_handler import FirstDateParseHandler

def main():
    #run post deploy scripts

    PostDeploy().post_deploy_routines()

    logging.getLogger().setLevel(logging.DEBUG)
    application = webapp.WSGIApplication([('/', MainHandler),
                                          ('/edit_user', EditUser),
                                          ('/logout', UrlHandler),
                                          ('/users', UserTable),
                                          ('/create_role', CreateRoles),
                                          ('/edit_user/(.*)', UserData),
                                          ('/check', CheckDate),
                                          ('/pr/automatic', AutomaticPerformanceReview),
                                          ('/event/update', UpdateEvent),
                                          ('/hr/settings', GetSettings),
                                          ('/pr/create', CreatePR),
                                          ('/pr/update', UpdatePR),
                                          ('/employee', EmployeeHome),
                                          ('/lock_form/(.*)', LockFormHandler),
                                          ('/manager/home', ManagerHome),
                                          ('/manager/pr/get/manager/(.*)', GetManagerForm),
                                          ('/employee/pr/get/employee/(.*)', GetEmployeeForm),
                                          ('/manager/pr/get/employee/(.*)', ManagerEmployeeForm),
                                          ('/manager/pr/add/manager/(.*)', AddManagerForm),
                                          ('/employee/pr/add/employee/(.*)', AddEmployeeForm),
                                          ('/pr/data/add', AddData),
                                          ('/pr/manager/submit/(.*)', ManagerFormSubmit),
                                          ('/pr/manager/approve/(.*)', ManagerFormApprove),
                                          ('/pr/manager/draft/(.*)', ManagerFormDraft),
                                          ('/pr/manager/register/(.*)', ManagerFormRegister),
                                          ('/pr/employee/submit/(.*)', EmployeeFormSubmit),
                                          ('/pr/employee/draft/(.*)', EmployeeFormDraft),
                                          ('/hr/report/detailed/(.*)', GetDetailedReport),
                                          ('/hr/report/summary/(.*)', GetSummaryReport),
                                          ('/pr/register', RegisterPerformanceReview),
                                          ('/pr/delete', DeletePR),
                                          ('/pr/data/update/(.*)', UpdateData),
                                          ('/hr/get/manager/(.*)', HRManagerForm),
                                          ('/pr/manager/check/(.*)', CheckFormContent),
                                          ('/manager/settings', ManagerSettings),
                                          ('/manager/settings/update', UpdateManagerSettings),
                                          ('/manager/get/department/(.*)',GetDepartmentPrs),
                                          ('/manager/get/period/(.*)',GetPeriodPrs),
                                          ('/get_users', GetJSONUsers),
                                          ('/pr/period/close/(.*)', ClosePeriod),
                                          ('/pr/period/reopen/(.*)', ReopenPeriod),
                                          ('/pr/comment/request', RequestComment),
                                          ('/pr/comment/save/(.*)', SaveComment),
                                          ('/pr/comment/delete/(.*)', DeleteComment),
                                          ('/pr/manager/comments/(.*)', ManagerComments),
                                          ('/hr', HRHome),
                                          ('/hr/new_period', HR),
                                          ('/upload_xml', UploadXml),
                                          ('/upload_file', UploadFile),
                                          ('/parse_xml/(.*)/(.*)/(.*)', ParseXml),
#                                          ('/upload', UploadHandler),
                                          ('/upload_contacts', UploadXlsHandler),
                                          ('/upload_first_date', FirstDateParseHandler),
                                          ('/parse_xls', XlsParseHandler),
                                          ('/serve/([^/]+)?', ServeHandler)
                                         ],
                                         debug=True)

    application = Authentication(application)
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()
