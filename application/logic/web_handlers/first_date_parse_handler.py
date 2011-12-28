import logging
import datetime
from logic.models import User
import xlrd
from google.appengine.ext.webapp import blobstore_handlers


class FirstDateParseHandler(blobstore_handlers.BlobstoreUploadHandler):

    def post(self):

        upload_files = self.get_uploads('file')
        blob_info = upload_files[0]

        file = blob_info.open().read()

        wb = xlrd.open_workbook(file_contents=file)
        wb.sheet_names()
        sh = wb.sheet_by_index(0)

        cols_dict = {'name': 0,
                     'date': 1}


        for rownum in range(sh.nrows)[6:]:

            date = sh.cell_value(rownum, cols_dict['date']) - 2

            first_date = datetime.date(year=1900, month=1, day=1)

            date = first_date + datetime.timedelta(days=date)

            name = sh.cell_value(rownum, cols_dict['name']).replace('  ', ' ')

            last_name, first_name = name.split(' ')[:2]
            user = User.all().filter('last_name',
                                        last_name).filter('first_name',
                                                              first_name).get()
            if user:
                user.first_date = date
                user.put()
            else:
                logging.debug('last name: "%s" first_name: "%s" string: %s' %(last_name, first_name, name))

        self.redirect('/users')
