from django.shortcuts import redirect, render #render para ir a un html, y redirect  para redireccionar a un html
from django.http import HttpResponse, JsonResponse
from django.db import connection #para optener cursor y realizar consultas SQL
from . import forms 

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
                COUNT(d.COMPRADOR_ID) AVG_DESCARGAS,
                vu.NOMBRE

            FROM PRODUCTO p 
            JOIN TIPO t 
            ON (p.PRODUCTO_ID = t.PRODUCTO_ID)
            JOIN DESCARGA d 
            ON (p.PRODUCTO_ID = d.PRODUCTO_ID)
            JOIN VALORACION val
            ON (p.PRODUCTO_ID = val.PRODUCTO_ID)
            JOIN VENDEDOR ven
            ON (p.VENDEDOR_ID = ven.VENDEDOR_ID)
            JOIN USUARIO vu
            ON (ven.USUARIO_ID = vu.USUARIO_ID)

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
    cursor = connection.cursor().execute("""
        SELECT 
            p.PRODUCTO_ID,
            p.NOMBRE,
            p.PRECIO,
            t.TIPO
                                
        FROM USUARIO u 
        JOIN COMPRADOR com 
        ON (u.USUARIO_ID = com.USUARIO_ID)
        JOIN CARRITO car 
        ON (com.COMPRADOR_ID = car.COMPRADOR_ID)
        JOIN PRDCTO_CRRTO pcar 
        ON (car.CARRITO_ID = pcar.CARRITO_ID)
        JOIN PRODUCTO p 
        ON (pcar.PRODUCTO_ID = p.PRODUCTO_ID)
        JOIN TIPO t 
        ON (p.PRODUCTO_ID = t.PRODUCTO_ID)

        WHERE u.USUARIO_ID = :usuario_id AND car.CARRITO_ID = (SELECT 
                        MAX(fcar.CARRITO_ID)
                    FROM CARRITO fcar
                    WHERE fcar.COMPRADOR_ID = com.COMPRADOR_ID)
                                         
     """, {'usuario_id' : usuario_id})
    
    resultados = cursor.fetchall()
    carrito = [{
        'producto_id' : producto_id,
        'nombre' : nombre ,
        'precio' : precio,
        'tipo' : tipo
    } for producto_id, nombre, precio, tipo in resultados]

    return render(request, 'shop/carrito.html', {
    'usuario_id': usuario_id,
    'carrito': carrito
    })


def crearSoporte(request, usuario_id):

    if request.method == 'GET':
        #show interface
        form = forms.CreateNewSoport()
    
        return render(request, 'user/crearSoporte.html', 
                  {'form': form, 'usuario_id': usuario_id})
    
    elif request.method == 'POST':
        form = forms.CreateNewSoport(request.POST)
        if form.is_valid():
            mensaje = form.cleaned_data['mensaje']

            cursor = connection.cursor().execute("""
                INSERT INTO SOPORTE (MENSAJE, USUARIO_ID) 
                VALUES (:1, :2)""", 
                {'1': mensaje, '2': usuario_id})
            
            cursor = connection.cursor().execute("""
                SELECT 
                    s.SOPORTE_ID,
                    s.MENSAJE,
                    s.FECHA
                                                
                FROM USUARIO u 
                JOIN SOPORTE s 
                ON (u.USUARIO_ID = s.USUARIO_ID)

                WHERE u.USUARIO_ID = :usuario_id                  
            """, {'usuario_id' : usuario_id})
            
            resultados = cursor.fetchall()
            soportes = [{
                'soporte_id' : soporte_id,
                'mensaje' : mensaje,
                'fecha' : fecha
            } for soporte_id, mensaje, fecha in resultados]

            return render(request, 'user/userSoporte.html', {
                'usuario_id': usuario_id,
                'soportes': soportes
                })
        
    return render(request, 'user/crearSoporte.html', 
                  {'form': form, 'usuario_id': usuario_id})


