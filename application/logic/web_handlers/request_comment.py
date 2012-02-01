from google.appengine.ext.webapp import RequestHandler
from logic.models import User, CommentToForm, PerformanceReview

class RequestComment(RequestHandler):

    def post(self):

        manager_email = self.request.get('manager_email')
        pr_key = self.request.get('pr_key')

        manager = User.gql("WHERE email = :manager_email", manager_email = manager_email).get()
        pr = PerformanceReview.get(pr_key)

        if manager is None:
            self.response.out.write('Some error happened. Try again please')
            return

        comment_to_form = CommentToForm.gql("WHERE pr = :pr AND manager = :manager", pr = pr, manager = manager).get()

        if comment_to_form is None:
            comment_to_form = CommentToForm(manager = manager,
                                        pr = pr)
            comment_to_form.put()

            self.response.out.write('You have successfully requested comment form %s %s' %(manager.first_name, manager.last_name))
        else:
            self.response.out.write('You have already requested comment form %s %s' %(manager.first_name, manager.last_name))
