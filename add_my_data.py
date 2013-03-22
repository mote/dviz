import os
import time

import client



FITBIT_STEPS_DIR = '/home/mote/logs/fitbit/steps/'

def load_file(f):
  for line in open(f):
    line = line.strip()
    t, v = line.split(',')
    yield t, v

def main():
  c = client.DvizClient(server='http://mote-dviz.appspot.com/push')
  secret = 'sekrit'
  series = 'fitbit_steps'
  total = 0
  for f in os.listdir(FITBIT_STEPS_DIR):
    f = os.path.join(FITBIT_STEPS_DIR, f)
    print 'adding file', f
    for t, v in load_file(f):
      c.add(series_name=series, value=v, user_secret=secret, timestamp=t)
      time.sleep(2)
      total += 1
      if total % 500 == 1:
        print '\ttotal', total




if __name__ == '__main__':
  main()

