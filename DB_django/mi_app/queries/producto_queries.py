from django.db import connection

def listaProducto():
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM PRODUCTO")
        resultadoBusqueda = cursor.fetchall()
    return resultadoBusqueda

def registrarProducto(vendedor_id, nombre, descripcion, precio):
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO PRODUCTO (VENDEDOR_ID, NOMBRE, DESCRIPCION, PRECIO)
                VALUES (%s, %s, %s, %s)
            """, [vendedor_id, nombre, descripcion, precio])
            connection.commit()
    except Exception as e:
        print("Ocurrió un error al insertar el producto:", e)

def eliminarProducto(producto_id):
    print("Eliminando producto")
    try:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM PRODUCTO WHERE PRODUCTO_ID = %s", [producto_id])
            connection.commit()
    except Exception as e:
        print("Ocurrió un error al eliminar el producto:", e)

def obtenerProducto(producto_id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM PRODUCTO WHERE PRODUCTO_ID = %s", [producto_id])
        producto = cursor.fetchone()
    return producto

def actualizarProducto(producto_id, nombre, precio):
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE PRODUCTO
                SET  NOMBRE = %s, PRECIO = %s
                WHERE PRODUCTO_ID = %s
            """, [nombre, precio, producto_id])
            connection.commit()
    except Exception as e:
        print("Ocurrió un error al actualizar el producto:", e)

def insertarProducto(vendedor_id, nombre, descripcion, precio, vendedor_usuario_id):
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO PRODUCTO (VENDEDOR_ID, NOMBRE, DESCRIPCION, PRECIO, VENDEDOR_USUARIO_ID)
                VALUES (%s, %s, %s, %s, %s)
            """, [vendedor_id, nombre, descripcion, precio, vendedor_usuario_id])
            cursor.execute("""
                SELECT max(PRODUCTO_ID) FROM PRODUCTO
            """)
            producto_id = cursor.fetchone()[0]
            return producto_id
    except Exception as e:
        print("Ocurrio un error al insertar el producto", e)
        return None