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
	Authentication, AddPrForm, GetPrForm, UpdateData, AddData, CreateRoles, GetPrs, GetSelfPr, UserTable


def main():
    logging.getLogger().setLevel(logging.DEBUG)
    application = webapp.WSGIApplication([('/', MainHandler),
                                          ('/add_emp', CreateUser),
                                          ('/users', UserTable),
                                        
                                          ('/pr/add/(.*)', AddPrForm),
                                          ('/pr/data/add', AddData),
                                          ('/pr/data/update/(.*)', UpdateData),
                                          ('/pr/self',GetSelfPr),
                                          ('/pr/(.*)', GetPrForm),
                                          ('/manager',GetPrs),
                                          ('/pr/self',GetSelfPr),
                                          ('/create_role', CreateRoles)
                                         ],
                                         debug=True)

    application = Authentication(application)
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()
