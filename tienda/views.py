from django.db import connection
from django.shortcuts import render
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
    if request.method == 'POST':
        prod_id = request.POST.get('producto_id')
        qty     = int(request.POST.get('cantidad', 1))

        try:
            producto = Producto.objects.get(producto_id=prod_id)
        except Producto.DoesNotExist:
            messages.error(request, 'Producto no encontrado.')
            return redirect('pagina_tienda')

        # Carrito en sesión
        cart = request.session.get('cart', {})
        cart[str(prod_id)] = cart.get(str(prod_id), 0) + qty
        request.session['cart'] = cart
        messages.success(request, f'Añadido {qty} × {producto.nombre} al carrito.')
    return redirect('pagina_tienda')

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
