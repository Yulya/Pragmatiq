import base64
from google.appengine.api import users
from google.appengine.ext.db import Model
from webob import Request, Response
from logic.func import check_password
from logic.models import User

class Authentication(object):

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):

        current_user = users.get_current_user()
        url = users.create_login_url("/")

        req = Request(environ)

        non_auth_urls = ['/create_role', '/users', '/add_emp', '/new_user', '/upload_contacts', '/parse_xls']
        if environ['PATH_INFO'] not in non_auth_urls:

            if current_user is None:
                try:
                    auth_header = req.headers['Authorization']
                except KeyError:
                    resp = Response(status="307", location=url)
                    return resp(environ, start_response)

                username, password = '', ''
                try:
                    user_info = base64.decodestring(auth_header[6:])
                    username, password = user_info.split(':')

                except ValueError:
                    resp = Response(status="401")
                    return resp(environ, start_response)

                user_info = User.gql("WHERE username = :username ",
                            username=username).get()

                if user_info is None:
                    resp = Response(status="401")
                    return resp(environ, start_response)

                if not check_password(password, user_info.password):
                    resp = Response(status="401")
                    return resp(environ, start_response)
            else:
                user_info = User.all().filter('email', str(current_user.email())).get()
                
                if user_info is None:
                    user_info = User(
                        email=current_user.email())
                    user_info.put()

            environ["current_user"] = user_info

            try:
                environ["current_role"] = Model.get(user_info.role[0]).value
            except IndexError:
                environ["current_role"] = ''

        resp = req.get_response(self.app)
        return resp(environ, start_response)
