from django.shortcuts import redirect, render #render para ir a un html, y redirect  para redireccionar a un html
from django.http import HttpResponse, JsonResponse
from django.db import connection #para optener cursor y realizar consultas SQL
from . import forms

def login(request):

    if request.method == 'GET':
        #show interface
        form = forms.Login()
    
        return render(request, 'login.html', 
                  {'form': form})
    
    elif request.method == 'POST':
        form = forms.Login(request.POST)
        if form.is_valid():
            correo = form.cleaned_data['correo']
            contrasena = form.cleaned_data['contrasena']

            cursor = connection.cursor().execute("""
                SELECT
                    USUARIO_ID
                FROM USUARIO 
                WHERE CORREO = :1 AND CONTRASENA = :2   
                """, 
                {'1': correo, '2': contrasena})
            
            usuario_id = cursor.fetchone()

            if(usuario_id):
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
                
                return render(request, 'index.html', 
                        {'productos': Productos, 
                        'usuario_id': usuario_id[0]
                        })
        
    return render(request, 'login.html', 
                  {'form': form})

def register(request):
    if request.method == 'GET':
        #show interface
        form = forms.Register()
    
        return render(request, 'register.html', 
                  {'form': form})
    
    elif request.method == 'POST':
        form = forms.Register(request.POST)
        if form.is_valid():
            correo = form.cleaned_data['correo']
            contrasena = form.cleaned_data['contrasena']
            nombre = form.cleaned_data['nombre']
            apellido = form.cleaned_data['apellido']
            direccion = form.cleaned_data['direccion']
            telefono = form.cleaned_data['telefono']

            cursor = connection.cursor().execute("""
                SELECT
                    USUARIO_ID
                FROM USUARIO 
                WHERE CORREO = :1 AND CONTRASENA = :2   
                """, 
                {'1': correo, '2': contrasena})
            
            usuario_id = cursor.fetchone()

            if(usuario_id):
                return render(request, 'login.html', 
                  {'form': forms.Login()})
            else:

                connection.cursor().execute("""
                        INSERT INTO USUARIO(NOMBRE, APELLIDO, CORREO, CONTRASENA) VALUES (:1 , :2, :3, :4)
                    """, {
                        '1' : nombre, 
                        '2' : apellido,
                        '3' : correo,
                        '4' : contrasena 
                    })
                
                cursor = connection.cursor().execute("""
                        SELECT
                            USUARIO_ID
                        FROM USUARIO 
                        WHERE CORREO = :1 AND CONTRASENA = :2   
                        """, 
                        {'1': correo, '2': contrasena})
                usuario_id = cursor.fetchone()

                connection.cursor().execute("""
                        INSERT INTO PERFIL(USUARIO_ID, DIRECCION, TELEFONO) VALUES (:1 , :2, :3)
                    """, {
                        '1' : usuario_id[0], 
                        '2' : direccion, 
                        '3' : telefono 
                    })
                
                connection.cursor().execute("""
                        INSERT INTO COMPRADOR(USUARIO_ID) VALUES (:1)
                    """, {
                        '1' : usuario_id[0]
                    })
                
                connection.cursor().execute("""
                        INSERT INTO VENDEDOR(USUARIO_ID) VALUES (:1)
                    """, {
                        '1' : usuario_id[0]
                    })
                
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
                
                return render(request, 'index.html', 
                        {'productos': Productos, 
                        'usuario_id': usuario_id[0]
                        })
        