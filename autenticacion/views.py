from django.shortcuts import render, redirect
from django.db import connection
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth import authenticate, login
import random
import string


def register_view(request):
    error = None

    if request.method == "POST":
        nombre = request.POST.get("name")
        correo = request.POST.get("email")
        contraseña = request.POST.get("password")
        direccion = request.POST.get("direccion")
        telefono = request.POST.get("telefono")
        tipo_usuario = request.POST.get("tipo_usuario")

        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO usuarios (nombre, correo, contraseña, dirección, teléfono, tipo_usuario)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, [nombre, correo, contraseña, direccion, telefono, tipo_usuario])
            
            # Registro exitoso: redirige al login
            return redirect("login")

        except Exception as e:
            print("Error al insertar usuario:", e)
            error = "Ocurrió un error al registrar el usuario. Intenta de nuevo."

    return render(request, "autenticacion/register.html", {
        "error": error
    })
          

def login_view(request):
    if request.method == "POST":
        correo = request.POST['email']
        contraseña = request.POST['password']

        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM usuarios WHERE correo = %s AND contraseña = %s", [correo, contraseña])
            usuario = cursor.fetchone()

        if usuario:
            print("Login exitoso. Usuario ID:", usuario[0])  # <-- imprime en consola
            request.session['usuario_id'] = usuario[0]
            return redirect('perfil')
        else:
            print("Login fallido.")
            return render(request, 'autenticacion/login.html', {'error': 'Credenciales inválidas'})
    
    return render(request, 'autenticacion/login.html')

def perfil(request):
    usuario_id = request.session.get('usuario_id')

    if not usuario_id:
        return redirect('login')

    if request.method == "POST":
        nueva_contraseña = request.POST.get('password')

        if nueva_contraseña:
            try:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "UPDATE usuarios SET contraseña = %s WHERE usuario_id = %s",
                        [nueva_contraseña, usuario_id]
                    )
                messages.success(request, "Contraseña actualizada correctamente.")
            except Exception as e:
                print("Error al actualizar contraseña:", e)
                messages.error(request, "Error al actualizar la contraseña.")
        else:
            messages.warning(request, "No se ingresó una nueva contraseña.")

    with connection.cursor() as cursor:
        cursor.execute("SELECT nombre, correo, dirección, teléfono FROM usuarios WHERE usuario_id = %s", [usuario_id])
        usuario = cursor.fetchone()

    if usuario:
        datos_usuario = {
            'nombre': usuario[0],
            'correo': usuario[1],
            'direccion': usuario[2],
            'telefono': usuario[3]
        }
        return render(request, 'autenticacion/profile.html', {'usuario': datos_usuario})
    else:
        return redirect('login')



def generar_contraseña(n=8):
    caracteres = string.ascii_letters + string.digits
    return ''.join(random.choice(caracteres) for _ in range(n))

def recover_password_view(request):
    if request.method == "POST":
        correo = request.POST.get("email")

        with connection.cursor() as cursor:
            cursor.execute("SELECT usuario_id FROM usuarios WHERE correo = %s", [correo])
            resultado = cursor.fetchone()

        if resultado:
            nueva_contraseña = generar_contraseña()

            try:
                # Actualizar la contraseña en la base de datos
                with connection.cursor() as cursor:
                    cursor.execute("UPDATE usuarios SET contraseña = %s WHERE correo = %s", [nueva_contraseña, correo])

                # Enviar la nueva contraseña por correo
                send_mail(
                    subject='Recuperación de contraseña - Tienda Deportiva',
                    message=f'Tu nueva contraseña es: {nueva_contraseña}',
                    from_email='tucorreo@gmail.com',
                    recipient_list=[correo],
                    fail_silently=False,
                )

                messages.success(request, "Se ha enviado una nueva contraseña a tu correo.")
                return redirect('login')

            except Exception as e:
                print("Error al enviar correo:", e)
                messages.error(request, "Hubo un error al enviar el correo.")
        else:
            messages.error(request, "El correo no se encuentra registrado.")

    return render(request, "autenticacion/recover_password.html")

def pagina_tienda(request):
    return render(request, 'tienda/productos.html')
