import logging
import urllib
from google.appengine.ext.webapp import RequestHandler, template
from logic.models import PerformanceReview, Dept, WorkProject, User, PerformanceReviewPeriod


class GetProjectPrs(RequestHandler):

    #selects all PR objects for current user's subs and returns them
    def get(self, name):

        user = self.request.environ['current_user']
        name = urllib.unquote(name).decode('utf-8')

        if name == 'all':
            projects = WorkProject.all().filter('manager', user).fetch(1000)
        else:
            projects = WorkProject.all().filter('name', name).fetch(1000)
        logging.debug(projects)
        for project in projects:
            project.prs = []
            for employee_key in project.employees:
                employee = User.get(employee_key)
                pr = employee.self_pr.order('-date').get()
                if pr:
                    project.prs.append(pr)
            logging.debug(project.prs)
        template_values = {'name': name,
                           'projects': projects,
                           'current_user': user.email}

        path = 'templates/api.manager.projects.html'
        self.response.out.write(template.render(path, template_values))
