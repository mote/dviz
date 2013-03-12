import data
from google.appengine.api import users

from handlers import base

class Detail(base.Base):
  def get(self, timerange, names):
    template_values = {
      'user': users.get_current_user(),
      'timerange': timerange,
      'series': names,
      'all_timeranges': ['hour', 'day', 'week', 'month', 'year', 'all'],
    }
    # only get first. will need to get them all, later.
    latest = data.get_latest_value(names.split(',')[0])
    if latest:
      template_values['latest_val'] = latest.value
      template_values['latest_ts'] = latest.timestamp
    else:
      template_values['latest_val'] = 'NaN'
      template_values['latest_ts'] = 'NaN'

    self.render('detail.html', template_values)
