import datetime
from google.appengine.ext.webapp import RequestHandler, template
from logic.models import PerformanceReviewPeriod

class GetAllEmployees(RequestHandler):

    def get(self):

        prs = PerformanceReviewPeriod.all().filter('finish_date >=',
                                             datetime.date.today()).fetch(1000)
        template_values = {'periods': prs}

        path = 'templates/hr_table.html'
        self.response.out.write(template.render(path, template_values))