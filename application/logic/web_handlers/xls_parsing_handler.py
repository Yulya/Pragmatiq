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
                     'login': 10,
                     'manager': 12
                    }
        manager_dict = {}

        reg = "^\s+|\n|\r|\s+$"

        manager_role = Role.all().filter('value', 'manager').get().key()
        employee_role = Role.all().filter('value', 'employee').get().key()


        for rownum in range(sh.nrows)[6:]:

            login = sh.cell_value(rownum,cols_dict['login']).replace(' ','')
            user = User().all().filter('login', login).get()
            if user is None:
                user = User(login=login)
                user.put()

            if not len(user.role):
                user.role.append(employee_role)

            string_fields = ['first_name',
                             'last_name',
                             'position',
                             'email']

            for field in string_fields:
                value = re.sub(reg, '', sh.cell_value(rownum,cols_dict[field]))
                user.__setattr__(field, value)

            department_str = re.sub(reg,
                                    '',
                                    sh.cell_value(rownum,cols_dict['dept']))
            department = Dept().all().filter('name', department_str).get()
            if department is None:
                department = Dept(name=department_str)
                department.put()
            user.dept = department

            user.put()

            manager_str = re.sub(reg,
                                 '',
                                 sh.cell_value(rownum,cols_dict['manager']))
            manager_dict.update({user: manager_str})

        for user in manager_dict.keys():
            manager_str = manager_dict[user].replace('  ',' ')
            if manager_str != '':
                last_name = manager_str.split(' ')[0]
                first_name = manager_str.split(' ')[1]
                manager = User.all().filter('last_name',
                                            last_name).filter('first_name',
                                                              first_name).get()
            else:
                manager = None
            if manager is not None:
                if manager_role not in manager.role:
                    manager.role.append(manager_role)
                    manager.put()

            user.manager = manager
            user.put()

        self.redirect('/users')


