import webapp2
import cgi
import re

# **************************************************************** Unit 2/rot13
rot13 = """
<!DOCTYPE html>
<html>
  <head>
    <title>Unit 2 Rot 13</title>
  </head>

  <body>
    <h2>Enter some text to ROT13:</h2>
    <form method="post">
      <textarea name="text" style="height: 100px; width: 400px;">%(usertext)s
      </textarea>
      <br>
      <input type="submit">
    </form>
  </body>
</html>
"""


class RotHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write(rot13 % {'usertext': ''})

    def post(self):
        user_data = self.request.get('text')
        if user_data:
            rot = user_data.encode('rot13')
            rot = cgi.escape(rot, quote=True)
        self.response.out.write(rot13 % {'usertext': rot})


# *************************************************************** Unit 2/signup

form = """
<!DOCTYPE html>
<html>
  <head>
    <title>Sign Up</title>
    <style type="text/css">
      .label {text-align: right}
      .error {color: red}
    </style>

  </head>
  <body>
    <h2>Signup</h2>
    <form method="post">
      <table>
        <tr>
          <td class="label">
            Username
          </td>
          <td>
            <input type="text" name="username" value="%(name)s">
          </td>
          <td class="error">
            %(name_error)s
          </td>
        </tr>

        <tr>
          <td class="label">
            Password
          </td>
          <td>
            <input type="password" name="password" value="">
          </td>
          <td class="error">
          %(password_error)s
          </td>
        </tr>

        <tr>
          <td class="label">
            Verify Password
          </td>
          <td>
            <input type="password" name="verify" value="">
          </td>
          <td class="error">
            %(verify_error)s
          </td>
        </tr>

        <tr>
          <td class="label">
            Email (optional)
          </td>
          <td>
            <input type="text" name="email" value="%(email)s">
          </td>
          <td class="error">
            %(email_error)s
          </td>
        </tr>
      </table>

      <input type="submit">
    </form>
  </body>
</html>
"""

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

        self.response.out.write(form % {'name': name, 'email': email,
                                        'name_error': name_error,
                                        'password_error': password_error,
                                        'verify_error': verify_error,
                                        'email_error': email_error})

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
            # no error so redirect to welcome page
            self.redirect('/unit2/welcome?username=%s' % user_name)
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
        user_name = self.request.get('username')
        self.response.out.write(welcome % {'name': user_name})
