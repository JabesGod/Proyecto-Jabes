from django.contrib.auth.models import User
from django.db import models




from django.db import models
from PIL import Image
from django.db.models.signals import pre_save
from django.dispatch import receiver

class Producto(models.Model):
    CATEGORIAS = (
    ('Medicamento/capsulas', 'Medicamento/capsulas'),
    ('Medicamento/liquido', 'Medicamento/liquido'),
    ('Cuidado/per', 'Cuidado/per'),
    ('Maternidad', 'Maternidad'),
    ('Belleza', 'Belleza'),
    ('Otros', 'Otros')
)
    nombre = models.CharField(max_length=100)
    precio = models.IntegerField()
    descripcion = models.TextField()
    categoria = models.CharField(max_length=50, choices=CATEGORIAS)
    cantidad = models.IntegerField()
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)
    imagen2 = models.ImageField(upload_to='productos/', blank=True, null=True)
    imagen3 = models.ImageField(upload_to='productos/', blank=True, null=True)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Otros campos adicionales para el perfil de usuario

    def __str__(self):
        return self.user.username


class Proveedor(models.Model):
    nombre_proveedor = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    correo = models.EmailField()
    entrega = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre_proveedor