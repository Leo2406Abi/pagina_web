from django.db import models

class Categoria(models.Model):
    categoria_id = models.AutoField(primary_key=True, db_column='categoria_id')
    nombre = models.CharField(max_length=100, db_column='nombre')

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'categorias'


class Producto(models.Model):
    producto_id = models.AutoField(primary_key=True, db_column='producto_id')
    nombre = models.CharField(max_length=255, db_column='nombre')
    descripción = models.TextField(db_column='descripción')
    precio = models.DecimalField(max_digits=10, decimal_places=2, db_column='precio')
    cantidad_en_stock = models.IntegerField(db_column='cantidad_en_stock')
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.CASCADE,
        db_column='categoria_id' )
    imagen = models.CharField(max_length=255, null=True, blank=True, db_column='imagen')

    class Meta:
        db_table = 'productos' 