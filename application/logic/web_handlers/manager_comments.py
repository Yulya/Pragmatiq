from google.appengine.ext.webapp import RequestHandler, template
from logic.models import PerformanceReview

class ManagerComments(RequestHandler):

    def get(self, pr_key):

        pr = PerformanceReview.get(pr_key)

        template_values = {
                   'pr': pr
                }

        path = 'templates/api.comments.html'
        self.response.out.write(template.render(path, template_values))