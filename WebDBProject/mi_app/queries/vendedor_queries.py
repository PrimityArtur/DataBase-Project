from django.db import connection

def listaVendedor():
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM vendedor")
        resultadoBusqueda = cursor.fetchall()
    return resultadoBusqueda

def obtenerVendedor(vendedor_id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM vendedor WHERE vendedor_id = %s", [vendedor_id])
        vendedor = cursor.fetchone()
    return vendedor


def registrarVendedor(usuario_id):
    try:
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO vendedor (usuario_id) VALUES (%s)", [usuario_id])
    except Exception as e:
        print(f"Ocurrió un error al agregar el vendedor: {e}")

def eliminarVendedor(vendedor_id):
    print("Eliminando vendedor")
    try:
        vendedor_id = int(vendedor_id)
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM vendedor WHERE VENDEDOR_ID = %s", [vendedor_id])
    except ValueError:
        print("El ID proporcionado no es válido.")
    except Exception as e:
        print("Ocurrió un error al eliminar el vrnfrfot:", e)

def actualizarVendedor(vendedor_id, usuario_id):
    try:
        vendedor_id = int(vendedor_id)
        if not (usuario_id):
            raise ValueError("Todos los campos deben tener un valor.")

        with connection.cursor() as cursor:
            sql = """UPDATE VENDEDOR
                     SET USUARIO_ID
                     WHERE VENDEDOR_ID = %s"""
            cursor.execute(sql, vendedor_id)
            return cursor.rowcount  # filas modificadas
    except ValueError as ve:
        print("Error de validación:", ve)
        return None
    except Exception as e:
        print("Ocurrió un error al actualizar el vendedor:", e)
        return None