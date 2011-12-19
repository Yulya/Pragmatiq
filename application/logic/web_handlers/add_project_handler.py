from google.appengine.ext.webapp import RequestHandler
from logic.models import WorkProject, User


class AddProjects(RequestHandler):

    def post(self):

        name = self.request.get('name')
        manager = self.request.get('manager')
        manager = User.all().filter('email', manager).get()
        project = WorkProject(name=name,
                              manager=manager,
                          employees = [])
        project.put()

        self.response.out.write('You have successfully created project "%s"'
                                % project.name)