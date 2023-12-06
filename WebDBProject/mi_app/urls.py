from django.urls import path
from . import views

urlpatterns = [
    path('show-datatable/<int:usuario_id>', views.show_datatable, name='show_datatable'),
    path('api/data/', views.get_combined_data, name='get_combined_data'),
    path('eliminar_producto_completo/<int:producto_id>/', views.eliminar_producto_completo, name='eliminar_producto_completo'),
    path('actualizar_producto/<int:producto_id>/', views.actualizar_producto, name='actualizar_producto'),
    path('insertar_producto/', views.insertar_producto, name='insertar_producto'),
]