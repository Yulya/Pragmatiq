from google.appengine.ext.webapp import RequestHandler, template
from logic.models import PerformanceReview


class GetSelfPR(RequestHandler):

    def get(self):

        user = self.request.environ['current_user']

        prs = PerformanceReview.all().filter('employee', user).order('-date')
        prs = prs.fetch(1000)

        current_pr = None

        if prs:
            if prs[0].is_open:
                current_pr = prs[0]
                prs.remove(prs[0])
#
#        if current_pr:
#            try:
#                form = pr.employee_form
#            except AttributeError:
#                pr = None

        template_values = {'current_pr': current_pr,
                           'prs': prs,
                           'user': user
                        }

        path = 'templates/api.employee.html'
        self.response.out.write(template.render(path, template_values))
