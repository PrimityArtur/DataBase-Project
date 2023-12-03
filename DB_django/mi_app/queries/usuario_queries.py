from django.db import connection

def listaUsuarios():
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM USUARIO")
        resultadoBusqueda = cursor.fetchall()
    return resultadoBusqueda

def registrarUsuario(nombre, apellido, correo, contrasena):
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO USUARIO (NOMBRE, APELLIDO, CORREO, CONTRASENA) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, [nombre, apellido, correo, contrasena])
    except Exception as e:
        print("Ocurrió un error al insertar el usuario:", e)

def eliminarUsuario(id_usuario):
    print("Eliminando usuario")
    try:
        id_usuario = int(id_usuario)
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM USUARIO WHERE USUARIO_ID = %s", [id_usuario])
    except ValueError:
        print("El ID proporcionado no es válido.")
    except Exception as e:
        print("Ocurrió un error al eliminar el usuario:", e)

def obtenerUsuario(id):
    try:
        id_usuario = int(id_usuario)
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM USUARIO WHERE USUARIO_ID = %s", [id_usuario])
            resultadoBusqueda = cursor.fetchone()
        return resultadoBusqueda
    except ValueError:
        print("El ID debe ser un entero")
    except Exception as e:
        print("Ocurrio un error al obtener el usuario:", e)
        return None

def actualizarUsuario(usuario_id, nombre, apellido, correo, contrasena):
    try:
        usuario_id = int(usuario_id)
        if not (nombre and apellido and correo and contrasena):
            raise ValueError("Todos los campos deben tener un valor.")

        with connection.cursor() as cursor:
            sql = """UPDATE USUARIO
                     SET NOMBRE = %s, APELLIDO = %s, CORREO = %s, CONTRASENA = %s
                     WHERE USUARIO_ID = %s"""
            cursor.execute(sql, [nombre, apellido, correo, contrasena, usuario_id])
            return cursor.rowcount  # filas modificadas
    except ValueError as ve:
        print("Error de validación:", ve)
        return None
    except Exception as e:
        print("Ocurrió un error al actualizar el usuario:", e)
        return None
        
