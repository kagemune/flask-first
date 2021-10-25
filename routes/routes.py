from controllers.controller import *
from controllers.errors import *


routes = {
    #'':'','':as_view(),
    'ind_rut':'/','ind_cont':indexController.as_view('index'),
    'log_rut':'/login','log_cont':loginController.as_view('login'),
    'reg_rut':'/registrarse','reg_cont': registerController.as_view('registrarse'),
    'con_rut':'/contacto','con_cont': contactController.as_view('contacto'),
    'pro_rut':'/producto','pro_cont': productController.as_view('producto'),
    'car_rut':'/carrito','car_cont': carController.as_view('carrito'),
    'creaPro_rut':'/crearproducto','creaPro_cont': crearProductoController.as_view('crearproducto'),
    
    
    # pagina de error 404 
    'notFound_route': 404, 'not_found_cont':notFoundController.as_view('error')
}
