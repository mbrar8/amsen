from datetime import datetime
import urllib2
import urllib
import json


class API:

  def __init__(self):
    #connect to the remote server
    self.baseUrl= 'https://blooming-hollows-23779.herokuapp.com/dbl'

  def push(self, pos, env):
       env['x']=pos.x
       env['y']=pos.y
       dict_json = json.dumps(env)
       now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
       print "pushing with date time : " + now
       args = 'time=' + urllib.quote_plus(now)
       args += '&reading='+ urllib.quote_plus(dict_json)
       url = self.baseUrl + '?' + args
       print url
       response = urllib2.urlopen(url)
       result = response.read()
       print result


