import base64
import datetime
import os
from webob import Request, Response
from django.utils import simplejson as json
from google.appengine.api import users
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp import RequestHandler
from logic.func import check_password, make_password
from logic.models import Employee, Usr

#
#class BaseHandler(RequestHandler):
#
#    def pre_get(self):
#        user = users.get_current_user()
#        if user is not None:
#            return user
#
#        basic_auth = self.request.headers.get('Authorization')
#        if not basic_auth:
#            self.error(401)
#            return
#
#        username, password = '', ''
#        try:
#            user_info = base64.decodestring(basic_auth[6:])
#            username, password = user_info.split(':')
#        except ValueError:
#            self.error(400)
#            return
#
#        user_info = Usr.gql("WHERE username = :username ",
#                            username=username).get()
#
#        if user_info is None:
#            self.error(401)
#            return
#
#        if not check_password(password, user_info.password):
#            self.error(401)
#            return
#
#        return user_info


class MainHandler(RequestHandler):

    def get(self):

#        user = self.pre_get()
#
#        if user is None:
#            url = users.create_login_url(self.request.uri)
#            self.redirect(url)
#
#        else:
#            try:
#                username = user.username
#            except AttributeError:
#                username = user.email()

            url = users.create_logout_url(users.create_login_url(self.request.uri))
            emp_query = Employee.all()
            employees = emp_query.fetch(1000)
            template_values = {'employees': employees,
#                               'user': username,
                               'url': url}

            path = os.path.join(os.path.dirname(__file__),
                                'templates/emp.html')
            self.response.out.write(template.render(path, template_values))


class CreateEmployee(RequestHandler):

    def post(self):

#        user = self.pre_get()
#
#        if not user:
#            self.response.set_status(401)
#            return

        data = json.loads(self.request.body)
        try:
            employee = Employee(first_name=data['first_name'],
                                 last_name=data['last_name'],
                                 e_mail=data['e_mail'],
                                 salary=int(data['salary']),
                                 first_date=datetime.datetime.strptime(
                                     data['first_date'], '%d-%m-%Y').date())

            employee.put()
        except ValueError as e:
            self.response.set_status(400, e.message)


class CreateUser(RequestHandler):

    def post(self):
        data = json.loads(self.request.body)
        try:
            usr = Usr(username=data['username'],
                      password=make_password(data['password']))

            usr.put()

        except Exception:
            self.response.set_status(400)


class Authentication(object):

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):

        user = users.get_current_user()
        url = users.create_login_url("/")

        req = Request(environ)

        if user is None:
            try:
                auth_header = req.headers['Authorization']
            except KeyError:
                resp = Response(status = "307", location = url)
                return resp(environ, start_response)

            username, password = '', ''
            try:
                user_info = base64.decodestring(auth_header[6:])
                username, password = user_info.split(':')

            except ValueError:
                resp = Response(status = "401")
                return resp(environ, start_response)

            user_info = Usr.gql("WHERE username = :username ",
                        username=username).get()

            if user_info is None:
                resp = Response(status = "401")
                return resp(environ, start_response)

            if not check_password(password, user_info.password):
                resp = Response(status = "401")
                return resp(environ, start_response)

        resp = req.get_response(self.app)
        return resp(environ, start_response)



