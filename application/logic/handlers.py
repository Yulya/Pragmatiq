import base64
from webob import Request, Response
import datetime
from google.appengine.api import users
from google.appengine.api.datastore_errors import BadKeyError
from google.appengine.ext.db import Model
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp import RequestHandler
from logic import models
from logic.func import check_password, send_message
from logic.models import User, PerformanceReviewForm, PerformanceReview, Role, Dept


class MainHandler(RequestHandler):

    #gets current user and returns his roles

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

    #selects all users and returns them

    def get(self):

        users = User.all().fetch(1000)
        for user in users:
            user.roles = ''
            for role in user.role:
                user.roles = user.roles + Model.get(role).value + ' '

        template_values = {'users': users,
                           }

        path = 'templates/users.html'
        self.response.out.write(template.render(path, template_values))


class GetManagers(RequestHandler):

    def get(self):

        users = User.all()
        managers = []
        for user in users:
            for role in user.role:
                if Model.get(role).value == 'manager':
                    managers.append(user)

        template_values = {'managers': managers,
                           }

        path = 'templates/new_user.html'
        self.response.out.write(template.render(path, template_values))


class CreateUser(RequestHandler):

    #gets data and puts them to DB

    def post(self):

        first_name = self.request.get('first_name')
        e_mail = self.request.get('e_mail')
        last_name = self.request.get('last_name')
        dept = self.request.get('dept')

        dept_ref = Dept.all().filter('name', dept).get()

        if dept_ref is None:
            dept_ref = Dept(name=dept)
            dept_ref.put()

        try:
            manager = Model.get(self.request.get('manager'))
        except BadKeyError:
            manager = None

        roles = self.request.get('role')[:-1].split(',')
        try:
            user = User(first_name=first_name,
                        e_mail=e_mail,
                        last_name=last_name,
                        dept=dept_ref,
                        manager=manager)
        
            for role in roles:
                role_key = Role.gql("WHERE value = :role", role=role).get().key()
                user.role.append(role_key)

            user.put()
        except ValueError:
            self.response.out.write('error')
            return
        self.response.out.write('ok')


class GetPreviousGoals(RequestHandler):

    def get(self, form_key):

        form = Model.get(form_key)

        pr = form.pr
        author = form.author

        prev_pr = PerformanceReview.all().order('-date').filter('date <', pr.date).filter('employee', pr.employee).get()

        if prev_pr is None:
            self.response.out.write("there aren't previous goals")
            return

        prev_form = prev_pr.forms.filter('author', author).get()
        prev_goals = prev_form.next_goals

        template_values = {'prev_goals': prev_goals}

        path = 'templates/prev.html'
        self.response.out.write(template.render(path, template_values))


class GetSelfPR(RequestHandler):

    def get(self):

        user = self.request.environ['current_user']

        pr = PerformanceReview.gql("WHERE employee = :user", user=user).get()
        form = pr.forms.filter('author', user).get()
        if form is None:
            return
        else:
            self.response.out.write(form.key())
            return


class GetPrs(RequestHandler):

    #selects all PR objects for current user's subs and returns them

    def get(self):

        user = self.request.environ['current_user']

        login_url = users.create_login_url(self.request.uri)
        logout_url = users.create_logout_url(login_url)

        employees = user.subs.fetch(1000)

        for employee in employees:

            pr = PerformanceReview.all().filter('employee', employee).order('-date').get()

            if pr is None:
                employee = None
            else:
                employee.self_form = pr.forms.filter('author', employee).get()
                employee.manager_form = pr.forms.filter('author', user).get()
                    
        template_values = {'user': user,
                           'employees': employees,
                           'url': logout_url}

        path = 'templates/manager.html'
        self.response.out.write(template.render(path, template_values))


class CreatePR(RequestHandler):

    #creates PR objects for all employees

    def post(self):

        user = self.request.environ['current_user']

        role_key = Role.gql("WHERE value = :hr", hr='hr').get().key()

        if role_key not in user.role:
            self.error(403)
            return

        date_str = self.request.get('date')
        type = self.request.get('type')

        employees = self.request.get('employees')[:-1].split(',')

        try:
            date = datetime.datetime.strptime(date_str, '%d.%m.%Y').date()
        except ValueError:
            self.response.out.write('incorrect date')
            self.error(403)
            return

        for employee in employees:

            user = Model.get(employee)

            if user.manager is not None:
                pr = PerformanceReview(employee=user,
                                       manager=user.manager,
                                       type=type,
                                       date=date)
                pr.put()
            else:
                pr = PerformanceReview(employee=user,
                                       type=type,
                                       date=date)
                pr.put()
        self.response.out.write('ok')


class AddPrForm(RequestHandler):

    #gets employee's key, select employee's PR

    def get(self, key):

        login_url = users.create_login_url(self.request.uri)
        logout_url = users.create_logout_url(login_url)

        user = self.request.environ['current_user']
        emp = Model.get(key)

        pr = PerformanceReview.all().filter('employee', emp).order('-date').get()

        pr_form = pr.forms.filter('author', user).get()

        if pr_form is None:
            pr_form = PerformanceReviewForm(pr=pr, author=user)
            pr_form.put()

        template_values = {'key': pr_form.key(),
                           'emp': emp,
                           'author': user,
                           'user': user,
                           'url': logout_url}

        path = 'templates/as_form.html'
        self.response.out.write(template.render(path, template_values))


class GetPrForm(RequestHandler):

    def get(self, key):

        user = self.request.environ['current_user']

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
                           'user': user,
                           'author': form.author,
                           'emp': form.pr.employee,
                           'next_goals': next_goals,
                           'challengers': challengers,
                           'achievements': achievements}

        if user.key() == form.author.key():
            path = 'templates/as_form.html'
            self.response.out.write(template.render(path, template_values))
        else:
            path = 'templates/form_data.html'
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

    def post(self):

        try:
            role = Role(value='manager')
            role.put()
            role = Role(value='employee')
            role.put()
            role = Role(value='hr')
            role.put()
        except:
            self.response.out.write('error')
            return


class CheckDate(RequestHandler):

    def get(self):

        today = datetime.date.today()
        subject = 'Performance Review'

        month = datetime.timedelta(days=30)
        two_weeks = datetime.timedelta(days=14)
        week = datetime.timedelta(days=7)

        prs = PerformanceReview.all().filter('date >=', today)

        for pr in prs:

            delta = pr.date - today
            text = 'Your Performance Review starts in ' \
                   + str(delta.days) + ' days'

            if delta == month or delta == two_weeks or delta <= week:

                send_message(pr.employee.e_mail, subject, text)


class HR(RequestHandler):
    
    def get(self):

        depts = Dept.all()

        template_values = {'depts': depts}

        path = 'templates/hr.html'
        self.response.out.write(template.render(path, template_values))


class Show(RequestHandler):

    def get(self):

        prs = PerformanceReview.all()

        template_values = {'prs': prs}

        path = 'templates/pr.html'
        self.response.out.write(template.render(path, template_values))



class Authentication(object):

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):

        user = users.get_current_user()
        url = users.create_login_url("/")

        req = Request(environ)

        non_auth_urls = ['/create_role', '/users', '/add_emp', '/new_user']
        if environ['PATH_INFO'] not in non_auth_urls:

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
                    user_info.put()

            environ["current_user"] = user_info
        resp = req.get_response(self.app)
        return resp(environ, start_response)
