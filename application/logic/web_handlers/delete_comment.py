from google.appengine.ext.db import BadKeyError
from google.appengine.ext.webapp import RequestHandler
from logic.models import CommentToForm

class DeleteComment(RequestHandler):

    def post(self, comment_key):

        user = self.request.environ['current_user']
        try:
            comment = CommentToForm.get(comment_key)
        except BadKeyError:
            return
        if user.email != comment.pr.manager.email:
            return
        comment.delete()
