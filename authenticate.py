import webapp2
import re  # regular expressions

from hashing import *
from templates import *


USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASS_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")


def valid_name(name):
    return USER_RE.match(name)


def valid_email(email):
    return EMAIL_RE.match(email)


def valid_password(password):
    return PASS_RE.match(password)


class SignupHandler(webapp2.RequestHandler):
    def write_form(self, name='', email='', name_error='',
                   password_error='', verify_error='', email_error=''):

        template = jinja_environment.get_template('signup.html')
        self.response.out.write(template.render({'name': name, 'email': email,
                                                 'name_error': name_error,
                                                 'password_error': password_error,
                                                 'verify_error': verify_error,
                                                 'email_error': email_error}))

    def get(self):
        self.write_form()

    def post(self):
        user_name = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        user_email = self.request.get('email')

        if user_name and valid_name(user_name):
            name_error = ''
        else:
            name_error = "please only use letters and numbers"

        if password and valid_password(password):
            password_error = ''
        else:
            password_error = "not valid"

        if verify and password and password == verify:
            verify_error = ''
        else:
            verify_error = "passwords don't match"

        email_error = ''
        if user_email:
            if not valid_email(user_email):
                email_error = "that's not a valid email"

        if not password_error and not email_error and not name_error and not verify_error:
            # no error so save user in DB, write to cookie and redirect to welcome page

            cookie = str('name=%s' % make_secure_val(user_name))
            self.response.headers.add_header('Set-Cookie', cookie)

            self.redirect('/welcome')

        else:
            # errors found go back to form and tell user where the problem was
            self.write_form(user_name, user_email, name_error, password_error,
                            verify_error, email_error)

welcome = """
<!DOCTYPE html>
<html>
  <head>
    <title>Unit 2 Signup</title>
  </head>

  <body>
    <h2>Welcome, %(name)s!</h2>
  </body>
</html>
"""


class WelcomeHandler(webapp2.RequestHandler):
    def get(self):
        user_name_cookie = self.request.cookies.get('name', None)
        user_name = check_secure_val(user_name_cookie)
        if user_name:
            self.response.out.write(welcome % {'name': user_name})
        else:
            self.redirect('/signup')
