from optparse import OptionParser
import json
import urllib2
import re
import datetime

parser = OptionParser()
parser.add_option("-f","--first_name",dest="first_name")
parser.add_option("-l","--last_name",dest="last_name")
parser.add_option("-e","--e_mail",dest="e_mail")
parser.add_option("-s","--salary",dest="salary")
parser.add_option("-d","--first_date",dest="first_date")

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
except:
    errors.append('enter correct date in form dd-mm-YY. ')

if not errors:
    data = json.dumps({"first_name":options.first_name,
                   "last_name":options.last_name,
                   "e_mail":options.e_mail,
                   "salary":options.salary,
                   "first_date":options.first_date
                   })
    
    req = urllib2.Request('http://localhost:8080/add_emp', data)
    resp = urllib2.urlopen(req)
    print resp.read()
else:
    for error in errors:
        print (error)




  