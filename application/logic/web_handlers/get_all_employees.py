from google.appengine.ext.webapp import RequestHandler, template
from logic.models import PerformanceReviewPeriod

class GetAllEmployees(RequestHandler):

    def get(self):

        periods = PerformanceReviewPeriod.all().fetch(1000)
        template_values = {'periods': periods}

        for period in periods:
            period.register = 'disabled'
            period.pr = []
            for pr in period.performance_reviews:
                pr.register = 'disabled'
                if pr.manager_form:
                    if pr.manager_form.status == 'submitted':
                        period.register = ''
                        pr.register = ''
                period.pr.append(pr)

        path = 'templates/hr_table.html'
        self.response.out.write(template.render(path, template_values))