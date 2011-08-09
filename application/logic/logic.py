from google.appengine.ext import db

class Employee(db.Model):
    first_name = db.StringProperty()
    last_name = db.StringProperty()
    e_mail = db.StringProperty()
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
