import logging
from google.appengine.api.datastore_errors import BadKeyError
from google.appengine.ext.webapp import RequestHandler
from logic.models import PerformanceReviewForm, User, SharedForm


class ShareForm(RequestHandler):

    def post(self):

        form_key = self.request.get('form_key')
        users = self.request.get('users')
        try:
            form = PerformanceReviewForm.get(form_key)
        except BadKeyError:
            self.response.out.write('error')
            return

        message = ['%(emp_fn)s %(emp_ln)s form shared to'
                                % {'emp_fn': form.pr.employee.first_name,
                                  'emp_ln': form.pr.employee.last_name}]

        user_emails = users.split(',')
        logging.debug(user_emails)
        for email in user_emails:
            if email:
                user = User.all().filter('email', email).get()
                if user:
                    shared_form = SharedForm.all().filter('form', form)\
                                                  .filter('user', user).get()
                    if not shared_form:
                        shared_form = SharedForm(user=user,
                                        form=form)
                        shared_form.put()

                message.append('%(first_name)s %(last_name)s,'
                                % {'first_name': user.first_name,
                                  'last_name': user.last_name})
        if len(message) > 1:
            self.response.out.write(' '.join(message)[:-1])
