from django.urls import path
from . import views

urlpatterns = [
    path('tienda/', views.pagina_tienda, name='pagina_tienda'),
    path('detalle-producto/', views.detalle_producto, name='detalle_producto'),
    path('carrito/', views.carrito, name='carrito'),
    path('checkout/', views.checkout, name='checkout'),
]
