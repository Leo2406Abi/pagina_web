from django.db import connection
from django.shortcuts import render, redirect
from tienda.models import Producto
from django.contrib import messages

def pagina_tienda(request):
    productos = Producto.objects.all()
    print("Productos encontrados:", productos.count())
    return render(request, 'tienda/productos.html', {'productos': productos})

def detalle_producto(request):
    return render(request, 'tienda/detalle_producto.html')

# --- Añadir al carrito ---
def agregar_carrito(request):
    if request.method == "POST":
        producto_id = request.POST.get("producto_id")
        cantidad = int(request.POST.get("cantidad", 1))
        try:
            producto = Producto.objects.get(pk=producto_id)
        except Producto.DoesNotExist:
            return redirect('pagina_tienda')
        carrito = request.session.get("carrito", {})
        producto_id_str = str(producto_id)
        if producto_id_str in carrito:
            carrito[producto_id_str] += cantidad
        else:
            carrito[producto_id_str] = cantidad
        # Guardar en la sesión
        request.session["carrito"] = carrito

    return redirect("pagina_tienda")

# --- Ver carrito ---
def ver_carrito(request):
    cart = request.session.get('cart', {})
    productos = []
    total = 0

    for prod_id, qty in cart.items():
        try:
            p = Producto.objects.get(producto_id=prod_id)
            p.cant_en_carrito = qty
            p.subtotal = p.precio * qty
            total += p.subtotal
            productos.append(p)
        except Producto.DoesNotExist:
            pass  # producto eliminado de la BD

    return render(request, 'tienda/carrito.html', {
        'productos': productos,
        'total': total
    })

def checkout(request):
    return render(request, 'tienda/checkout.html')
