import hashlib
import random
import string
from google.appengine.api import mail, users


def make_password(password):
    salt = ''.join(random.choice(
        string.ascii_uppercase
        + string.ascii_lowercase
        + string.digits) for x in range(4))
    hash = hashlib.sha1(salt + password).hexdigest()
    return salt + '$' + hash


def check_password(str_pass, hash_pass):
    salt, hash = hash_pass.split('$')
    return hash == hashlib.sha1(salt + str_pass).hexdigest()


def send_message(receiver, subject, text):

    message = mail.EmailMessage()
    message.sender = users.get_current_user().email()
    message.subject = subject
    message.to = receiver
    message.body = text

    mail.check_email_valid(receiver, message.to)
    message.send()
