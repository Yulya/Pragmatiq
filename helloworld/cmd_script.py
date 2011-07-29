from optparse import OptionParser
import json
import urllib2

parser = OptionParser()
parser.add_option("-f","--first_name",dest="first_name")
parser.add_option("-l","--last_name",dest="last_name")
parser.add_option("-e","--e_mail",dest="e_mail")
parser.add_option("-s","--salary",dest="salary")
parser.add_option("-d","--first_date",dest="first_date")

(options, args) = parser.parse_args()
errors = []
if not options.first_name.isalpha():
    errors.append('enter correct first name. ')
if not options.first_name.isalpha():
    errors.append('enter correct last name. ')
if not options.salary.isdigit():
    errors.append('enter correct salary. ')
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
else: print(errors)




  