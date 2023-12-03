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
            
            resultado = cursor.fetchone()

            if(resultado):
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
                        'usuario_id': resultado[0]
                        })
        
    return render(request, 'login.html', 
                  {'form': form})

def register(request):
    return render(request, 'register.html')