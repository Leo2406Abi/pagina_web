from django.urls import path
from . import views

urlpatterns = [
    path('productos/', views.pagina_tienda, name='productos'),
    path('detalle-producto/', views.detalle_producto, name='detalle_producto'),
    path('carrito/', views.carrito, name='carrito'),
    path('checkout/', views.checkout, name='checkout'),
]