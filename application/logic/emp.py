from google.appengine.ext import db

class Employee(db.Model):
    first_name = db.StringProperty()
    last_name = db.StringProperty()
    e_mail = db.StringProperty()
    salary = db.IntegerProperty()
    first_date = db.DateProperty()
