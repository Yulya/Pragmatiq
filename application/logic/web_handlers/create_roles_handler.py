from google.appengine.ext.webapp import RequestHandler
from logic.models import Role

class CreateRoles(RequestHandler):

    def post(self):

        try:
            role = Role(value='manager')
            role.put()
            role = Role(value='employee')
            role.put()
            role = Role(value='hr')
            role.put()
        except:
            self.response.out.write('error')
            return