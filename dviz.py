# NOTE: NO SECURITY. You can add crap like a series name "<script>alert("!")</script>" and have bad things happen.
#

import webapp2

from handlers import addrandom
from handlers import admin
from handlers import delete
from handlers import detail
from handlers import graph
from handlers import list
from handlers import mainpage
from handlers import newseries
from handlers import push
from handlers import raw
from handlers import series
from handlers import user

app = webapp2.WSGIApplication([
  ('/', mainpage.MainPage),
  ('/user', user.User),
  ('/save-user', user.SaveUser),
  ('/raw/(.+)/(.+)', raw.RawData),
  ('/raw', raw.RawData),
  ('/list', list.List),
  ('/push', push.Push),
  ('/newseries', newseries.NewSeries),
  ('/random', addrandom.AddRandom),  # for testing only.
  ('/graph/(.+)', graph.Graph),
  ('/detail/(.+)/(.+)', detail.Detail),
  ('/s/(.+)', series.Series),
  ('/api/delete/user/(.+)', delete.DeleteUser),
  ('/api/delete/series/(.+)', delete.DeleteSeries),
  ('/admin', admin.Admin),
  ('/admin/users', admin.Users),
  ('/admin/user', admin.User)
  ])
