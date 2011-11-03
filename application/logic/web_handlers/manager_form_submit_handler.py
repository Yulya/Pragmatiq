from google.appengine.ext.webapp import RequestHandler
from logic.models import PerformanceReviewForm

class ManagerFormSubmit(RequestHandler):

    def get(self, key):

        user = self.request.environ['current_user']

        form = PerformanceReviewForm.get(key)

        if form.pr.manager.email != user.email:
            self.error(307)
            return

        errors = []
        try:
            form.salary[0]
        except IndexError:
            errors.append("put employee's salary")
        try:
            form.grade[0]
        except IndexError:
            errors.append("put employee's grade")
        try:
            form.conclusion[0]
        except IndexError:
            errors.append("put PR conclusion")

        if not errors:
            form.status = 'submitted'
            form.put()
            self.response.out.write('ok')
        else:
            self.response.out.write('\n'.join(errors))