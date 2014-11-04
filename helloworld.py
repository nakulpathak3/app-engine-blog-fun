import webapp2
import cgi
from date_validation import valid_year, valid_day, valid_month
from rot13 import *
from signup import *

form1="""
<form method="post">
	What is your birthday?
	<br>
	<label>
        Month
		<input type="text" name="month" value="%(month)s">
	</label>

	<label>	Day
		<input type="text" name="day" value="%(day)s">
	</label>

	<label> Year
	<input type="text" name="year" value="%(year)s">
	</label>
    <div style="color: red">%(error)s</div>
	<br>
	<input type="submit">
</form>
"""

class MainPage(webapp2.RequestHandler):

    def write_form(self, error="", month="", day="", year=""):
        self.response.out.write(form1 % {"error": error, "month": month, "day": day, "year": year})

    def get(self):
        self.response.out.write(form1)

    def post(self):
    	user_day = self.request.get('day')
    	user_month = self.request.get('month')
    	user_year = self.request.get('year')

        day = valid_day(user_day)
        month = valid_month(user_month)
        year = valid_year(user_year)

    	if not (year and month and day):
			self.write_form("Fuck you, enter properly bitch", user_day, user_month, user_year)
        else:
            self.redirect("/thanks")

class ThanksHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write("Thanks! That's a totally valid day!")


application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/thanks', ThanksHandler),
    ('/rot13', Rot13),
    ('/signup', SignUpHandler),
    ('/welcome', WelcomeHandler)
], debug=True)