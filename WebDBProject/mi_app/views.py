from django.shortcuts import render
from django.db import transaction
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
import json
from .queries import (
    producto_queries, 
    usuario_queries, 
    vendedor_queries, 
    tipo_queries, 
    schematic_queries, 
    plugin_queries,
    descarga_queries,
    valoracion_queries,
    prodCarrito_queries,
)

@transaction.atomic
def get_combined_data(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT
                p.producto_id as producto_id,
                u.nombre AS vendedor_nombre,
                u.apellido AS vendedor_apellido,
                p.nombre AS producto_nombre,
                p.precio AS producto_precio,
                t.tipo AS tipo,
                s.dimensiones AS schematic_dimensiones,
                pl.version AS plugin_version,
                t.tipo_id AS tipo_id
            FROM
                usuario u
            INNER JOIN
                vendedor v ON u.usuario_id = v.usuario_id
            INNER JOIN
                producto p ON v.vendedor_id = p.vendedor_id
            INNER JOIN
                tipo t ON p.producto_id = t.producto_id
            LEFT JOIN
                schematic s ON t.tipo_id = s.tipo_id
            LEFT JOIN
                plugin pl ON t.tipo_id = pl.tipo_id
        """)
        rows = cursor.fetchall()
        print("rows=", rows)
        data = [
            {
                "producto_id": row[0],
                "vendedor_nombre": row[1],
                "vendedor_apellido": row[2],
                "producto_nombre": row[3],
                "producto_precio": row[4],
                "tipo": row[5],
                "schematic_dimensiones": row[6] if row[6] is not None else '',
                "plugin_version": row[7] if row[7] is not None else '',
                "tipo_id": row[8]
            }
            for row in rows
        ]
        #print(data)
        return JsonResponse({"data": data}, safe=False)  

def show_datatable(request, usuario_id = None):
    return render(request, 'datatable_template.html', {'usuario_id': usuario_id})

@csrf_exempt
def eliminar_producto_completo(request, producto_id):
    with connection.cursor() as cursor:
        producto_id = int(producto_id)
        print("Seleccionando ID\n", "productoID = ", producto_id)
        cursor.execute("""
            SELECT
                pr.producto_id,
                tp.tipo_id,
                sc.tipo_id,
                pl.tipo_id
            FROM
                producto pr 
                LEFT JOIN tipo tp ON pr.producto_id = tp.producto_id
                LEFT JOIN schematic sc ON tp.tipo_id = sc.tipo_id
                LEFT JOIN plugin pl ON tp.tipo_id = pl.tipo_id
            WHERE
                pr.producto_id = %s
        """, [producto_id])
        print("Identificado ID\n")
        ids_para_eliminar = cursor.fetchall()


    print("Preparandose para eliminar\n")
    for row in ids_para_eliminar:
        producto_id, tipo_id, schematic_id, plugin_id = row[0], row[1], row[2], row[3]
        
        plugin_queries.eliminarPlugin(plugin_id)
        schematic_queries.eliminarSchematic(schematic_id)
        tipo_queries.eliminarTipo(tipo_id)
        descarga_queries.eliminarDescarga(producto_id)
        valoracion_queries.eliminarValoracion(producto_id)
        prodCarrito_queries.eliminarProdCarrito(producto_id)
        producto_queries.eliminarProducto(producto_id)

    return JsonResponse({"success": True, "message": "Producto y entidades relacionadas eliminadas."})


@csrf_exempt
@require_http_methods(["POST"])
def actualizar_producto(request, producto_id):
    print("Actualizando producto:", producto_id)
    if request.method == 'POST':
        data = json.loads(request.body)
        producto_id = data.get('id')
        nombre = data.get('name')
        precio = data.get('price')
        tipo_id = data.get('tipo_id')
        tipo = data.get('tipo')
        dimensiones_o_version = data.get('dimensiones_o_version')
        print(f"\n\nProductoID ={producto_id}, NombreProd = {nombre}, PrecioProd = {precio}, tipo = {tipo}, tipoID = {tipo_id}")
        try:
            producto_queries.actualizarProducto(producto_id, nombre, precio)
            if tipo == 'PLUGIN':
                plugin_queries.modificarPlugin(tipo_id, dimensiones_o_version)
            elif tipo == 'SCHEMATIC':
                schematic_queries.modificarSchematic(tipo_id, dimensiones_o_version)
            print("\nACTUALIZADO PRODUCTO")
            return JsonResponse({'success': True, 'message': 'Producto actualizado correctamente'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': 'Error al actualizar el producto: {}'.format(e)})

@csrf_exempt
@require_http_methods(["POST"])
def insertar_producto(request):
    data = json.loads(request.body)
    vendedor_id = data.get('vendedor_id')
    
    # verificar si vendedor_id existe en la base de datos.
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT
                usuario_id
            FROM
                vendedor
            WHERE
                vendedor_id = %s
        """, [vendedor_id])
        resultado = cursor.fetchone()  
    
    if resultado is None:
        return JsonResponse({'success': False, 'message': 'Vendedor no existe.'}, status=404)
    
    usuario_id, = resultado
    nombre = data.get('nombre')
    descripcion = data.get('descripcion')
    precio = data.get('precio')
    tipo = data.get('tipo')
    dim_ver = data.get('dimension_version')
    ver_comp = data.get('version_compatible')
    print(f"Insertando producto para VENDEDOR_ID = {vendedor_id}, nombre = {nombre}, desc={descripcion}, precio = {precio}, tipo = {tipo}, dim_ver = {dim_ver}, ver_comp = {ver_comp}")
    try:
        producto_id = producto_queries.insertarProducto(vendedor_id, nombre, descripcion, precio, usuario_id)
        tipo_id = tipo_queries.registrarTipo(ver_comp,tipo,producto_id,vendedor_id)
        if(tipo == "SCHEMATIC"):
            schematic_queries.registrarSchematic(tipo_id,dim_ver)
        if(tipo == "PLUGIN"):
            plugin_queries.registrarPlugin(tipo_id, dim_ver)
        return JsonResponse({'success': True, 'message': 'Producto agregado correctamente'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': 'Error al agregar el producto: {}'.format(e)})

