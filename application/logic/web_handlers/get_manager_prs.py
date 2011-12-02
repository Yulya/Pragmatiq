from google.appengine.ext.webapp import RequestHandler, template
from logic.models import PerformanceReview, SharedForm

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

        shared_forms = SharedForm.all().filter('user', user).fetch(1000)

        template_values = {
                           'periods': periods.values(),
                           'current_user': user.email,
                           'shared_forms': shared_forms}

        path = 'templates/api.manager.html'
        self.response.out.write(template.render(path, template_values))