import datetime

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


def parse_time(timestamp_str):
  for format_str in TIME_FORMATS:
    try:
      return datetime.datetime.strptime(timestamp_str, format_str)
    except ValueError, e:
      pass
  return datetime.datetime.now()


def has_value(s):
  if not s:
    return False
  if s == 'None':
    return False
  return True
  
def to_seconds(timestamp):
  if isinstance(timestamp, str):
    timestamp = parse_time(timestamp)
  return timestamp.strftime('%s')

def from_seconds(time_seconds):
  return datetime.datetime.utcfromtimestamp(int(time_seconds))
