from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Proveedor
from .models import Producto
from django import forms




class RegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['email', 'username', 'password1', 'password2']



class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['nombre_proveedor', 'telefono', 'correo', 'entrega']
        labels = {
            'nombre_proveedor': 'Nombre del proveedor',
            'telefono': 'Teléfono',
            'correo': 'Correo electrónico',
            'entrega': 'Entrega del proveedor'
        }


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'precio', 'descripcion', 'categoria', 'cantidad', 'imagen', 'imagen2', 'imagen3']


class AgregarProductoForm(forms.Form):
    cantidad = forms.IntegerField(min_value=1)


