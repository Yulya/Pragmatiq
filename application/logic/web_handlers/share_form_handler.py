from google.appengine.api.datastore_errors import BadKeyError
from google.appengine.ext.webapp import RequestHandler
from logic.models import PerformanceReviewForm, User, SharedForm

class ShareForm(RequestHandler):

    def post(self):

        form_key = self.request.get('form_key')
        user_email = self.request.get('user_email').strip()

        try:
            form = PerformanceReviewForm.get(form_key)
        except BadKeyError:
            self.response.out.write('error')
            return

        user = User.all().filter('email', user_email).get()

        if not user:
            self.response.out.write('incorrect user email')
            return

        shared_form = SharedForm(user=user,
                                form=form)
        shared_form.put()

        message = ('%(emp_fn)s %(emp_ln)s form shared to %(u_fn)s %(u_ln)s'
                                %{'emp_fn': form.pr.employee.first_name,
                                  'emp_ln': form.pr.employee.last_name,
                                  'u_fn': user.first_name,
                                    'u_ln': user.last_name})
        self.response.out.write(message)