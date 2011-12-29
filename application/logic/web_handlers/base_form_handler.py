from google.appengine.api import users
from google.appengine.ext import blobstore
from google.appengine.ext.db import BadKeyError
from google.appengine.ext.webapp import RequestHandler
from logic.models import PerformanceReview, PerformanceReviewForm


class BaseFormHandler(RequestHandler):

    template_values = {}
    path = ''
    type = ''

    def get(self, key):

        user = self.request.environ['current_user']

        login_url = users.create_login_url(self.request.uri)
        logout_url = users.create_logout_url(login_url)

        try:
            pr = PerformanceReview.get(key)
        except:
            try:
                form = PerformanceReviewForm.get(key)
                pr = form.pr
            except:
                self.error(405)
                return

        form = pr.forms.filter('type', self.type).get()
        prev_pr = PerformanceReview.all().order('-date').\
                                        filter('date <', pr.date).\
                                        filter('employee', pr.employee).get()
        if prev_pr is not None:
            prev_form = prev_pr.forms.filter('type', self.type).get()
        else:
            prev_form = None

        upload_url = blobstore.create_upload_url('/upload')

        self.template_values.update({'form': form,
                                     'file_key': form.file_key,
                                     'user': user,
                                     'upload_url': upload_url,
                                     'prev_form': prev_form,
                                     'file_name': form.file_name})
