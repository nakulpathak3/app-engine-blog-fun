import webapp2
import cgi

form2 = """<form method="post">

<textarea rows="18" cols="100" name="text">%(text)s</textarea>

<input type="submit" value="submit">
</form>"""

def rot_13(string):
    return string.encode("rot13")

def escape(s):
    return cgi.escape(s, quote=True)

class Rot13(webapp2.RequestHandler):
    def write_form2(self, s=""):
        self.response.out.write(form2 % {"text" :escape(s)})

    def get(self):
        self.write_form2()

    def post(self):
        user_input = self.request.get('text')
        code = rot_13(user_input)
        self.write_form2(code)