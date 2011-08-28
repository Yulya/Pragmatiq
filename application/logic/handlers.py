import base64
import datetime
from webob import Request, Response
from django.utils import simplejson as json
from google.appengine.api import users
from google.appengine.ext.db import Model
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp import RequestHandler
from logic.func import check_password, make_password
from logic.models import Employee, Usr, PreviousGoals, NextGoals


class MainHandler(RequestHandler):

    def get(self):

        login_url = users.create_login_url(self.request.uri)
        logout_url = users.create_logout_url(login_url)
        emp_query = Employee.all()
        employees = emp_query.fetch(1000)
        template_values = {'employees': employees,
                           'url': logout_url}

        path = 'templates/emp.html'
        self.response.out.write(template.render(path, template_values))


class CreateEmployee(RequestHandler):

    def post(self):

        data = json.loads(self.request.body)
        try:
            employee = Employee(first_name=data['first_name'],
                                 last_name=data['last_name'],
                                 e_mail=data['e_mail'],
                                 salary=int(data['salary']),
                                 first_date=datetime.datetime.strptime(
                                     data['first_date'], '%d-%m-%Y').date())

            employee.put()
        #python2.5 doesn't support following syntax
        #except ValueError as e;
        except ValueError, e:
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


class ShowAssessmentForm(RequestHandler):

    def get(self):

        url = users.create_logout_url(users.create_login_url(self.request.uri))
        template_values = {'url': url}

        path = 'templates/as_form.html'
        self.response.out.write(template.render(path, template_values))


class AddAssessmentForm(RequestHandler):

    def post(self):

        if self.request.get('key'):
            key = self.request.get('key')
            obj = Model.get(key)
            obj.value = self.request.get('value')
            obj.put()
        else:
            key = ''
            if self.request.get('table'):
                if self.request.get('table') == 'next_goals':
                    next_goal = NextGoals()
                    next_goal.put()
                    key = next_goal.key()
                elif self.request.get('table') == 'challengers':
                    next_goal = NextGoals()
                    next_goal.put()
                    key = next_goal.key()
                elif self.request.get('table') == 'achievements':
                    next_goal = NextGoals()
                    next_goal.put()
                    key = next_goal.key()
                else:
                    self.error(400)
            else:
                self.error(400)
            self.response.out.write(key)


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
                resp = Response(status="307", location=url)
                return resp(environ, start_response)

            username, password = '', ''
            try:
                user_info = base64.decodestring(auth_header[6:])
                username, password = user_info.split(':')

            except ValueError:
                resp = Response(status="401")
                return resp(environ, start_response)

            user_info = Usr.gql("WHERE username = :username ",
                        username=username).get()

            if user_info is None:
                resp = Response(status="401")
                return resp(environ, start_response)

            if not check_password(password, user_info.password):
                resp = Response(status="401")
                return resp(environ, start_response)

        resp = req.get_response(self.app)
        return resp(environ, start_response)
