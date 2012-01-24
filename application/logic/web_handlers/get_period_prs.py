import logging
import urllib
from google.appengine.ext.webapp import RequestHandler, template
from logic.models import PerformanceReview, Dept, WorkProject, User, PerformanceReviewPeriod


class GetPeriodPrs(RequestHandler):

    #selects all PR objects for current user's subs and returns them
    def get(self, name):

        user = self.request.environ['current_user']
        name = urllib.unquote(name).decode('utf-8')

        prs = PerformanceReview.all().filter('manager',
                                             user).order("-date").fetch(1000)

        def get_sub_prs(manager, prs):

            current_manager_prs = PerformanceReview.all().filter('manager',
                                             manager).order("-date").fetch(1000)

            prs.extend(current_manager_prs)

            for manager in manager.subs:
                get_sub_prs(manager, prs)


            return prs

        if user.edit_sub_reviews:
            prs = []
            get_sub_prs(user, prs)

        periods = PerformanceReviewPeriod.all().filter('description', name).fetch(1000)
        for period in periods:
            period.prs = filter(lambda x: x.period.key() == period.key(), prs)

        template_values = {'name': name,
                           'periods': periods,
                           'current_user': user.email}

        path = 'templates/api.manager.periods.html'
        self.response.out.write(template.render(path, template_values))
