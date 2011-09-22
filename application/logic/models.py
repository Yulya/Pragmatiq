from google.appengine.ext import db


class Role(db.Model):
    value = db.StringProperty()


class User(db.Model):
    first_name = db.StringProperty()
    last_name = db.StringProperty()
    e_mail = db.StringProperty()
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
    title = db.StringProperty()
    date = db.DateProperty()


class PerformanceReviewForm(db.Model):
    pr = db.ReferenceProperty(PerformanceReview, collection_name='forms')
    author = db.ReferenceProperty(User, collection_name='forms')


class PreviousGoals(db.Model):
    form = db.ReferenceProperty(PerformanceReviewForm,
                                collection_name='previous_goals')
    value = db.StringProperty()
    result = db.StringProperty(
      choices=('Below Expectations', 'Meet Expectations',
               'Above Expectations'))
    comment = db.StringProperty()


class NextGoals(db.Model):
    form = db.ReferenceProperty(PerformanceReviewForm,
                                collection_name='next_goals')
    value = db.StringProperty()
    comment = db.StringProperty()


class Achievements(db.Model):
    form = db.ReferenceProperty(PerformanceReviewForm,
                                collection_name='achievements')
    value = db.StringProperty()
    comment = db.StringProperty()


class Challengers(db.Model):
    form = db.ReferenceProperty(PerformanceReviewForm,
                                collection_name='challengers')
    value = db.StringProperty()
    comment = db.StringProperty()


class Conclusion(db.Model):
    form = db.ReferenceProperty(PerformanceReviewForm,
                                collection_name='conclusion')
    value = db.StringProperty()
    comment = db.StringProperty()
