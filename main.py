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
import cgi
import re

form = """
<!DOCTYPE html>
<html>
    <head>
        <title>Sign-Up</title>
        <style>
            .error {
                color: red;
            }
        </style>
    </head>
    <body>
        <h1>Sign-Up</h1>
        <form method="post">
            <table>
                <tbody>
                    <tr>
                        <td>
                            <label>Username</label>
                        </td>
                        <td>
                            <input name="username" type="text" value="%(username)s">
                            <span class="error">%(username_error)s</span>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <label>Password</label>
                        </td>
                        <td>
                            <input name="password" type="password">
                            <span class="error">%(valid_password_error)s</span>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <label>Verify Password</label>
                        </td>
                        <td>
                            <input name="verify-password" type="password">
                            <span class="error">%(password_match_error)s</span>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <label>Email (optional)</label>
                        </td>
                        <td>
                            <input name="email" type="text" value="%(email)s">
                            <span class="error">%(email_error)s</span>
                        </td>
                    </tr>
                </tbody>
            </table>
            <input type="submit">
        </form>
    </body>
</html>
"""

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    if not USER_RE.match(username):
        return False
    else:
        return True

PASSWORD_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    if not PASSWORD_RE.match(password):
        return False
    else:
        return True

EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
def valid_email(email):
    if not EMAIL_RE.match(email):
        return False
    else:
        return True


class MainHandler(webapp2.RequestHandler):

    def write_form(self, username_error="", valid_password_error="", password_match_error="", email_error="", username="", email=""):
        #get user inputs for username and email for sake of preserving user's input if form is rerendered
        user_username = self.request.get("username")
        user_email = self.request.get("email")

        username = cgi.escape(user_username, quote=True)
        email = cgi.escape(user_email, quote=True)

        self.response.write(form % {"username_error": username_error,
                                    "valid_password_error": valid_password_error,
                                    "password_match_error": password_match_error,
                                    "email_error": email_error,
                                    "username": username,
                                    "email":email})

    def get(self):
        self.write_form()

    def post(self):
        #get user inputs
        user_username = self.request.get("username")
        user_password = self.request.get("password")
        user_verify_input = self.request.get("verify-password")
        user_email = self.request.get("email")

        #html escape user inputs
        username = cgi.escape(user_username, quote=True)
        password = cgi.escape(user_password, quote=True)
        verify_input = cgi.escape(user_verify_input, quote=True)
        email = cgi.escape(user_email, quote=True)

        #check if valid username
        username_error = ""
        if valid_username(username) == False:
            username_error="Username not valid."

        #check if valid password
        valid_password_error = ""
        if valid_password(password) == False:
            valid_password_error="Password not valid."

        #check if password and verify password are the same
        password_match_error = ""
        if password != verify_input:
            password_match_error="Your passwords didn't match."

        #check if valid email address
        email_error = ""
        if email and valid_email(email) == False:
            email_error="Email address not valid."

        #if everything valid, go to welcome page
        if username_error or valid_password_error or password_match_error or email_error:
            self.write_form(username_error, valid_password_error, password_match_error, email_error)
        else:
            self.redirect("/welcome/?username=%(username)s" % {"username":username})


class WelcomeHandler(webapp2.RequestHandler):
    def get(self):
        username = self.request.get("username")
        self.response.write("Welcome " + username + "!")


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/welcome/', WelcomeHandler)
], debug=True)
