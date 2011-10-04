import base64
import urllib
from webob import Request, Response
import datetime
from google.appengine.api import users
from google.appengine.api.datastore_errors import BadKeyError
from google.appengine.ext import blobstore
from google.appengine.ext.db import Model
from google.appengine.ext.webapp import template, blobstore_handlers
from google.appengine.ext.webapp import RequestHandler
from logic import models
from logic.func import check_password, send_message
from logic.models import User, PerformanceReviewForm, PerformanceReview,\
    Role, Dept, NextGoals


class MainHandler(RequestHandler):

    #gets current user and returns his roles

    def get(self):

        user = self.request.environ['current_user']
        email = None
        if user is not None:
            email = user.email

        login_url = users.create_login_url(self.request.uri)
        logout_url = users.create_logout_url(login_url)
        roles = []
        for role_key in user.role:
            roles.append(Model.get(role_key).value)
        template_values = {
                           'username': email,
                           'user': user,
                           'roles': roles,
                           'logout_url': logout_url}

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


class UrlHandler(RequestHandler):

    def get(self):

        login_url = users.create_login_url('/')
        logout_url = users.create_logout_url(login_url)
        self.redirect(logout_url)

class CreateUser(RequestHandler):

    #gets data and puts them to DB

    def post(self):

        first_name = self.request.get('first_name')
        email = self.request.get('email')
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
                        email=email,
                        last_name=last_name,
                        dept=dept_ref,
                        manager=manager)
        
            for role in roles:
                role_key = Role.gql("WHERE value = :role",
                                    role=role).get().key()
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

        prev_pr = PerformanceReview.all().order('-start_date').\
                                          filter('start_date <', pr.date).\
                                          filter('employee', pr.employee).get()

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
        pr = PerformanceReview.all().filter('employee',user).\
                                     order('-start_date').get()
        try:
            form = pr.forms.filter('author', user).get()
        except AttributeError:
            self.response.out.write('pr not created')
            return
        if form is not None:
            self.response.out.write(form.key())
        

class GetPrs(RequestHandler):

    #selects all PR objects for current user's subs and returns them

    def get(self):

        user = self.request.environ['current_user']

        login_url = users.create_login_url(self.request.uri)
        logout_url = users.create_logout_url(login_url)

        employees = []

        for employee in user.subs.fetch(1000):

            pr = PerformanceReview.all().filter('employee', employee).\
                                        order('-start_date').get()

            if pr is not None:

                employee.self_form = pr.forms.filter('author', employee).get()
                employee.manager_form = pr.forms.filter('author', user).get()
                employees.append(employee)

        template_values = {'user': user,
                           'employees': employees,
                           'url': logout_url}

        path = 'templates/api.manager.html'
        self.response.out.write(template.render(path, template_values))


class CreatePR(RequestHandler):

    #creates PR objects for all employees

    def post(self):

        user = self.request.environ['current_user']

        role_key = Role.gql("WHERE value = :hr", hr='hr').get().key()

        if role_key not in user.role:
            self.error(403)
            return

        start_str = self.request.get('start')
        finish_str = self.request.get('finish')
        type = self.request.get('type')

        employees = self.request.get('employees')[:-1].split(',')

        try:
            start = datetime.datetime.strptime(start_str, '%d.%m.%Y').date()
            finish = datetime.datetime.strptime(finish_str, '%d.%m.%Y').date()
        except ValueError:
            self.response.out.write('incorrect start_date')
            self.error(403)
            return

        for employee in employees:

            user = Model.get(employee)


            if user.manager is not None:
                pr = PerformanceReview(employee=user,
                                       manager=user.manager,
                                       type=type,
                                       start_date=start,
                                       finish_date=finish)
                pr.put()
            else:
                pr = PerformanceReview(employee=user,
                                       type=type,
                                       start_date=start,
                                       finish_date=finish)
                pr.put()

                           

        self.response.out.write('ok')


