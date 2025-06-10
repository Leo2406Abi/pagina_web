from django.db import connection
from django.shortcuts import render
from tienda.models import Producto

def pagina_tienda(request):
    productos = Producto.objects.all()
    print("Productos encontrados:", productos.count())
    return render(request, 'tienda/productos.html', {'productos': productos})

def detalle_producto(request):
    return render(request, 'tienda/detalle_producto.html')

def carrito(request):
    return render(request, 'tienda/carrito.html')

def checkout(request):
    return render(request, 'tienda/checkout.html')
