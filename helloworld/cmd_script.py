from optparse import OptionParser
from django.utils import simplejson as json
import urllib2

parser = OptionParser()
parser.add_option("-f","--first_name",dest="first_name")
parser.add_option("-l","--last_name",dest="last_name")
parser.add_option("-e","--e_mail",dest="e_mail")
parser.add_option("-s","--salary",dest="salary")
parser.add_option("-d","--first_date",dest="first_date")

(options, args) = parser.parse_args()

data = json.dumps({"first_name":options.first_name,
                   "last_name":options.last_name,
                   "e_mail":options.e_mail,
                   "salary":options.salary,
                   "first_date":options.first_date
                   })

req = urllib2.Request('/createemployee', data)




  