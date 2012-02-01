from google.appengine.ext import db


class Role(db.Model):
    value = db.StringProperty()

class Dept(db.Model):
    name = db.StringProperty()

class User(db.Model):
    first_name = db.StringProperty()
    last_name = db.StringProperty()
    email = db.StringProperty()
    position = db.StringProperty()
    password = db.StringProperty()
    role = db.ListProperty(db.Key)
    manager = db.SelfReferenceProperty(collection_name='subs')
    dept = db.ReferenceProperty(Dept, collection_name='users')
    first_date = db.DateProperty()
    edit_sub_reviews = db.IntegerProperty(choices=(0, 1), default=0)


class Event(db.Model):
    start_date = db.DateProperty()
    finish_date = db.DateProperty()
    first_effective_date = db.DateProperty()
    type = db.StringProperty()


class ContactXlsFile(db.Model):
    file_key = db.StringProperty()


class PerformanceReviewPeriod(db.Model):
    description = db.StringProperty()
    start_date = db.DateProperty()
    finish_date = db.DateProperty()
    type = db.StringProperty(choices=('annual','semi-annual'))
    is_open = db.BooleanProperty(default=True)


class PerformanceReview(db.Model):
    employee = db.ReferenceProperty(User, collection_name='self_pr')
    manager = db.ReferenceProperty(User, collection_name='managed_pr')
    date = db.DateProperty()
    first_effective_date = db.DateProperty()
    period = db.ReferenceProperty(PerformanceReviewPeriod,
                                  collection_name='performance_reviews')

    @property
    def employee_form(self):
        return self.forms.filter('type', 'employee').get()

    @property
    def manager_form(self):
        return self.forms.filter('type', 'manager').get()

    @property
    def is_open(self):
        if self.manager_form is None:
            return True
        result = self.manager_form.status != "approved"
        return result



class PerformanceReviewForm(db.Model):
    pr = db.ReferenceProperty(PerformanceReview, collection_name='forms')
    type = db.StringProperty(choices=('manager','employee'))
    status = db.StringProperty(default='draft', choices=('draft',
                                                         'submitted',
                                                         'registered',
                                                         'approved'))
    lock_time = db.DateTimeProperty()
    user_locked_form = db.ReferenceProperty(User)
    file_key = db.StringProperty()
    file_name = db.StringProperty()

    @property
    def get_all_data(self):

        data = {'next_goals' : self.next_goals,
                'challenges' : self.challenges,
                'achievements' : self.achievements,
                'projects' : self.projects,
                'responsibilities' : self.responsibilities,
                'skills' : self.skills,
                'careers' : self.careers,
                'issues' : self.issues,
                'complaints' : self.complaints,
                'manager_helps' : self.manager_helps,
                'position': self.position.get(),
                'salary': self.salary.get(),
                'grade': self.grade.get(),
                'job_assessment': self.job_assessment.get(),
                'conclusion': self.conclusion.get()}
        return data


class CommentToForm(db.Model):
    manager = db.ReferenceProperty(User, collection_name='requested_comments')
    comment = db.TextProperty()
    pr = db.ReferenceProperty(PerformanceReview, collection_name='comments')

class HrComment(db.Model):
    value = db.StringProperty()
    form = db.ReferenceProperty(PerformanceReviewForm,
                                collection_name='hr_comments')

class ManagerComment(db.Model):
    value = db.StringProperty()
    manager = db.ReferenceProperty()
    form = db.ReferenceProperty(PerformanceReviewForm,
                                collection_name='manager_comments')

class Position(db.Model):
    value = db.StringProperty()
    form = db.ReferenceProperty(PerformanceReviewForm,
                                collection_name='position')

class JobAssessment(db.Model):
    value = db.StringProperty(default='5', choices=('1','2','3','4','5','6','7','8','9','10'))
    form = db.ReferenceProperty(PerformanceReviewForm,
                                collection_name='job_assessment')

class Project(db.Model):
    form = db.ReferenceProperty(PerformanceReviewForm,
                                collection_name='projects')
    value = db.StringProperty()


class Grade(db.Model):
    form = db.ReferenceProperty(PerformanceReviewForm,
                                collection_name='grade')
    value = db.StringProperty()


class Salary(db.Model):
    form = db.ReferenceProperty(PerformanceReviewForm,
                                collection_name='salary')
    value = db.StringProperty()


class Responsibility(db.Model):
    form = db.ReferenceProperty(PerformanceReviewForm,
                                collection_name='responsibilities')
    value = db.StringProperty()


class Skill(db.Model):
    form = db.ReferenceProperty(PerformanceReviewForm,
                                collection_name='skills')
    value = db.StringProperty()


class Career(db.Model):
    form = db.ReferenceProperty(PerformanceReviewForm,
                                collection_name='careers')
    value = db.StringProperty()


class Issue(db.Model):
    form = db.ReferenceProperty(PerformanceReviewForm,
                                collection_name='issues')
    value = db.StringProperty()


class Complaint(db.Model):
    form = db.ReferenceProperty(PerformanceReviewForm,
                                collection_name='complaints')
    value = db.StringProperty()


class ManagerHelp(db.Model):
    form = db.ReferenceProperty(PerformanceReviewForm,
                                collection_name='manager_helps')
    value = db.StringProperty()


class PreviousGoals(db.Model):
    form = db.ReferenceProperty(PerformanceReviewForm,
                                collection_name='previous_goals')
    value = db.StringProperty()
    result = db.IntegerProperty(default=2, choices=(1, 2, 3))
    comment = db.StringProperty()


class NextGoals(db.Model):
    form = db.ReferenceProperty(PerformanceReviewForm,
                                collection_name='next_goals')
    value = db.StringProperty()
    comment = db.StringProperty()
    result = db.IntegerProperty(default=2, choices=(1, 2, 3))


class Achievements(db.Model):
    form = db.ReferenceProperty(PerformanceReviewForm,
                                collection_name='achievements')
    value = db.StringProperty()



class Challenges(db.Model):
    form = db.ReferenceProperty(PerformanceReviewForm,
                                collection_name='challenges')
    value = db.StringProperty()



class Conclusion(db.Model):
    form = db.ReferenceProperty(PerformanceReviewForm,
                                collection_name='conclusion')
    value = db.StringProperty(choices=('meet expectations',
                                       'below expectations',
                                       'above expectations'),
                              default='meet expectations')
    
