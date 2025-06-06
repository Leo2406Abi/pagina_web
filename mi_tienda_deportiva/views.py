from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Usuario, Categoria, Pedido, DetallePedido, Pago
from tienda.models import Producto


# Verificar sesión admin
def verificar_sesion_admin(request):
    return request.session.get('admin_logged_in')

def inicio(request):
    return render(request, 'mi_tienda_deportiva/inicio.html')

def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username == 'root' and password == '':
            request.session['admin_logged_in'] = True
            return redirect('admin_dashboard')
        else:
            return render(request, 'mi_tienda_deportiva/admin_login.html', {'error': 'Credenciales inválidas'})
    return render(request, 'mi_tienda_deportiva/admin_login.html')

def admin_logout(request):
    request.session.flush()
    return redirect('admin_login')

# Panel principal
def admin_dashboard(request):
    if not verificar_sesion_admin(request):
        return redirect('admin_login')

    usuarios = User.objects.all()
    productos = Producto.objects.select_related('categoria').all()
    return render(request, 'mi_tienda_deportiva/admin_dashboard.html', {
        'usuarios': usuarios,
        'productos': productos 
    })

def ver_usuarios(request):
    usuarios = Usuario.objects.all()  
    return render(request, 'mi_tienda_deportiva/ver_usuarios.html', {
        'usuarios': usuarios,
        'total_usuarios': usuarios.count()
    })


def ver_productos(request):
    productos = Producto.objects.all()
    print(productos)  # Para depurar
    return render(request, 'mi_tienda_deportiva/ver_productos.html', {'productos': productos})


def ver_pedidos(request):
    if not verificar_sesion_admin(request):
        return redirect('admin_login')
    pedidos = Pedido.objects.all()
    return render(request, 'mi_tienda_deportiva/ver_pedidos.html', {'pedidos': pedidos})

def ver_categorias(request):
    if not verificar_sesion_admin(request):
        return redirect('admin_login')
    categorias = Categoria.objects.all()
    return render(request, 'mi_tienda_deportiva/ver_categorias.html', {'categorias': categorias})

def ver_detalles(request):
    if not verificar_sesion_admin(request):
        return redirect('admin_login')
    detalles = DetallePedido.objects.select_related('producto', 'pedido').all()
    return render(request, 'mi_tienda_deportiva/ver_detalles.html', {'detalles': detalles})

def ver_pagos(request):
    if not verificar_sesion_admin(request):
        return redirect('admin_login')
    pagos = Pago.objects.select_related('pedido').all()
    return render(request, 'mi_tienda_deportiva/ver_pagos.html', {'pagos': pagos})

# Eliminar
def eliminar_elemento(request):
    if not verificar_sesion_admin(request):
        return redirect('admin_login')

    tipo = request.GET.get('tipo')
    busqueda = request.GET.get('busqueda')
    modelo = {
        'usuario': Usuario,
        'producto': Producto,
        'pedido': Pedido,
        'categoria': Categoria,
        'detalle': DetallePedido,
        'pago': Pago
    }.get(tipo)

    id_field = ID_FIELDS.get(tipo)

    if modelo and id_field:
        try:
            if busqueda.isdigit():
                filtro = {id_field: busqueda}
            else:
                filtro = {'nombre': busqueda}

            objeto = modelo.objects.get(**filtro)
            objeto.delete()
            mensaje = f'{tipo.capitalize()} eliminado exitosamente.'
        except modelo.DoesNotExist:
            mensaje = f'{tipo.capitalize()} no encontrado.'
        except Exception as e:
            mensaje = f'Error al eliminar: {str(e)}'
    else:
        mensaje = 'Tipo no válido.'

    return render(request, 'mi_tienda_deportiva/resultado_admin.html', {'mensaje': mensaje})

# Modificar
def modificar_elemento(request):
    if not verificar_sesion_admin(request):
        return redirect('admin_login')

    if request.method == 'POST':
        tipo = request.POST.get('tipo')
        id_valor = request.POST.get('id')
        campo = request.POST.get('campo')
        nuevo_valor = request.POST.get('nuevo_valor')

        modelo = {
            'usuario': Usuario,
            'producto': Producto,
            'pedido': Pedido,
            'categoria': Categoria,
            'detalle': DetallePedido,
            'pago': Pago
        }.get(tipo)

        id_field = ID_FIELDS.get(tipo)

        if modelo and id_field:
            try:
                objeto = modelo.objects.get(**{id_field: id_valor})
                if hasattr(objeto, campo):
                    setattr(objeto, campo, nuevo_valor)
                    objeto.save()
                    mensaje = f'{tipo.capitalize()} modificado correctamente.'
                else:
                    mensaje = f'El campo "{campo}" no existe en {tipo}.'
            except modelo.DoesNotExist:
                mensaje = 'Elemento no encontrado.'
            except Exception as e:
                mensaje = f'Error al modificar: {str(e)}'
        else:
            mensaje = 'Tipo no válido.'

        return render(request, 'mi_tienda_deportiva/resultado_admin.html', {'mensaje': mensaje})

    return render(request, 'mi_tienda_deportiva/resultado_admin.html', {'mensaje': 'Método no permitido'})

# Verificar existencia
def verificar_elemento(request):
    if not verificar_sesion_admin(request):
        return redirect('admin_login')

    tipo = request.GET.get('tipo')
    busqueda = request.GET.get('busqueda')

    modelo = {
        'usuario': Usuario,
        'producto': Producto,
        'pedido': Pedido,
        'categoria': Categoria,
        'detalle': DetallePedido,
        'pago': Pago
    }.get(tipo)

    id_field = ID_FIELDS.get(tipo)

    if modelo and id_field:
        try:
            if busqueda.isdigit():
                filtro = {id_field: busqueda}
            else:
                filtro = {'nombre': busqueda}

            objeto = modelo.objects.get(**filtro)
            mensaje = f'{tipo.capitalize()} encontrado: {objeto}'
        except modelo.DoesNotExist:
            mensaje = f'{tipo.capitalize()} no encontrado.'
        except Exception as e:
            mensaje = f'Error: {str(e)}'
    else:
        mensaje = 'Tipo no válido.'

    return render(request, 'mi_tienda_deportiva/resultado_admin.html', {'mensaje': mensaje})

ID_FIELDS = {
    'usuario': 'usuario_id',
    'producto': 'producto_id',
    'pedido': 'pedido_id',
    'detalle': 'detalle_id',
    'categoria': 'categoria_id',
    'pago': 'pago_id',
}
