import json
from google.appengine.ext.webapp import RequestHandler
from logic.models import User


class GetJSONUsers(RequestHandler):

    def get(self):

        term = self.request.get('term')

        users = User.all().fetch(1000)

        users = filter(lambda x: x.email[:len(term)] == term, users)

        user_list = map(lambda x: x.email, users)

        user_list_json = json.dumps(user_list)
        self.response.out.write(user_list_json)
