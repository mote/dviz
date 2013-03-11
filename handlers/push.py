# NOTE: NO SECURITY. You can add crap like a series name "<script>alert("!")</script>" and have bad things happen.
#

import sys
import datetime
import data

from google.appengine.api import users

from handlers import base

# Different possbilities for parseing timestamp strings.
TIME_FORMATS = [
    '%Y-%m-%d %H:%M:%S',
    '%Y/%m/%d %H:%M:%S',
    '%Y.%m.%d.%H%M.%S',
    '%Y%m%d.%H%M.%S',
    '%Y%m%d%H%M%S',
    '%Y%m%d%H%M%S',
    '%Y%m%d.%H%M',
    '%Y.%m%d.%H%M',
    '%Y%m%d%H%M',
    '%Y/%m/%d',
    ]

def has_value(s):
  if not s:
    return False
  if s == 'None':
    return False
  return True
  

class Push(base.Base):
  def get(self):
    self.post()

  def post(self):
    user_secret = self.request.get('user_secret')
    try:
      user = users.get_current_user()
      user_id = user.user_id()
    except:
      user_id = None

    series = self.request.get('series')
    value = float(self.request.get('value'))
    timestamp_str = self.request.get('timestamp')
    timems = self.request.get('timems')
    if not has_value(timestamp_str):
      if has_value(timems):
        time_seconds = float(timems) / 1000
        timestamp = datetime.datetime.utcfromtimestamp(time_seconds)
    else:
      for format_str in TIME_FORMATS:
        try:
          timestamp = datetime.datetime.strptime(timestamp_str, format_str)
          break
        except ValueError, e:
          pass
    if not timestamp:
      timestamp = datetime.datetime.now()
    data.add(name=series, value=value, timestamp=timestamp, user_id=user_id,
        secret=user_secret)
    self.response.out.write('Added: %s, %s, %s\n' % (
      series, value, timestamp))
