import logging
from google.appengine.ext.db import BadKeyError
from google.appengine.ext.webapp import RequestHandler
from logic.models import CommentToForm

class SaveComment(RequestHandler):

    def post(self, comment_key):

        comment = self.request.get('comment')
        logging.debug(comment)
        try:
            comment_to_form = CommentToForm.get(comment_key)
        except BadKeyError:
            self.response.out.write('Error')
            return

        comment_to_form.comments.append(comment)
        comment_to_form.put()
        self.response.out.write('ok')