def uRecibo(request, usuario_id):

    cursor = connection.cursor().execute("""
            SELECT 
                r.RECIBO_ID,
                r.FECHA,
                pag.TOTAL,
                mp.NOMBRE
                                         
            FROM USUARIO u 
            JOIN COMPRADOR com 
            ON (u.USUARIO_ID = com.USUARIO_ID)
            JOIN RECIBO r 
            ON (com.COMPRADOR_ID = r.COMPRADOR_ID)
            JOIN PAGO pag 
            ON (r.PAGO_ID = pag.PAGO_ID)
            JOIN METODO_PAGO mp 
            ON (pag.METODO_PAGO_ID = mp.METODO_PAGO_ID)

            WHERE u.USUARIO_ID = :usuario_id
                                         
     """, {'usuario_id' : usuario_id})
    
    resultados = cursor.fetchall()
    recibos = [{
        'recibo_id' : recibo_id,
        'fecha' : fecha,
        'total' : total,
        'metodo_pago' : metodo_pago,
    } for recibo_id, fecha, total, metodo_pago in resultados]

    cursor = connection.cursor().execute("""
        SELECT 
            r.RECIBO_ID,
            p.NOMBRE,
            p.PRECIO,
            pcar.CANTIDAD
                                    
        FROM USUARIO u 
        JOIN COMPRADOR com 
        ON (u.USUARIO_ID = com.USUARIO_ID)
        JOIN CARRITO car 
        ON (com.COMPRADOR_ID = car.COMPRADOR_ID)
        JOIN PRDCTO_CRRTO pcar 
        ON (car.CARRITO_ID = pcar.CARRITO_ID)
        JOIN PRODUCTO p 
        ON (pcar.PRODUCTO_ID = p.PRODUCTO_ID)
        JOIN RECIBO r 
        ON (com.COMPRADOR_ID = r.COMPRADOR_ID)

        WHERE u.USUARIO_ID = :usuario_id
                                         
     """, {'usuario_id' : usuario_id})
    
    resultados = cursor.fetchall()
    productosComprados = [{
        'recibo_id' : recibo_id,
        'nombre' : nombre ,
        'precio' : precio,
        'cantidad' : cantidad
    } for recibo_id, nombre, precio, cantidad in resultados]

    # Agrupar productos comprados dentro de cada recibo
    for recibo in recibos:
        recibo['productos'] = [
            producto for producto in productosComprados
            if producto['recibo_id'] == recibo['recibo_id']
        ]

        
    return render(request, 'user/userRecibo.html', {
        'usuario_id': usuario_id,
        'recibos': recibos
        })


def uSoporte(request, usuario_id):
    cursor = connection.cursor().execute("""
        SELECT 
            s.SOPORTE_ID,
            s.MENSAJE,
            s.FECHA
                                        
        FROM USUARIO u 
        JOIN SOPORTE s 
        ON (u.USUARIO_ID = s.USUARIO_ID)

        WHERE u.USUARIO_ID = :usuario_id                  
    """, {'usuario_id' : usuario_id})
    
    resultados = cursor.fetchall()
    soportes = [{
        'soporte_id' : soporte_id,
        'mensaje' : mensaje,
        'fecha' : fecha
    } for soporte_id, mensaje, fecha in resultados]

    return render(request, 'user/userSoporte.html', {
        'usuario_id': usuario_id,
        'soportes': soportes
        })


