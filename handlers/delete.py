import webapp2
from google.appengine.api import users

import data

class DeleteUser(webapp2.RequestHandler):
  def get(self, user_id):
    try:
      data.delete_user(user_id)
      self.response.out.write('Deleted user %s.' % user_id)
    except UserException:
      self.response.out.write('Problem removing user %s.' % user_id)

class DeleteSeries(webapp2.RequestHandler):
  def get(self, series_name):
    # TODO: later, pass in user secret as option here.
    # For starters, only delete stuff that we own.
    current_user = users.get_current_user()
    if not current_user:
      self.response.out.write("Can't delete anything without a user.")
    count = data.delete_series(series_name, current_user.user_id())
    self.response.out.write('Deleted %d items from %s' % (count, series_name))


