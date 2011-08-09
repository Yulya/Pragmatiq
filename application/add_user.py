import json
from optparse import OptionParser
import urllib2


parser = OptionParser()
parser.add_option("-n","--name",dest="username")
parser.add_option("-p","--password",dest="password")
(options, args) = parser.parse_args()

data = json.dumps({"username":options.username,
                   "password":options.password})

req = urllib2.Request('http://localhost:8080/add_usr', data)
resp = urllib2.urlopen(req)
print resp.read()
  