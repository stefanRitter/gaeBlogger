#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2

from unit2 import *
from blog import *

form = """
<form method="post">
  <input type="text" name="day">
  <input type="text" name="month">
  <input type="text" name="year">
  <br>
  <br>
  <div style="color:red">%(error)s</div>
  <input type="submit">
</form>
"""


class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.redirect('/blog')


app = webapp2.WSGIApplication([
    ('/', MainHandler), ('/unit2/rot13', RotHandler),
    ('/unit2/signup', SignupHandler), ('/unit2/welcome', WelcomeHandler),
    ('/blog', BlogHandler), ('/blog/newpost', NewPostHandler), ('/blog/([0-9]+)', PostHandler)
], debug=True)

#class TestHandler(webapp2.RequestHandler):
#    def post(self):
#        q = self.request.get('q')
#        self.response.write(q)
#
#        #self.response.headers['Content-Type'] = 'text/plain'
#        #self.response.out.write(self.request)
