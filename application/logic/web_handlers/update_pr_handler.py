import datetime
from google.appengine.ext.db import Model
from google.appengine.ext.webapp import RequestHandler


class UpdatePR(RequestHandler):

    def post(self):

        key = self.request.get('key')
        pr = Model.get(key)
        start_str = self.request.get('start')
        finish_str = self.request.get('finish')
        first_date = self.request.get('first_date')

        if start_str:
            try:
                start = datetime.datetime.strptime(start_str,
                                                   '%Y-%m-%d').date()
                pr.start_date = start
            except ValueError:
                self.response.out.write('incorrect date')
                self.error(401)
                return

        if finish_str:
            try:
                finish = datetime.datetime.strptime(finish_str,
                                                    '%Y-%m-%d').date()
                pr.finish_date = finish
            except ValueError:
                self.response.out.write('incorrect date')
                self.error(401)
                return

        if first_date:
            try:
                first_effective_date = datetime.datetime.strptime(first_date,
                                                    '%Y-%m-%d').date()
                pr.first_effective_date = first_effective_date
            except ValueError:
                self.response.out.write('incorrect date')
                self.error(401)
                return

        pr.put()
