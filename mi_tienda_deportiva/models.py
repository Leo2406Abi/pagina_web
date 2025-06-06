from django.db import models
from django.utils import timezone
from tienda.models import Producto, Categoria



class Usuario(models.Model):
    usuario_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    correo = models.EmailField()
    contraseña = models.CharField(max_length=128)
    dirección = models.TextField()
    teléfono = models.CharField(max_length=15)
    tipo_usuario = models.CharField(max_length=20)

    class Meta:
        db_table = 'usuarios'

class Pedido(models.Model):
    pedido_id = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, db_column='usuario_id')
    fecha_pedido = models.DateTimeField(auto_now_add=True)  
    estado = models.CharField(max_length=50)
    monto_total = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'pedidos'

class DetallePedido(models.Model):
    detalle_id = models.AutoField(primary_key=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'detalles_pedido'

class Pago(models.Model):
    pago_id = models.AutoField(primary_key=True)
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, db_column='pedido_id')
    monto_pagado = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_pago = models.DateTimeField()
    método_pago = models.CharField(max_length=100)

    class Meta:
        db_table = 'pagos' 
