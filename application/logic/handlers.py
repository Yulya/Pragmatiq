import base64
import datetime
from webob import Request, Response
from django.utils import simplejson as json
from google.appengine.api import users
from google.appengine.api.datastore_errors import BadKeyError
from google.appengine.ext.db import Model
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp import RequestHandler
from logic import models
from logic.func import check_password, make_password
from logic.models import User, PerformanceReviewForm, PerformanceReview, Role


class MainHandler(RequestHandler):

    def get(self):


        user = self.request.environ['current_user']

        login_url = users.create_login_url(self.request.uri)
        logout_url = users.create_logout_url(login_url)
        roles = []
        for role_key in user.role:
            roles.append(Model.get(role_key).value)
        template_values = {'user': user,
                           'roles': roles,
                           'url': logout_url}

        path = 'templates/index.html'
        self.response.out.write(template.render(path, template_values))


class UserTable(RequestHandler):

    def get(self):

        users = User.all()

        template_values = {'users': users,
                           }

        path = 'templates/users.html'
        self.response.out.write(template.render(path, template_values))

class CreateUser(RequestHandler):

#    def post(self):
#
#        data = json.loads(self.request.body)
#        roles = data['role'].split(',')
#        role_keys = []
#        for role in roles:
#            role_key = Role.gql("WHERE value = :value",
#                                value = role).get().key()
#            if role_key is not None:
#                role_keys.append(role_key)
#
#        try:
#            user = User(first_name=data['first_name'],
#                        username=data['username'],
#                        password=data['password'],
#                        last_name=data['last_name'],
#                        e_mail=data['e_mail'],
#                        salary=int(data['salary']),
#                        role=role_keys,
#                        first_date=datetime.datetime.strptime(
#                        data['first_date'], '%d-%m-%Y').date())
#
#
#            user.put()
#
#        except ValueError, e:
#            self.response.set_status(400, e.message)

    def post(self):

        first_name = self.request.get('first_name')
        e_mail = self.request.get('e_mail')
        last_name = self.request.get('last_name')
        manager = self.request.get('user')

class GetSelfPr(RequestHandler):

    def get(self):

        user = self.request.environ['current_user']

        login_url = users.create_login_url(self.request.uri)
        logout_url = users.create_logout_url(login_url)

        pr = PerformanceReview.gql("WHERE employee = :user", user = user).get()
        form = pr.forms.filter('author', user).get()
        if form is None:
            return
        self.response.out.write(form.key())



class GetPrs(RequestHandler):

    def get(self):

        user = self.request.environ['current_user']

        login_url = users.create_login_url(self.request.uri)
        logout_url = users.create_logout_url(login_url)
        employees = User.all().fetch(1000)

        for employee in employees:

            pr = PerformanceReview.gql("WHERE employee = :employee\
                                        AND manager = :user",
                                       employee = employee, user = user).get()
            if pr is None:
                employee.self_form = None
                employee.manager_form = None
            else:
                employee.self_form = PerformanceReviewForm.gql(
                    "WHERE author = :employee AND pr = :pr",
                    employee = employee, pr = pr).get()
                employee.manager_form = PerformanceReviewForm.gql(
                    "WHERE author = :user AND pr = :pr",
                    user = user, pr = pr).get()

        template_values = {'user': user,
                           'employees': employees,
                           'url': logout_url}

        path = 'templates/manager.html'
        self.response.out.write(template.render(path, template_values))


class AddPrForm(RequestHandler):

    def get(self, key):

        
        login_url = users.create_login_url(self.request.uri)
        logout_url = users.create_logout_url(login_url)

        user = self.request.environ['current_user']
        emp = Model.get(key)

        pr = PerformanceReview.gql("WHERE employee = :employee",
                                   employee = emp, manager = user).get()

        pr_form = PerformanceReviewForm.gql("WHERE pr =:pr \
                                            AND author = :author",
                                            pr=pr, author=user).get()

        if pr_form is None:
            pr_form = PerformanceReviewForm(pr=pr,author=user)
            pr_form.put()
        
        template_values = {'key': pr_form.key(),
                           'url': logout_url}

        path = 'templates/as_form.html'
        self.response.out.write(template.render(path, template_values))


class GetPrForm(RequestHandler):

    def get(self, key):

        login_url = users.create_login_url(self.request.uri)
        logout_url = users.create_logout_url(login_url)

        try:
            form = PerformanceReviewForm.get(key)
        except BadKeyError:
            self.error(405)
            return

        next_goals = form.next_goals
        challengers = form.challengers
        achievements = form.achievements

        template_values = {'url': logout_url,
                           'key': key,
                           'next_goals': next_goals,
                           'challengers': challengers,
                           'achievements': achievements}

        path = 'templates/as_form.html'
        self.response.out.write(template.render(path, template_values))


class UpdateData(RequestHandler):

    def post(self, object_key):

        value = self.request.get('value')
        try:
            obj = Model.get(object_key)
        except BadKeyError:
            self.error(405)
            return

        obj.value = self.request.get('value')
        obj.put()


class AddData(RequestHandler):

    def post(self):

        dict = {'next_goals': 'NextGoals',
                'challengers': 'Challengers',
                'achievements': 'Achievements'}

        form_key = self.request.get('form_key')
        table = self.request.get('table')

        try:
            attr = getattr(models, dict[table])
        except AttributeError, KeyError:
            self.error(405)
            return

        obj = attr()

        try:
            obj.form = PerformanceReviewForm.get(form_key)
            obj.put()
            key = obj.key()
        except BadKeyError:
            self.error(405)
            return

        self.response.out.write(key)


class CreateRoles(RequestHandler):

    def get(self):
        
        role = Role(value='manager')
        role.put()
        k = role.key()
        role = Role(value='employee')
        role.put()
        role = Role(value='hr')
        role.put()


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

            user_info = User.gql("WHERE username = :username ",
                        username=username).get()

            if user_info is None:
                resp = Response(status="401")
                return resp(environ, start_response)

            if not check_password(password, user_info.password):
                resp = Response(status="401")
                return resp(environ, start_response)
        else:
            user_info = User.gql("WHERE e_mail = :e_mail",
                                 e_mail=user.email()).get()
            if user_info is None:
                user_info = User(
                    e_mail=user.email())

        environ["current_user"] = user_info
        resp = req.get_response(self.app)
        return resp(environ, start_response)
