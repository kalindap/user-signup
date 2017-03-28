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

form = """
<!DOCTYPE html>
<html>
    <head>
        <title>User Sign-Up</title>
    </head>
    <body>
        <h1>Sign-Up</h1>
        <form>
            <label>Username
            <input name="username" type="text">
            </label>
            <br>
            <label>Password
            <input name="password" type="text">
            </label>
            <br>
            <label>Verify Password
            <input name="verify-password" type="text">
            </label>
            <br>
            <label>Email (optional)
            <input name="email" type="text">
            </label>
            <br>
            <input type="submit">
        </form>
    </body>
</html>
"""

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write(form)

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
