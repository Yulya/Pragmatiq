from google.appengine.ext.webapp import RequestHandler, template
from logic.models import PerformanceReviewPeriod, Dept, PerformanceReview, CommentToForm

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

        archived_periods = PerformanceReviewPeriod.gql("WHERE is_open = false ORDER BY start_date DESC").fetch(1000)

        def manager_has_pr_in_period(period):
            for pr in period.performance_reviews:
                if pr.manager.email == manager.email:
                    return True

        archived_periods = filter(manager_has_pr_in_period, archived_periods)

        comments = CommentToForm.gql("WHERE manager = :manager", manager = manager).fetch(1000)
        comments = filter(lambda x: x.pr.period.is_open, comments)

        template_values = {"departments": user_departments,
                           "archived_periods": archived_periods,
                           "comments": comments
                           }

        path = 'templates/api.manager.home.html'
        self.response.out.write(template.render(path, template_values))
