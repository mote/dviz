# NOTE: NO SECURITY. You can add crap like a series name "<script>alert("!")</script>" and have bad things happen.
#

import sys
import datetime

from google.appengine.api import users

import data
import util
from handlers import base


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
    value = self.request.get('value')
    payload = self.request.get('payload')
    if value:
      value = float(value)
      timestamp_str = self.request.get('timestamp')
      timems = self.request.get('timems')
      status = self.single_add(timestamp_str, timems, series, value, user_id,
          user_secret)
    elif payload:
      status = self.bulk_add(payload, series, user_id, user_secret)
    else:
      status = 'Must specify either value or payload.'
    self.response.out.write(status)

  def single_add(self, timestamp_str, timems, series, value, user_id,
      user_secret):
    if not util.has_value(timestamp_str):
      if util.has_value(timems):
        time_seconds = float(timems) / 1000
        timestamp = util.from_seconds(time_seconds)
      else:
        timestamp = datetime.datetime.now()
    else:
      timestamp = util.parse_time(timestamp_str)
    data.add(name=series, value=value, timestamp=timestamp, user_id=user_id,
        secret=user_secret)
    return 'Added: %s, %s, %s\n' % (series, value, timestamp)
   
  def bulk_add(self, payload, series, user_id, user_secret):
    total = 0
    for item in payload.split('\n'):
      total += 1
      time_seconds, value = item.split(' ')
      timestamp = util.from_seconds(time_seconds)
      value = float(value)
      data.add(name=series, value=value, timestamp=timestamp, user_id=user_id,
          secret=user_secret)
    return 'Added %d items to %s' % (total, series)

