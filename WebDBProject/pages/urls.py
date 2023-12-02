from django.urls import path
from . import views 

#urls del proyecto
urlpatterns = [
    path('', views.index, name="index"),

    path('perfil/<int:usuario_id>', views.userPerfil, name="perfil"),   
    path('home/<int:usuario_id>', views.home, name="home"),   
    path('carrito/<int:usuario_id>', views.carrito, name="carrito"),
    path('crearSoporte/<int:usuario_id>', views.crearSoporte, name="crearSoporte"),
    path('editarProducto/<int:usuario_id>', views.editarProducto, name="editarProducto"),

    path('uRecibo/<int:usuario_id>', views.uRecibo, name="uRecibo"),
    path('uSoporte/<int:usuario_id>', views.uSoporte, name="uSoporte"),
    path('uProducto/<int:usuario_id>', views.uProducto, name="uProducto"),

]
