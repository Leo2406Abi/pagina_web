from django.urls import path
from . import views

urlpatterns = [
    path('productos/', views.pagina_tienda, name='pagina_tienda'),
    path('agregar-carrito/', views.agregar_carrito, name='agregar_carrito'),
    path('carrito/', views.ver_carrito, name='ver_carrito'),
]
