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
ddef agregar_carrito(request):
    if request.method == "POST":
        prod_id = request.POST.get("producto_id")
        cantidad = int(request.POST.get("cantidad", 1))

        try:
            producto = Producto.objects.get(producto_id=prod_id)
        except Producto.DoesNotExist:
            return redirect("pagina_tienda")  # O mostrar un mensaje de error

        carrito = request.session.get("carrito", {})

        prod_id_str = str(prod_id)  # ← asegúrate de que sea string

        if prod_id_str in carrito:
            carrito[prod_id_str] += cantidad
        else:
            carrito[prod_id_str] = cantidad

        request.session["carrito"] = carrito
        return redirect("ver_carrito")



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

# --- Ver carrito ---
def ver_carrito(request):
    cart = request.session.get('cart', {})
    productos = []
    total = 0

    for prod_id, qty in cart.items():
        try:
            p = Producto.objects.get(producto_id=int (prod_id))
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

def eliminar_del_carrito(request):
    carrito = request.session.get("carrito", {})
    mensaje = ""
    if request.method == "POST":
        productos_a_eliminar = request.POST.getlist("productos_a_eliminar")
        if productos_a_eliminar:
            for prod_id in productos_a_eliminar:
                carrito.pop(str(prod_id), None)          # quita el ítem del dict
            request.session["carrito"] = carrito     # guarda el carrito limpio
            mensaje = "Producto(s) eliminado(s) del carrito."
    # Re-construir los datos que el template necesita
    productos = []
    total = 0
    for prod_id, qty in carrito.items():
        try:
            p = Producto.objects.get(producto_id=prod_id)
            subtotal = p.precio * qty
            productos.append({
                "producto_id": p.producto_id,
                "nombre":      p.nombre,
                "cant_en_carrito": qty,
                "precio":      p.precio,
                "subtotal":    subtotal,
            })
            total += subtotal
        except Producto.DoesNotExist:
            continue
    # ←  usa request y la ruta correcta de plantilla
    return render(
        request,
        "tienda/carrito.html",
        {"productos": productos, "total": total, "mensaje": mensaje}
    )

def checkout(request):
    return render(request, 'tienda/checkout.html')
