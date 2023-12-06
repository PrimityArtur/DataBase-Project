from django.db import connection

def eliminarProdCarrito(producto_id):
    print("Eliminando ProdCarrito")
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM PRDCTO_CRRTO WHERE PRODUCTO_ID = %s", [producto_id])
        connection.commit()