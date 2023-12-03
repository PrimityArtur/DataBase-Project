from django.db import connection

def eliminarValoracion(producto_id):
    print("Eliminando Valoracion")
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM VALORACION WHERE PRODUCTO_ID = %s", [producto_id])
        connection.commit()