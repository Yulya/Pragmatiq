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
from logic.models import User, PerformanceReviewForm


class MainHandler(RequestHandler):

    def get(self):

        login_url = users.create_login_url(self.request.uri)
        logout_url = users.create_logout_url(login_url)

        forms = PerformanceReviewForm.all()
        keys = []
        for form in forms:
            keys.append(form.key())

        template_values = {'keys': keys,
                           'url': logout_url}

        path = 'templates/index.html'
        self.response.out.write(template.render(path, template_values))


class CreateUser(RequestHandler):

    def post(self):

        data = json.loads(self.request.body)
        try:
            user = User(first_name=data['first_name'],
                        username=data['username'],
                        password=data['password'],
                        last_name=data['last_name'],
                        e_mail=data['e_mail'],
                        salary=int(data['salary']),
                        first_date=datetime.datetime.strptime(
                        data['first_date'], '%d-%m-%Y').date())

            user.put()

        except ValueError, e:
            self.response.set_status(400, e.message)


class CreateUser(RequestHandler):

    def post(self):
        data = json.loads(self.request.body)
        try:
            usr = User(username=data['username'],
                      password=make_password(data['password']))

            usr.put()

        except Exception:
            self.response.set_status(400)


class AddPrForm(RequestHandler):

    def get(self):

        login_url = users.create_login_url(self.request.uri)
        logout_url = users.create_logout_url(login_url)

        form = PerformanceReviewForm()
        form.put()
        key = form.key()

        template_values = {'key': key,
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
                                 e_mail=user.email())
            if user_info is None:
                user = User(
                    e_mail=user.email())

        resp = req.get_response(self.app)
        return resp(environ, start_response)
