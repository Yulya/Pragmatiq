import logging
from google.appengine.ext.webapp import RequestHandler

class UpdateManagerSettings(RequestHandler):

    def post(self):

        manager = self.request.environ['current_user']
        
        edit_sub_reviews = int(self.request.get('edit_sub_reviews'))

        manager.edit_sub_reviews = edit_sub_reviews
        manager.put()
        logging.debug(edit_sub_reviews)



