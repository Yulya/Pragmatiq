from google.appengine.ext import blobstore
from google.appengine.ext.webapp import RequestHandler
from logic.models import ContactXlsFile, User, Dept
import xlrd
import os.path


class XlsParseHandler(RequestHandler):

    def get(self):

        wb = xlrd.open_workbook(os.path.dirname(__file__) + '/contacts.xls')
        wb.sheet_names()
        sh = wb.sheet_by_index(0)

        cols_dict = {'first_name': 1,
                     'last_name': 0,
                     'dept': 2,
                     'position': 3,
                     'email': 4,
#                     'skype': 5,
#                     'internal_number': 6,
#                     'phone_number': 7,
#                     'tariff_table': 8,
#                     'tariff_level': 9,
                     'login': 10,
#                     'city': 11,
                     'manager': 12
        }
        manager_dict = {}

        for rownum in range(sh.nrows)[6:]:

            login = sh.cell_value(rownum,cols_dict['login'])

            user = User().all().filter('login', login).get()

            if user is None:
                user = User()
            manager_str = ''

            for key in cols_dict.keys():

                value = sh.cell_value(rownum,cols_dict[key])
                if key == 'last_name' or key == 'first_name':
                    value = value.replace(' ','')
                if key == 'dept':
                    department = Dept().all().filter('name', value).get()
                    if department is None:
                        department = Dept(name=value)
                        department.put()
                    value = department
                if key == 'manager':
                    manager_str = value
                try:
                    user.__setattr__(key, value)
                except AttributeError:
                    pass
            user.put()
            manager_dict.update({user: manager_str})

        for user in manager_dict.keys():
            manager_str = manager_dict[user]
            if manager_str != '':
                last_name = manager_str.split(' ')[0]
                last_name = last_name.replace(' ','')
                first_name = manager_str.split(' ')[1]
                manager = User.all().filter('last_name', last_name).get()
                if manager is None:
                    self.response.out.write('@'+ last_name+'@\n')
            else:
                manager = None
            user.manager = manager
            user.put()


        self.redirect('/users')