def uProducto(request, usuario_id):
    cursor = connection.cursor().execute("""
        SELECT 
            p.PRODUCTO_ID,
            p.NOMBRE,
            p.PRECIO,
            t.TIPO,
            AVG(val.ESTRELLAS) AVG_ESTRELLAS,
            COUNT(d.COMPRADOR_ID) AVG_DESCARGAS

        FROM USUARIO u
        JOIN VENDEDOR ven
        ON (u.USUARIO_ID = ven.USUARIO_ID)
        JOIN PRODUCTO p
        ON (ven.VENDEDOR_ID = p.VENDEDOR_ID)
        JOIN TIPO t 
        ON (p.PRODUCTO_ID = t.PRODUCTO_ID)
        JOIN DESCARGA d 
        ON (p.PRODUCTO_ID = d.PRODUCTO_ID)
        JOIN VALORACION val
        ON (p.PRODUCTO_ID = val.PRODUCTO_ID)

        WHERE u.USUARIO_ID = :usuario_id
        GROUP BY p.PRODUCTO_ID, p.NOMBRE, p.PRECIO, t.TIPO
            
    """, {'usuario_id' : usuario_id})
    
    resultados = cursor.fetchall()    
    Productos = [{
            'producto_id': producto_id, 
            'nombre': nombre, 
            'precio': precio,
            'tipo' : tipo,
            'estrellas' : estrellas,
            'descargas' : descargas,
            } 
            for producto_id, nombre, precio, tipo, estrellas, descargas in resultados]
    
    return render(request, 'user/userProducto.html', {'productos': Productos, 'usuario_id': usuario_id})


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
            AVG(val.ESTRELLAS),
            COUNT(d.COMPRADOR_ID),
            vu.NOMBRE

        FROM PRODUCTO p 
        JOIN TIPO t 
        ON (p.PRODUCTO_ID = t.PRODUCTO_ID)
        LEFT OUTER JOIN PLUGIN plu 
        ON (t.TIPO_ID = plu.TIPO_ID)
        LEFT OUTER JOIN SCHEMATIC sch 
        ON (t.TIPO_ID = sch.TIPO_ID)
        JOIN DESCARGA d 
        ON (p.PRODUCTO_ID = d.PRODUCTO_ID)
        JOIN VALORACION val
        ON (p.PRODUCTO_ID = val.PRODUCTO_ID)
        JOIN VENDEDOR ven
        ON (p.VENDEDOR_ID = ven.VENDEDOR_ID)
        JOIN USUARIO vu
        ON (ven.USUARIO_ID = vu.USUARIO_ID)

        GROUP BY p.PRODUCTO_ID, p.NOMBRE, p.DESCRIPCION, p.PRECIO, p.FECHA, t.TIPO, plu.VERSION, sch.DIMENSIONES, vu.NOMBRE
        HAVING p.PRODUCTO_ID = :producto_id
    """, {'producto_id' : producto_id})
    
    resultados = cursor.fetchall()    
    Producto = [{
            'producto_id': producto_id, 
            'nombre': nombre, 
            'descripcion': descripcion, 
            'precio': precio,
            'fecha': fecha,
            'tipo' : tipo,
            'version' : version,
            'dimensiones' : dimensiones,
            'estrellas' : estrellas,
            'descargas' : descargas,
            'vendedor' : vendedor
            } 
            for producto_id, nombre, descripcion, precio, fecha, tipo, version, dimensiones, estrellas, descargas, vendedor in resultados]

    cursor = connection.cursor().execute("""
        SELECT 
            cu.NOMBRE,
            val.COMENTARIO,
            val.ESTRELLAS

        FROM PRODUCTO p 
        JOIN VALORACION val
        ON (p.PRODUCTO_ID = val.PRODUCTO_ID)
        JOIN COMPRADOR com
        ON (val.COMPRADOR_ID = com.COMPRADOR_ID)
        JOIN USUARIO cu
        ON (com.USUARIO_ID = cu.USUARIO_ID)

        WHERE p.PRODUCTO_ID = :producto_id
    """, {'producto_id' : producto_id})
    
    resultados = cursor.fetchall()    
    comentarios = [{
            'comprador': comprador, 
            'comentario': comentario, 
            'estrellas' : estrellas
            } 
            for comprador, comentario, estrellas in resultados]
    
    return render(request, 'shop/producto.html', {
        'producto': Producto, 
        'comentarios' : comentarios, 
        'usuario_id': usuario_id
        })


def pago(request, usuario_id):
    return render(request, 'shop/pago.html', {'usuario_id': usuario_id})


def soporteRespuestas(request, usuario_id, soporte_id):
    cursor = connection.cursor().execute("""
        SELECT 
            s.MENSAJE,
            s.FECHA,
            res.MENSAJE,
            res.FECHA,
            res.TIPO,
            u.NOMBRE,
            uad.NOMBRE

        FROM USUARIO u 
        JOIN SOPORTE s 
        ON (u.USUARIO_ID = s.USUARIO_ID)
        JOIN RESPUESTA res 
        ON (s.SOPORTE_ID = res.SOPORTE_ID)
        LEfT OUTER JOIN ADMINISTRADOR ad 
        ON (res.ADMINISTRADOR_ID = ad.ADMINISTRADOR_ID)
        LEfT OUTER JOIN USUARIO uad 
        ON (ad.USUARIO_ID = uad.USUARIO_ID)

        WHERE s.SOPORTE_ID = :soporte_id               
    """, {'soporte_id' : soporte_id})

    resultados = cursor.fetchall()
    respuestasSoporte = [{
        'mensajeSoporte' : mensajeSoporte,
        'fechaSoporte' : fechaSoporte,
        'mensaje' : mensaje,
        'fecha' : fecha,
        'tipo' : tipo,
        'usuario' : usuario,
        'administrador' : administrador
    } for mensajeSoporte, fechaSoporte, mensaje, fecha, tipo, usuario, administrador in resultados]

    return render(request, 'user/soporteRespuestas.html', {
        'usuario_id': usuario_id,
        'respuestasSoporte': respuestasSoporte
        })