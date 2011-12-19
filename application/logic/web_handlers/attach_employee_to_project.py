import logging
from google.appengine.api.datastore_errors import BadKeyError
from google.appengine.ext.webapp import RequestHandler
from logic.models import User, WorkProject


class AttachEmployeeToProject(RequestHandler):

    def post(self):

        project_key = self.request.get('project_key')
        users = self.request.get('employees')
        try:
            project = WorkProject.get(project_key)
        except BadKeyError:
            self.response.out.write('error')
            return

        user_emails = users.split(',')
        employees = map(lambda x: User.get(x).email, project.employees)
        attached_users = []
        existed_users = []

        for email in user_emails:
            if email:
                user = User.all().filter('email', email).get()
                if user:
                    logging.debug(user)
                    if user.email not in employees:
                        project.employees.append(user.key())
                        project.put()
                        attached_users.append(user.email)
                    else:
                        existed_users.append(user.email)
        if attached_users:
            attached_users = (', ').join(attached_users)
            self.response.out.write('You have attached to "%s" %s' % (project.name, attached_users))
        if existed_users:
            existed_users = (', ').join(existed_users)
            self.response.out.write('%s are already attached to "%s' % (existed_users, project.name))

