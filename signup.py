import webapp2
import logging
import re

form="""
    <form method="post">
    Signup
    <br>
    <label> Username:
    <input type="text" name="username" value="%(username)s">
    </label>
    <br>
    <label> Password:
    <input type="password" name="password" value="%(password)s">
    </label>
    <br>
    <label> Verify Password:
    <input type="password" name="verify" value="%(verify)s">
    </label>
    <br>
    <label> Email(optional):
    <input type="text" name="email" value="%(email)s">
    </label>
    <br>
    <input type="submit">
    </form>"""

class SignUpHandler(webapp2.RequestHandler):
    def load_form(self,username="",password="",verify="",email=""):
        self.response.write(form % {"username": username, "password": password, "verify": verify, "email": email})

    def get(self):
        self.load_form()

    def post(self):
        logging.error("Data set submitted.")
        username = self.request.get("username")
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")
        if(self.valid_str(username) and self.valid_str(password) and self.valid_str(verify) and password == verify):
            self.redirect('/welcome?user=' + username)
        else:
            self.load_form(username, password, verify, email)

    def valid_str(self,str):
        logging.error("Is " + str + " valid?")
        if re.match(r'^[A-Za-z0-9_]+$', str):
            logging.error(str + " was valid.")
            return True
        else:
            logging.error(str + " was invalid.")
            return False

class WelcomeHandler(webapp2.RequestHandler):
    def get(self):
        logging.error("Welcome Page Opened with username:" + self.request.get("user") +".")
        self.response.write("Welcome, "+ self.request.get("user"))
