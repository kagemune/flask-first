from flask import Flask,g
from db import close_db
from routes.routes import *
import os


app = Flask(__name__)
app.config.from_mapping(
    SECRET_KEY="development"
)
UPLOAD_FOLDER = '/static/img/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 

#rutas de la aplicacion
app.add_url_rule(routes["ind_rut"], view_func=routes["ind_cont"])
app.add_url_rule(routes["log_rut"], view_func=routes["log_cont"])
app.add_url_rule(routes["reg_rut"], view_func=routes["reg_cont"])
app.add_url_rule(routes["pro_rut"], view_func=routes["pro_cont"])
app.add_url_rule(routes["con_rut"], view_func=routes["con_cont"])
app.add_url_rule(routes["car_rut"], view_func=routes["car_cont"])
app.add_url_rule(routes["creaPro_rut"], view_func=routes["creaPro_cont"])

#ruta del 404
app.register_error_handler(routes['notFound_route'],routes['not_found_cont'])


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


@app.before_request
def load_logged_in_user():
    username = session.get('username') #get es para devolver valores de un diccionario
    #print('entro a app.before_request')
    if username is None:
        g.user = None
        #print('g.user : ',g.user)
    else: #trae una tupla
        g.user = get_db().execute( 
            'SELECT * FROM Usuario_final WHERE nombre= ?',(username,)
        ).fetchone()
        g.rol = g.user[6]


    






if  __name__ == "__main__":
    os.environ['FLASK_ENV'] = 'development'
    app.run(debug=True)