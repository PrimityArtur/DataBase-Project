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
            LEFT OUTER JOIN DESCARGA d 
            ON (p.PRODUCTO_ID = d.PRODUCTO_ID)
            LEFT OUTER JOIN VALORACION val
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
        FROM USUARIO u 
        LEFT OUTER JOIN PERFIL p 
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
            car.CARRITO_ID,
            p.PRODUCTO_ID,
            p.NOMBRE,
            p.PRECIO,
            t.TIPO,
            pcar.CANTIDAD
                                
        FROM USUARIO u 
        JOIN COMPRADOR com 
        ON (u.USUARIO_ID = com.USUARIO_ID)
        JOIN CARRITO car 
        ON (com.COMPRADOR_ID = car.COMPRADOR_ID)
        LEFT OUTER JOIN PRDCTO_CRRTO pcar 
        ON (car.CARRITO_ID = pcar.CARRITO_ID)
        LEFT OUTER JOIN PRODUCTO p 
        ON (pcar.PRODUCTO_ID = p.PRODUCTO_ID)
        LEFT OUTER JOIN TIPO t 
        ON (p.PRODUCTO_ID = t.PRODUCTO_ID)

        WHERE u.USUARIO_ID = :usuario_id AND car.CARRITO_ID = (SELECT 
                        MAX(fcar.CARRITO_ID)
                    FROM CARRITO fcar
                    WHERE fcar.COMPRADOR_ID = com.COMPRADOR_ID)
                                         
     """, {'usuario_id' : usuario_id})
    
    resultados = cursor.fetchall()
    carrito = [{
        'carrito_id' : carrito_id,
        'producto_id' : producto_id,
        'nombre' : nombre ,
        'precio' : precio,
        'tipo' : tipo,
        'cantidad' : cantidad
    } for carrito_id, producto_id, nombre, precio, tipo, cantidad in resultados]

    PrecioTotal = 0
    for i in carrito:
        if(i['precio']):
            PrecioTotal += i['precio']*i['cantidad']

    return render(request, 'shop/carrito.html', {
        'usuario_id': usuario_id,
        'carrito': carrito,
        'precioTotal' : PrecioTotal
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
        ON (car.CARRITO_ID = r.CARRITO_ID)
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
        LEFT OUTER JOIN DESCARGA d 
        ON (p.PRODUCTO_ID = d.PRODUCTO_ID)
        LEFT OUTER JOIN VALORACION val
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

    if request.method == 'POST':
        form = forms.AnadirCarritoForm(request.POST)
        if form.is_valid():
            cantidad_producto = form.cleaned_data['cantidad_producto']

            cursor = connection.cursor().execute("""
                SELECT 
                    car.CARRITO_ID,
                    c.COMPRADOR_ID,
                    car.PRECIO_TOTAL
                FROM COMPRADOR c JOIN CARRITO car
                ON c.COMPRADOR_ID = car.COMPRADOR_ID
                                                 
                WHERE c.USUARIO_ID = :usuario_id
                    AND  car.CARRITO_ID = (SELECT 
                                            MAX(CARRITO_ID) 
                                            FROM CARRITO car1 
                                            WHERE car1.comprador_ID = c.COMPRADOR_ID)""", 

                {'usuario_id': usuario_id})
            
            resultados = cursor.fetchall()
            comprador = [{
                'carrito_id' : carrito_id,
                'comprador_id' : comprador_id,
                'precio_total' : precio_total
            } for carrito_id, comprador_id, precio_total  in resultados]

            cursor = connection.cursor().execute("""
                SELECT 
                    VENDEDOR_ID,
                    PRECIO
                FROM PRODUCTO
                WHERE PRODUCTO_ID = :producto_id""", 

                {'producto_id': producto_id})
            
            resultados = cursor.fetchall()
            vendedor = [{
                'vendedor_id' : vendedor_id,
                'precio' : precio
            } for vendedor_id, precio  in resultados]

            connection.cursor().execute("""
                INSERT INTO PRDCTO_CRRTO (CARRITO_ID, PRODUCTO_ID, CANTIDAD, CARRITO_COMPRADOR_ID, PRODUCTO_VENDEDOR_ID) 
                VALUES (:1, :2, :3, :4, :5)""", 
                {'1': comprador[0]['carrito_id'], 
                 '2': producto_id, 
                 '3' : cantidad_producto, 
                 '4' : comprador[0]['comprador_id'],
                 '5' : vendedor[0]['vendedor_id']})
            
            connection.cursor().execute("""
                UPDATE CARRITO 
                SET PRECIO_TOTAL = (SELECT 
                                        PRECIO_TOTAL + :2 
                                    FROM CARRITO 
                                    WHERE CARRITO_ID = :1)
                WHERE CARRITO_ID = :1""", {
                    '1': comprador[0]['carrito_id'],
                    '2': (vendedor[0]['precio']*cantidad_producto)
                 })

            return redirect('carrito', usuario_id)
    
    else:
        form = forms.AnadirCarritoForm()
    
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
            LEFT OUTER JOIN DESCARGA d 
            ON (p.PRODUCTO_ID = d.PRODUCTO_ID)
            LEFT OUTER JOIN VALORACION val
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
            LEFT OUTER JOIN VALORACION val
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
            'form': form, 
            'producto': Producto, 
            'comentarios' : comentarios, 
            'usuario_id': usuario_id
            })


def pago(request, usuario_id, carrito_id, precioTotal):
    if request.method == 'POST':
        form = forms.CreatePago(request.POST)
        if form.is_valid():
            seleccion_usuario = form.cleaned_data['seleccion']

            cursor = connection.cursor().execute("""
                SELECT 
                    METODO_PAGO_ID
                FROM METODO_PAGO
                WHERE NOMBRE = :seleccion_usuario
            """, { 
                'seleccion_usuario': seleccion_usuario })
            seleccion = cursor.fetchone()

            cursor = connection.cursor().execute("""
                SELECT 
                    c.COMPRADOR_ID
                FROM COMPRADOR c
                JOIN USUARIO u
                ON c.USUARIO_ID = u.USUARIO_ID
                WHERE u.USUARIO_ID = :usuario_id
            """, { 
                'usuario_id': usuario_id })
            comprador_id = cursor.fetchone()

            connection.cursor().execute("""
                INSERT INTO PAGO(COMPRADOR_ID, METODO_PAGO_ID, TOTAL) VALUES (:1, :2, :3)
            """, {
                '1' : comprador_id[0], 
                '2' : seleccion[0], 
                '3' : precioTotal, 
            })


            cursor = connection.cursor().execute("""
                SELECT 
                    MAX(p.PAGO_ID)
                FROM COMPRADOR c
                JOIN PAGO p
                ON c.COMPRADOR_ID = p.COMPRADOR_ID
                WHERE c.USUARIO_ID = :usuario_id
            """, { 
                'usuario_id': usuario_id })
            pago_id = cursor.fetchone()

            
            connection.cursor().execute("""
                INSERT INTO RECIBO(PAGO_ID, COMPRADOR_ID, CARRITO_ID, PAGO_COMPRADOR_ID, PAGO_METODO_PAGO_ID, CARRITO_COMPRADOR_ID) VALUES (:1, :2, :3, :4, :5, :6)
            """, {
                '1' : pago_id[0], 
                '2' : comprador_id[0], 
                '3' : carrito_id, 
                '4' : comprador_id[0], 
                '5' : seleccion[0], 
                '6' : comprador_id[0]
                })

            connection.cursor().execute("""
                INSERT INTO CARRITO(COMPRADOR_ID, PRECIO_TOTAL) VALUES (:1, :2)
            """, {
                '1' : comprador_id[0], 
                '2' : 0
                })
            
            return redirect('uRecibo', usuario_id)
    else:
        form = forms.CreatePago()

    cursor = connection.cursor().execute("""
    SELECT 
        car.CARRITO_ID,
        p.PRODUCTO_ID,
        p.NOMBRE,
        p.PRECIO,
        t.TIPO,
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
    LEFT OUTER JOIN TIPO t 
    ON (p.PRODUCTO_ID = t.PRODUCTO_ID)

    WHERE u.USUARIO_ID = :usuario_id AND car.CARRITO_ID = (SELECT 
                    MAX(fcar.CARRITO_ID)
                FROM CARRITO fcar
                WHERE fcar.COMPRADOR_ID = com.COMPRADOR_ID)
                                         
     """, {'usuario_id' : usuario_id})
    
    resultados = cursor.fetchall()
    carrito = [{
        'carrito_id' : carrito_id,
        'producto_id' : producto_id,
        'nombre' : nombre ,
        'precio' : precio,
        'tipo' : tipo,
        'cantidad' : cantidad
    } for carrito_id, producto_id, nombre, precio, tipo, cantidad in resultados]

    return render(request, 'shop/pago.html', {
        'form': form, 
        'usuario_id': usuario_id, 
        'carrito': carrito,
        'precioTotal' : precioTotal})

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
        LEFT OUTER JOIN RESPUESTA res 
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