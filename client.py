#!/usr/bin/python
"Client library to add stuff to dviz."

import datetime
import sys
import time
import urllib
import urllib2

import util

QPS = 1.0/120

class DvizClient:
  def __init__(self, server='http://localhost:8080'):
    self._BASE_URL = server
    self._ADD_URL = '%s/push' % server
    self._MAX_BULK_ADD_SIZE = 200
    self._NUM_RETRIES = 5
    
  def add(self, series_name, value, timestamp=None, user_secret=None):
    data = {
      'series': series_name,
      'value': value,
      'timestamp': timestamp,
      'user_secret': user_secret,
      }
    return self._low_level_add(data)
    
  def bulk_add(self, series_name, timestamp_values, user_secret=None):
    """timestamp_values is a dictionary of timestamp, value pairs."""
    if len(timestamp_values) > self._MAX_BULK_ADD_SIZE:
      sys.stderr.write(
          'Bulk adding over %d values (%d). Not recommended.\n' % (
          self._MAX_BULK_ADD_SIZE, len(timestamp_values)))
    # TODO: split up into chunks and add individually instead of printing error.
    payload = '\n'.join('%s %s' % (util.to_seconds(t), v) for t, v in
        timestamp_values.iteritems())
    data = {
        'series': series_name,
        'payload': payload,
        'user_secret': user_secret,
        }
    return self._low_level_add(data)

  def _low_level_add(self, data):
    pdata = urllib.urlencode(data)
    req = urllib2.Request(self._ADD_URL, pdata)
    error = None
    for i in range(self._NUM_RETRIES):
      try:
        time.sleep(1.0/QPS)
        resp = urllib2.urlopen(req)
        return resp.read()
      except urllib2.HTTPError, e:
        error = e
        sys.stderr.write('Error: %s\n' % e)
    return error
  

if __name__ == '__main__':
  dc = DvizClient()
  value = datetime.datetime.now().second
  day = datetime.datetime(year=1979, month=6, day=28, hour=10, minute=42,
      second=12).strftime('%Y%m%d.%H%M.%S')
  print dc.add(series_name='from_ts', value=value, user_secret='foo',
      timestamp=day)

