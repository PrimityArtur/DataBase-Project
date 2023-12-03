from django.shortcuts import redirect, render #render para ir a un html, y redirect  para redireccionar a un html
from django.http import HttpResponse, JsonResponse
from django.db import connection #para optener cursor y realizar consultas SQL
# from .forms import CreateNewSoport

def index(request):
    
    return render(request, 'index.html')


def home(request, usuario_id=None):
    cursor = connection.cursor().execute("""
            SELECT 
                p.PRODUCTO_ID,
                p.NOMBRE,
                p.PRECIO,
                t.TIPO,
                AVG(val.ESTRELLAS) AVG_ESTRELLAS,
                AVG(d.COMPRADOR_ID) AVG_DESCARGAS,
                vu.NOMBRE

            FROM PRODUCTO p 
            JOIN TIPO t 
            ON (p.PRODUCTO_ID = t.PRODUCTO_ID)
            JOIN DESCARGA d 
            ON (p.PRODUCTO_ID = d.PRODUCTO_ID)
            JOIN VALORACION val
            ON (p.PRODUCTO_ID = val.PRODUCTO_ID)
            JOIN USUARIO vu
            ON (p.PRODUCTO_ID = vu.USUARIO_ID)

            GROUP BY p.PRODUCTO_ID, p.NOMBRE, p.PRECIO, t.TIPO, vu.NOMBRE
        """)
    
    resultados = cursor.fetchall()    
    Productos = [{
            'producto_id': producto_id, 
            'nombre': nombre, 
            'precio': precio,
            'tipo' : tipo,
            'estrellas' : estrellas,
            'descargas' : descargas,
            'vendedor' : vendedor
            } 
            for producto_id, nombre, precio, tipo, estrellas, descargas, vendedor in resultados]
    
    return render(request, 'index.html', {'productos': Productos, 'usuario_id': usuario_id})


def navBar(request, usuario_id):
    return render(request, 'layouts/navbar.html', {'usuario_id': usuario_id})


def userPerfil(request, usuario_id):

    cursor = connection.cursor().execute("""
        SELECT 
            u.NOMBRE,
            u.APELLIDO,
            u.CORREO,
            u.FCHA_RGSTRO,
            p.DIRECCION,
            p.TELEFONO,
            p.FOTO
        FROM USUARIO u JOIN PERFIL p 
        ON (u.USUARIO_ID = p.USUARIO_ID)
        WHERE u.USUARIO_ID = :usuario_id       
        """, {'usuario_id': usuario_id})

    resultados = cursor.fetchall()

    # Crear una lista de diccionarios con los nombres y apellidos
    nombres = [{'nombre': nombre, 
                'apellido': apellido,
                'correo' : correo,
                'fcha_rgstro' : fcha_rgstro,
                'direccion' : direccion,
                'telefono' : telefono,
                'foto' : foto
                } 
               for nombre, apellido, correo, fcha_rgstro, direccion, telefono, foto in resultados]

    return render(request, 'user/userPerfil.html', 
                  {'nombres': nombres, 'usuario_id': usuario_id})


def carrito(request, usuario_id):
    return render(request, 'shop/carrito.html', {'usuario_id': usuario_id})


def crearSoporte(request, usuario_id):
    return render(request, 'user/crearSoporte.html', {'usuario_id': usuario_id})


def uRecibo(request, usuario_id):
    return render(request, 'user/userRecibo.html', {'usuario_id': usuario_id})


def uSoporte(request, usuario_id):
    return render(request, 'user/userSoporte.html', {'usuario_id': usuario_id})


def uProducto(request, usuario_id):
    return render(request, 'user/userProducto.html', {'usuario_id': usuario_id})


def editarProducto(request, usuario_id):
    return render(request, 'user/editarProducto.html', {'usuario_id': usuario_id})


def producto(request, usuario_id, producto_id):
    cursor = connection.cursor().execute("""
    SELECT 
        p.PRODUCTO_ID,
        p.NOMBRE,
        p.DESCRIPCION,
        p.PRECIO,
        p.FECHA,
        t.TIPO,
        plu.VERSION,
        sch.DIMENSIONES,                                         
        val.ESTRELLAS,
        vu.NOMBRE

    FROM PRODUCTO p 
    JOIN TIPO t 
    ON (p.PRODUCTO_ID = t.PRODUCTO_ID)
    JOIN PLUGIN plu 
    ON (t.TIPO_ID = plu.TIPO_ID)
    JOIN SCHEMATIC sch 
    ON (t.TIPO_ID = sch.TIPO_ID)
    JOIN VALORACION val
    ON (p.PRODUCTO_ID = val.PRODUCTO_ID)
    JOIN USUARIO vu
    ON (p.PRODUCTO_ID = vu.USUARIO_ID)
    """)
    
    resultados = cursor.fetchall()    
    Productos = [{
            'producto_id': producto_id, 
            'nombre': nombre, 
            'precio': precio,
            'tipo' : tipo,
            'estrellas' : estrellas,
            'vendedor' : vendedor
            } 
            for producto_id, nombre, precio, tipo, estrellas, vendedor in resultados]
    
    return render(request, 'shop/producto.html', {'productos': Productos, 'usuario_id': usuario_id})


def pago(request, usuario_id):
    return render(request, 'shop/pago.html', {'usuario_id': usuario_id})


def soporteRespuestas(request, usuario_id):
    return render(request, 'user/soporteRespuestas.html', {'usuario_id': usuario_id})