import logging
from google.appengine.ext.webapp import RequestHandler, template
from logic.models import WorkProject, User

class GetProjects(RequestHandler):

    def get(self):
        
        projects = WorkProject.all().fetch(1000)

        for project in projects:
            employee_list = map(lambda x: User.get(x), project.employees)
            project.employee_list = employee_list

        logging.debug(projects)

        path = 'templates/projects.html'

        template_values = {'projects': projects}

        self.response.out.write(template.render(path,
                                                template_values))
