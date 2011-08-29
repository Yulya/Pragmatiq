from google.appengine.ext import db


class Employee(db.Model):
    first_name = db.StringProperty()
    last_name = db.StringProperty()
    e_mail = db.EmailProperty()
    salary = db.IntegerProperty()
    first_date = db.DateProperty()


class Usr(db.Model):
    username = db.StringProperty()
    password = db.StringProperty()
    roles = db.ListProperty(db.Key)


class Phone(db.Model):
    employee = db.ReferenceProperty(Employee,
                                 collection_name='phone_numbers')
    phone_type = db.StringProperty(
      choices=('home', 'work', 'fax', 'mobile', 'other'))
    number = db.PhoneNumberProperty()


class Roles(db.Model):
    role = db.StringProperty()


class AssessmentForm(db.Model):
    name = db.StringProperty()
    employee = db.ReferenceProperty(Employee, collection_name='pr')
    manager = db.ReferenceProperty(Employee, collection_name='emp_pr')


class PreviousGoals(db.Model):
    form = db.ReferenceProperty(AssessmentForm,
                                collection_name='previous_goals')
    value = db.StringProperty()
    result = phone_type = db.StringProperty(
      choices=('Below Expectations', 'Meet Expectations',
               'Above Expectations'))
    comment = db.StringProperty()


class NextGoals(db.Model):
    form = db.ReferenceProperty(AssessmentForm,
                                collection_name='next_goals')
    value = db.StringProperty()
    comment = db.StringProperty()


class Achievements(db.Model):
    form = db.ReferenceProperty(AssessmentForm,
                                collection_name='achievements')
    value = db.StringProperty()
    comment = db.StringProperty()
    

class Challengers(db.Model):
    form = db.ReferenceProperty(AssessmentForm,
                                collection_name='challengers')
    value = db.StringProperty()
    comment = db.StringProperty()


class Conclusion(db.Model):
    form = db.ReferenceProperty(AssessmentForm, collection_name='conclusion')
    value = db.StringProperty()
    comment = db.StringProperty()
