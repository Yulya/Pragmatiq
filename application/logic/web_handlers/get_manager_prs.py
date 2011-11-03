from google.appengine.ext.webapp import RequestHandler, template
from logic.models import PerformanceReview

class GetPrs(RequestHandler):

    #selects all PR objects for current user's subs and returns them
    def get(self):

        user = self.request.environ['current_user']

        prs = PerformanceReview.all().filter('manager',
                                             user).order("-date").fetch(1000)

        #todo: find another solution
        periods = dict()
        for pr in prs:
            periods[pr.period.key()] = pr.period

        template_values = {
                           'periods': periods.values(),
                           'current_user': user.email}

        path = 'templates/api.manager.html'
        self.response.out.write(template.render(path, template_values))