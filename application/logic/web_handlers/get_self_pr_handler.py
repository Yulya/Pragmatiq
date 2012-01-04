from google.appengine.ext.webapp import RequestHandler, template
from logic.models import PerformanceReview


class GetSelfPR(RequestHandler):

    def get(self):

        user = self.request.environ['current_user']

        pr = PerformanceReview.all().filter('employee', user).\
                                     order('-date').get()
        try:
            form = pr.employee_form
        except AttributeError:
            pr = None

        template_values = {'pr': pr,
                            'user': user
                        }

        path = 'templates/api.employee.html'
        self.response.out.write(template.render(path, template_values))
