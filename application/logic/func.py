import hashlib
import random
import string
from google.appengine.api import mail, users
from logic.models import PerformanceReview


def make_password(password):

    salt = ''.join(random.choice(
        string.ascii_uppercase
        + string.ascii_lowercase
        + string.digits) for x in range(4))
    hash = hashlib.sha1(salt + password).hexdigest()
    return salt + hash


def check_password(str_pass, hash_pass):

    salt = hash_pass[0:4]
    hash = hash_pass[4:]
    return hash == hashlib.sha1(salt + str_pass).hexdigest()


def send_message(receiver, subject, text):

    message = mail.EmailMessage()
    message.sender = users.get_current_user().email()
    message.subject = subject
    message.to = receiver
    message.body = text

    mail.check_email_valid(receiver, message.to)
    message.send()

def get_prev_pr(pr):

    prev_pr = PerformanceReview.all().order('-date').\
                                        filter('date <', pr.date).\
                                        filter('employee', pr.employee).get()

    return prev_pr

    
    
