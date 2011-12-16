import logging
from google.appengine.api.datastore_errors import BadKeyError
from google.appengine.ext.webapp import RequestHandler
from logic.models import User, WorkProject


class AttachEmployeeToProject(RequestHandler):

    def post(self):

        project_key = self.request.get('project_key')
        logging.debug(project_key)
        users = self.request.get('employees')
        try:
            project = WorkProject.get(project_key)
        except BadKeyError:
            self.response.out.write('error')
            return

        user_emails = users.split(',')

        for email in user_emails:
            if email:
                user = User.all().filter('email', email).get()
                if user:
                    project.employees.append(user.key())
                    project.put()

        self.response.out.write('ok')
