from google.appengine.ext.webapp import RequestHandler
from logic.models import WorkProject


class AddProjects(RequestHandler):

    def post(self):

        name = self.request.get('name')
        
        project = WorkProject(name=name,
                          employees = [])
        project.put()

        self.response.out.write('ok')