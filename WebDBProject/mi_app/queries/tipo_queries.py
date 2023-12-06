from django.db import connection


def obtenerTipo(tipo_id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM TIPO WHERE TIPO_ID = %s", [tipo_id])
        tipo = cursor.fetchone()
    return tipo

def registrarTipo(version_compatible, tipo, producto_id, producto_vendedor_id):
    try:
        with connection.cursor() as cursor:
            version_compatible = version_compatible
            cursor.execute("""
                INSERT INTO TIPO (VRSION_CMPTBLE, TIPO, PRODUCTO_ID, PRODUCTO_VENDEDOR_ID)
                VALUES (%s, %s, %s, %s)
            """, [version_compatible, tipo, producto_id, producto_vendedor_id])
            cursor.execute("""
                SELECT max(tipo_id) FROM tipo
            """)
            tipo_id = cursor.fetchone()[0]
            connection.commit()
            return tipo_id
    except Exception as e:
        print("Ocurrio un error al insertar el tipo", e)
        return None

def actualizarTipo(tipo_id, version_compatible, tipo, producto_id, producto_vendedor_id):
    with connection.cursor() as cursor:
        cursor.execute("""
            UPDATE TIPO
            SET VERSION_CMPTBLE = %s, TIPO = %s, PRODUCTO_ID = %s, PRODUCTO_VENDEDOR_ID = %s
            WHERE TIPO_ID = %s
        """, [version_compatible, tipo, producto_id, producto_vendedor_id, tipo_id])
        connection.commit()

def eliminarTipo(tipo_id):
    print("Eliminando tipo")
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM TIPO WHERE TIPO_ID = %s", [tipo_id])
        connection.commit()