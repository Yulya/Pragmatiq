import datetime
from google.appengine.ext.webapp import RequestHandler
from logic.models import PerformanceReviewForm

class LockFormHandler(RequestHandler):

    def get(self, form_key):

        form = PerformanceReviewForm.get(form_key)

        current_time = datetime.datetime.now()

        user = self.request.environ['current_user']
        minute = datetime.timedelta(seconds=60)
        user_locked_form = form.user_locked_form
        lock_time = form.lock_time

        if user_locked_form.email == user.email:
            form.lock_time = current_time + minute
            form.put()
            self.response.out.write('ok')
            return

        if form.lock_time is None:
            form.user_locked_form = user
            form.lock_time = current_time + minute
            form.put()
            self.response.out.write('ok')
            return
        
        if form.lock_time < current_time:
            form.user_locked_form = user
            form.lock_time = current_time + minute
            form.put()
            self.response.out.write('ok')
            return

        self.response.out.write('form is locked by %s'
                                %form.user_locked_form.email)