import logging
from google.appengine.ext.webapp import RequestHandler, template
from logic.models import PerformanceReview, SharedForm, Dept

class GetPrs(RequestHandler):

    #selects all PR objects for current user's subs and returns them
    def get(self, dept):

        user = self.request.environ['current_user']
        
        logging.debug(dept)

        prs = PerformanceReview.all().filter('manager',
                                             user).order("-date").fetch(1000)

        if dept == 'all':

            departments = Dept.all().fetch(1000)

            for department in departments:
                department.prs = filter(lambda x: x.employee.dept.name == department.name, prs)
                logging.debug(department.prs)

        else:
            departments = Dept.all().filter('name', dept).fetch(1000)

            for department in departments:
                department.prs = filter(lambda x: x.employee.dept.name == department.name, prs)

        logging.debug(departments)

        shared_forms = SharedForm.all().filter('user', user).fetch(1000)

        template_values = {'dept': dept,
                           'depts': departments,
                           'current_user': user.email,
                           'shared_forms': shared_forms}

        path = 'templates/api.manager.html'
        self.response.out.write(template.render(path, template_values))