class AddPrForm(RequestHandler):

    #gets employee's key, select employee's PR

    def get(self, key):

        login_url = users.create_login_url(self.request.uri)
        logout_url = users.create_logout_url(login_url)

        user = self.request.environ['current_user']
        emp = Model.get(key)

        pr = PerformanceReview.all().filter('employee', emp).\
                                    order('-start_date').get()

        pr_form = pr.forms.filter('author', user).get()

        if pr_form is None:
            pr_form = PerformanceReviewForm(pr=pr, author=user)
            pr_form.put()

        prev_pr = PerformanceReview.all().order('-start_date').\
                                        filter('start_date <', pr.start_date).\
                                        filter('employee', pr.employee).get()
        author = pr_form.author

        prev_goals = []

        try:
            prev_form = prev_pr.forms.filter('author', author).get()
            prev_goals = prev_form.next_goals
        except AttributeError:
            prev_goals = []

        upload_url = blobstore.create_upload_url('/upload')


        if pr.type == 'intermediate':

            for goal in prev_goals:
                next_goal = NextGoals(form=pr_form,value=goal.value).put()


        template_values = {'key': pr_form.key(),
                           'emp': emp,
                           'date': pr.finish_date,
                           'type': pr.type,
                           'prev_goals': prev_goals,
                           'next_goals': pr_form.next_goals,
                           'author': user, #todo: rename author to manager
                           'upload_url': upload_url,
                           'user': user,
                           'url': logout_url}

        path = 'templates/api.assessment_form.html'
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

        pr = form.pr
        author = form.author

        prev_pr = PerformanceReview.all().order('-start_date').\
                                        filter('start_date <', pr.start_date).\
                                        filter('employee', pr.employee).get()

        try:
            prev_form = prev_pr.forms.filter('author', author).get()
            prev_goals = prev_form.next_goals
        except AttributeError:
            prev_goals = []

        next_goals = form.next_goals
        challenges = form.challenges #todo: use challenges instead of challengers
        achievements = form.achievements
        projects = form.projects
        responsibilities = form.responsibilities
        skills = form.skills
        careers = form.careers
        issues = form.issues
        complaints = form.complaints
        manager_helps = form.manager_helps

        upload_url = blobstore.create_upload_url('/upload')

        
        template_values = {'url': logout_url,
                           'key': key,
                           'user': user,
                           'date': pr.finish_date,
                           'author': form.author, #todo: rename to manager
                           'emp': form.pr.employee,
                           'type': form.pr.type,
                           'file_key': form.file_key,
                           'file_name': form.file_name,
                           'upload_url': upload_url,
                           'prev_goals': prev_goals,
                           'next_goals': next_goals,
                           'challenges': challenges,
                           'careers': careers,
                           'achievements': achievements,
                           'projects': projects,
                           'responsibilities': responsibilities,
                           'skills': skills,
                           'issues': issues,
                           'complaints': complaints,
                           'manager_helps': manager_helps
                           }


        if user.key() == form.author.key():
            path = 'templates/api.assessment_form.html'
            self.response.out.write(template.render(path, template_values))
        else:
            path = 'templates/api.form_data.html'
            self.response.out.write(template.render(path, template_values))


class UpdateData(RequestHandler):

    def post(self, object_key):


        try:
            obj = Model.get(object_key)
        except BadKeyError:
            self.error(405)
            return

        if self.request.get('value'):
            obj.value = self.request.get('value')

        if self.request.get('grade'):
            obj.grade = int(self.request.get('grade'))
            
        obj.put()


class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):

    def post(self):
        
        upload_files = self.get_uploads('file')
        key = self.request.get('key')
        blob_info = upload_files[0]
        form = Model.get(key)
        form.file_key = str(blob_info.key())
        form.file_name = blob_info.filename

        form.put()
        self.redirect('/')

class ServeHandler(blobstore_handlers.BlobstoreDownloadHandler):
    
    def get(self, resource):

        resource = str(urllib.unquote(resource))
        blob_info = blobstore.BlobInfo.get(resource)
        self.send_blob(blob_info)



class AddData(RequestHandler):

    def post(self):

        dict = {'next_goals': 'NextGoals',
                'challenges': 'Challenges',
                'achievements': 'Achievements',
                'project': 'Project',
                'skill': 'Skill',
                'responsibility': 'Responsibility',
                'career': 'Career',
                'manager_help': 'ManagerHelp',
                'complaint': 'Complaint',
                'issue': 'Issue'}

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

        prs = PerformanceReview.all().filter('start_date >=', today)

        for pr in prs:

            delta = pr.date - today
            text = 'Your Performance Review starts in ' \
                   + str(delta.days) + ' days'

            if delta == month or delta == two_weeks or delta <= week:

                send_message(pr.employee.email, subject, text)


class HR(RequestHandler):
    
    def get(self):

        depts = Dept.all()

        template_values = {'depts': depts}

        path = 'templates/api.hr.html'
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

        current_user = users.get_current_user()
        url = users.create_login_url("/")

        req = Request(environ)

        non_auth_urls = ['/create_role', '/users', '/add_emp', '/new_user']
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
                user_info = User.gql("WHERE email = :email",
                                     email=current_user.email()).get()
                if user_info is None:
                    user_info = User(
                        email=current_user.email())
                    user_info.put()

            environ["current_user"] = user_info
        resp = req.get_response(self.app)
        return resp(environ, start_response)
