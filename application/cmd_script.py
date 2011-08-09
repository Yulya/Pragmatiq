import base64
from optparse import OptionParser
import json
import urllib2
import re
import datetime
import getpass



parser = OptionParser()
parser.add_option("-f","--first_name",dest="first_name")
parser.add_option("-l","--last_name",dest="last_name")
parser.add_option("-e","--e_mail",dest="e_mail")
parser.add_option("-s","--salary",dest="salary")
parser.add_option("-d","--first_date",dest="first_date")

username = raw_input('username:')
password = getpass.getpass()

(options, args) = parser.parse_args()
errors = []
if not options.first_name.isalpha():
    errors.append('enter correct first name')

if not options.first_name.isalpha():
    errors.append('enter correct last name')

if not options.salary.isdigit():
    errors.append('enter correct salary')

if re.match('^[0-9a-z]+[._0-9a-z-]+[0-9a-z]+@([0-9a-z][0-9a-z-]+.)+[a-z]{2,4}$',options.e_mail) == None:
    errors.append('enter correct e_mail')

try:
    first_date = datetime.datetime.strptime(options.first_date, '%d-%m-%Y')
except ValueError:
    errors.append('enter correct date in form dd-mm-YY. ')

if not errors:
    data = json.dumps({"first_name":options.first_name,
                   "last_name":options.last_name,
                   "e_mail":options.e_mail,
                   "salary":options.salary,
                   "first_date":options.first_date
                   })

    base64string = base64.encodestring(
                '%s:%s' % (username, password))[:-1]
    auth_header =  "Basic %s" % base64string


    req = urllib2.Request('http://localhost:8080/add_emp', data)
    req.add_header("Authorization", auth_header)
    try:
        resp = urllib2.urlopen(req)
    except urllib2.HTTPError, e:
        print e
        
else:
    for error in errors:
        print (error)





  