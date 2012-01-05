from google.appengine.api.datastore_errors import BadKeyError
from google.appengine.ext.db import Model
from google.appengine.ext.webapp import RequestHandler


class UpdateData(RequestHandler):

    def post(self, object_key):

        try:
            obj = Model.get(object_key)
        except BadKeyError:
            self.error(405)
            return

        if self.request.get('value') == '' and not self.request.get('result'):
            obj.delete()
            return

        if self.request.get('value'):
            obj.value = self.request.get('value')

        try:
            obj.manager = self.request.environ['current_user']
        except AttributeError:
            pass

        if self.request.get('result'):
            obj.result = int(self.request.get('result'))

        obj.put()

        if obj.value is None:
            obj.delete()
