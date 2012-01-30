import logging
from google.appengine.ext.webapp import RequestHandler, template
from logic.models import PerformanceReviewPeriod, Dept, PerformanceReview

class ManagerHome(RequestHandler):

    #show home page
    def get(self):
        manager = self.request.environ['current_user']

        user_departments_keys = []

        prs = PerformanceReview.all().filter('manager',
                                             manager)

        for pr in prs:
            if pr.period.is_open:
                if not pr.employee.dept.key() in user_departments_keys:
                    user_departments_keys.append(pr.employee.dept.key())

        user_departments = map(lambda x: Dept.get(x), user_departments_keys)

        archived_periods = PerformanceReviewPeriod.all().order("-finish_date").fetch(1000)

        def manager_has_pr_in_period(period):
            for pr in period.performance_reviews:
                if pr.manager.email == manager.email:
                    return True

        archived_periods = filter(manager_has_pr_in_period, archived_periods)

        template_values = {"departments": user_departments,
                           "archived_periods": archived_periods,
                           }

        path = 'templates/api.manager.home.html'
        self.response.out.write(template.render(path, template_values))
 