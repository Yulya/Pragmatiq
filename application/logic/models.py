from google.appengine.ext import db, blobstore


class Role(db.Model):
    value = db.StringProperty()


class User(db.Model):
    first_name = db.StringProperty()
    last_name = db.StringProperty()
    email = db.StringProperty()
    salary = db.IntegerProperty()
    first_date = db.DateProperty()
    username = db.StringProperty()
    password = db.StringProperty()
    role = db.ListProperty(db.Key)
    manager = db.SelfReferenceProperty(collection_name='subs')
    dept = db.ReferenceProperty(collection_name='users')


class Dept(db.Model):
    name = db.StringProperty()

class Phone(db.Model):
    employee = db.ReferenceProperty(User,
                                 collection_name='phone_numbers')
    phone_type = db.StringProperty(
      choices=('home', 'work', 'fax', 'mobile', 'other'))
    number = db.PhoneNumberProperty()


class PerformanceReview(db.Model):
    employee = db.ReferenceProperty(User, collection_name='self_pr')
    manager = db.ReferenceProperty(User, collection_name='managed_pr')
    type = db.StringProperty(choices=('main','intermediate'))
    start_date = db.DateProperty()
    finish_date = db.DateProperty()


class PerformanceReviewForm(db.Model):
    pr = db.ReferenceProperty(PerformanceReview, collection_name='forms')
    author = db.ReferenceProperty(User, collection_name='forms')
    file_key = db.StringProperty()
    file_name = db.StringProperty()


class Project(db.Model):
    form = db.ReferenceProperty(PerformanceReviewForm,
                                collection_name='projects')
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
    grade = db.IntegerProperty(default=2, choices=(1, 2, 3))


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
    value = db.StringProperty()
    
