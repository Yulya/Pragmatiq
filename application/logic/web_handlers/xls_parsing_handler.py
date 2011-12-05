import logging
import re
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import RequestHandler
from logic.models import User, Dept, ContactXlsFile, Role
import xlrd


class XlsParseHandler(RequestHandler):

    def get(self):

        file_key = ContactXlsFile.all().get().file_key
        blob_info = blobstore.BlobInfo.get(file_key)
        file = blob_info.open().read()
        
        wb = xlrd.open_workbook(file_contents=file)
        wb.sheet_names()
        sh = wb.sheet_by_index(0)

        cols_dict = {'first_name': 1,
                     'last_name': 0,
                     'dept': 2,
                     'position': 3,
                     'email': 4,
                     'manager': 12
                    }
        manager_dict = {}

        reg = "^\s+|\n|\r|\s+$"


        employee_role = Role.all().filter('value', 'employee').get().key()


        for rownum in range(sh.nrows)[6:]:
            email = sh.cell_value(rownum,cols_dict['email']).strip()
            user = User.all().filter('email', email).get()
            if user is None:
                user = User(email=email)
                user.put()

            if not user.role:
                user.role.append(employee_role)

            string_fields = ['first_name',
                             'last_name',
                             'position',
                             ]

            for field in string_fields:
                value = re.sub(reg, '', sh.cell_value(rownum,cols_dict[field]))
                setattr(user, field, value)

            department_str = re.sub(reg,
                                    '',
                                    sh.cell_value(rownum,cols_dict['dept']))
            department = Dept.all().filter('name', department_str).get()
            if department is None:
                department = Dept(name=department_str)
                department.put()
            user.dept = department

            user.put()

            manager_str = re.sub(reg,
                                 '',
                                 sh.cell_value(rownum,cols_dict['manager']))
            manager_dict[user.key()] = manager_str

        manager_role = Role.all().filter('value', 'manager').get().key()

        for user_key in manager_dict:

            manager_str = manager_dict[user_key].replace('  ',' ')

            if manager_str:
                last_name, first_name = manager_str.split(' ')[:2]
                manager = User.all().filter('last_name',
                                            last_name).filter('first_name',
                                                              first_name).get()
            else:
                manager = None

            if manager is not None:
                if manager_role not in manager.role:
                    manager.role.append(manager_role)
                    manager.put()

            user = User.get(user_key)
            user.manager = manager
            user.put()

        self.redirect('/users')


