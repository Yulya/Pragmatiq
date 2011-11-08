from google.appengine.api import users
from google.appengine.ext.db import Model
from google.appengine.ext.webapp import RequestHandler
from logic.models import PerformanceReview, PerformanceReviewForm

class AddEmployeeForm(RequestHandler):

    type = 'employee'
    form = None
    flag = 1

    def get(self, key):

        login_url = users.create_login_url(self.request.uri)
        logout_url = users.create_logout_url(login_url)

        user = self.request.environ['current_user']
        emp = Model.get(key)

        pr = PerformanceReview.all().filter('employee', emp).\
                                    order('-date').get()

        pr_form = pr.forms.filter('type', self.type).get()

        if pr_form is None:
            pr_form = PerformanceReviewForm(pr=pr, type=self.type, status='draft')
            pr_form.put()
            
        self.form = pr_form

        if self.flag:
            self.redirect('/pr/get/%(type)s/%(key)s' % {'type': self.type, 'key': pr.key()})
