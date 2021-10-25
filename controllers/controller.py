import os
from sqlite3.dbapi2 import connect
from flask.views import MethodView
from flask import render_template,request,redirect,flash,jsonify,session,g
from db import get_db
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename, send_from_directory

UPLOAD_FOLDER = '/static/img/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


class indexController(MethodView):
    def get(self):
        if "username" in session:
            return render_template("index.html")
        else:
            return redirect("/login")
        
class contactController(MethodView):
    def get(self):
        return render_template("contacto.html")

class productController(MethodView):
    
    def get(self):
        if "username" in session:
            name = request.args.get("prod1","batido")
            db = get_db()
            comentarios = db.execute("SELECT * FROM comentarios ")
            producto = db.execute("SELECT* FROM productos WHERE nombre=?",(name,)).fetchone()
            g.data = comentarios.fetchall()
            prod = producto[2]
            prod2 = producto[3]
            return render_template("producto.html", data= g.data,productos=prod,prod2=prod2)
        else:
            return redirect ("/login")
    def post(self):
        try:
                user = session.get("username")
                comentario = request.form["comentario"]
                producto = 3
                calificacion=request.form["estrellas"]
                db= get_db()
                db.execute('INSERT INTO comentarios(username,comentario,producto,calificacion) VALUES(?,?,?,?)',(user,comentario,producto,calificacion))
                db.commit()
                return redirect("producto")        
        except:
            flash("no se guardo el comentario","error")
            return redirect("producto") 
    

class registerController(MethodView):
    
    def get(self):
        if "username" in session:
            return redirect("/")
        else:
            return render_template("registrarse.html")
    
    def post(self):
        
        try:
            nombre = request.form["nombre"]
            correo = request.form["correo"]
            telefono = request.form["telefono"]
            contraseña =request.form["contraseña"]
            date = request.form["date"]
            db= get_db()
            db.execute('INSERT INTO Usuario_final(nombre,correo,telefono,contrasena,fecha,rol_id) VALUES(?,?,?,?,?,?)',(nombre,correo,telefono,generate_password_hash(contraseña),date,3))
            db.commit()
            flash("la informacion se ingresado con exito","success")
            return redirect("/")
        except:
            flash("un error ha ocurrido ","error")
            return render_template("registrarse.html")
    
class loginController(MethodView):
    def get(self):
        if "username" in session:
            return redirect("/")
        else:
            return render_template ("login.html")
    
    def post(self):
        try:
            correo = request.form["Email"]
            contraseña = request.form["password"]
            db= get_db()
            user = db.execute(
                "SELECT * FROM Usuario_final WHERE correo=?",(correo,)
                ).fetchone()
            
            dbpass = user[4]
            valPassword = check_password_hash(dbpass,contraseña)
            
            #print(valPassword)
            #print(user[6])
            
            if user is None:
                flash("usuario o contraseña incorrectos ","error")
                return redirect("/login")
            else :
                if user[6] == 3 and valPassword == True:
                    session["username"]= user[1]
                    return redirect("/")
        except:
            flash("un error ha ocurrido no try ","error")
            return redirect("/login")

class carController(MethodView):
    
    def get(self):
        if "username" in session:
            return render_template("carrito_de_compra.html")
        else:
            return render_template("login.html") 
    #def post(self)
    
def allowed_file(filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
def ruta(filename):
    return send_from_directory(os.getcwd() + UPLOAD_FOLDER ,filename=filename , as_attachment=False)            

class crearProductoController(MethodView):
    def get(self):
        try:
            if g.rol == 3:
                return render_template("crearProducto.html")
        except:
            return redirect("/")
    def post(self):
        if g.rol == 3:
            try:    
                if "file" not in request.files:
                    flash("no hay archivo","error")
                    return render_template("crearProducto.html")
                file = request.files["file"]
                nombre = request.form["nombre"]
                descripcion = request.form["descripcion"]
                if file.filename=="":
                    flash("no hay archivo correcto","error")
                    return render_template("crearProducto.html")
                if file.filename and allowed_file(file.filename):
                    
                    filename = secure_filename(file.filename)
                    file.save(os.getcwd()+UPLOAD_FOLDER + filename)
                    filename1 = UPLOAD_FOLDER + filename
                    db= get_db()
                    db.execute (
                        'INSERT INTO productos(nombre,descripcion,filename) VALUES(?,?,?)',(nombre,descripcion,filename1)
                        )
                    db.commit()
                    flash("producto creado","success")
                    return redirect("/crearproducto") 
                else:
                    flash("problema en file","error" )
                    return redirect("/crearproducto")
                
            except:
                flash("no creado","error")
                return redirect("/crearproducto")