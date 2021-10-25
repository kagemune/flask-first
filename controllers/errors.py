from flask.views import MethodView
from flask import render_template

class notFoundController(MethodView):
    def get(self,error):
        return render_template("error.html", error=error)