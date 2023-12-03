from django.db import connection

def eliminarDescarga(producto_id):
    print("Eliminando descarga")
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM DESCARGA WHERE PRODUCTO_ID = %s", [producto_id])
        connection.commit()