import datetime
from google.appengine.ext.db import Model
from google.appengine.ext.webapp import RequestHandler
from logic.models import Role

class UpdatePR(RequestHandler):

    def post(self):

        user = self.request.environ['current_user']

        role_key = Role.gql("WHERE value = :hr", hr='hr').get().key()

        if role_key not in user.role:
            self.error(403)
            return

        key = self.request.get('key')
        pr = Model.get(key)
        start_str = self.request.get('start')
        finish_str = self.request.get('finish')

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

        pr.put()