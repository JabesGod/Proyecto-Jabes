import os
import uuid
import smtplib
import random
import string
from PIL import Image
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib import messages
from django.urls import reverse
from email.message import EmailMessage
from django.db.models import Q
from .models import Proveedor, Producto
from .forms import ProveedorForm, RegistrationForm, ProductoForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.http import JsonResponse 
from django.core.mail import send_mail


def home(request): 
    if request.method == 'GET':
        productos = Producto.objects.all()
        paginator = Paginator(productos, 18)  # 18 productos por página
        page_number = request.GET.get('page')  # Obtiene el número de página actual
        page_obj = paginator.get_page(page_number)  # Obtiene el objeto de página actual
        return render(request, 'home.html', {'page_obj': page_obj})
    else:
        buscar_palabra = request.POST.get('buscar', '')  # Obtener la palabra buscada del formulario
        
        productos = Producto.objects.filter(Q(nombre__icontains=buscar_palabra))
        paginator = Paginator(productos, 18)  # 18 productos por página
        page_number = request.GET.get('page')  # Obtiene el número de página actual
        page_obj = paginator.get_page(page_number)  # Obtiene el objeto de página actual
        return render(request, 'home.html', {'page_obj': page_obj, 'buscar_palabra': buscar_palabra})


def user_is_admin(user):
    return user.is_authenticated and user.is_staff

@login_required
@user_passes_test(user_is_admin)
def adminMenu(request):
    return render(request, "admin.html")



def detalle_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)

    if request.method == 'POST' and 'buscar' in request.POST:
        query = request.POST['buscar']
        productos_recomendados = Producto.objects.filter(
            Q(nombre__icontains=query) & Q(categoria=producto.categoria)
        ).exclude(id=producto_id).order_by('?')[:6]
    else:
        productos_recomendados = Producto.objects.filter(
            categoria=producto.categoria
        ).exclude(id=producto_id).order_by('?')[:6]

    return render(request, 'detalle_producto.html', {'producto': producto, 'productos_recomendados': productos_recomendados})


def desarrollador(request):
   
    return render(request, 'desarrollador.html', {'desarrolladores': desarrollador})
   

def recuperarcontrasena(request):
    email_sent = False  # Variable para indicar si el correo ha sido enviado

    if request.method == 'POST': 
        email = request.POST['email']
        try: 
            user = User.objects.get(email=email)
        except: 
            print("sexooooo")
        if user: 
            correo = "no-reply@adventureclothing.shop"
            contrasena = "DannyyYesid15"
            url = "mail.adventureclothing.shop"
            passhas, password = generar_password()
            user.password = passhas
            user.save()

            def sendEmail(subject: str, senderEmail: str, receiverEmail: str, smtpUrl: str, password: str, content: str) -> bool:
                try:
                    message = EmailMessage()
                    message['Subject'] = subject
                    message['From'] = senderEmail
                    message['To'] = receiverEmail
                    message.set_content(content)
                    server = smtplib.SMTP(smtpUrl, '587')
                    server.ehlo()
                    server.starttls()
                    server.login(senderEmail, password)
                    server.send_message(message)
                    server.quit()
                    return True
                except:
                    return False

            email_sent = sendEmail("Recupera tu cuenta puto", correo, email,
                                   url, contrasena, "Hola caballero, al parecer usted ha perdido el acceso a nuestra página web, esta es su contraseña temporal: " + password)
            return redirect(signin)
    else: 
        return render(request, 'password_reset_form.html', {'email_sent': email_sent})



def generar_password(longitud=8):
    caracteres = string.ascii_letters + string.digits
    password = ''.join(random.choice(caracteres) for i in range(longitud))
    passhashed = make_password(password)
    return passhashed, password

@login_required
def cambiarcontrasena(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        
        # Verificar que la contraseña actual sea correcta
        if request.user.check_password(current_password):
            # Cambiar la contraseña del usuario
            request.user.set_password(new_password)
            request.user.save()
            
            messages.success(request, 'Contraseña cambiada exitosamente.')
            return redirect('signin')
        else:
            messages.error(request, 'La contraseña actual es incorrecta.')
    
    return render(request, 'new_password.html')


def signin(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            # Verificar si el usuario es administrador y establecer el campo is_admin
            if user.is_staff:  # Puedes usar otro criterio para determinar si un usuario es administrador
                user.is_admin = True
                user.save()

            return redirect('home')
        else:
            msg = 'Nombre de usuario o contraseña incorrectos'
            messages.error(request, msg)
    return render(request, 'login.html')



def signout(request):
    logout(request)
    return redirect(reverse('home'))


def singup(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']

            # Verificar si el usuario o correo ya existen en la base de datos
            if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
                messages.error(request, 'El usuario o correo electrónico ya existe.')
                return render(request, 'singup.html', {'form': form})

            form.save()
            # Redirigir a la página de inicio de sesión después de un registro exitoso
            return redirect('signin')

    else:
        form = RegistrationForm()
    return render(request, 'singup.html', {'form': form})


def usuarios(request):
    users = User.objects.all()
    return render(request, 'usuarios.html', {'users': users})

def proveedores(request):
    proveedores = Proveedor.objects.all()
    return render(request, 'proveedores.html', {'proveedores': proveedores})

def nuevo_proveedor(request):
    if request.method == 'POST':
        form = ProveedorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('proveedores')
    else:
        form = ProveedorForm()
    return render(request, 'nuevo_proveedor.html', {'form': form})

def editar_proveedor(request, proveedor_id):
    proveedor = get_object_or_404(Proveedor, pk=proveedor_id)
    if request.method == 'POST':
        form = ProveedorForm(request.POST, instance=proveedor)
        if form.is_valid():
            form.save()
            return redirect('proveedores')
    else:
        form = ProveedorForm(instance=proveedor)
    return render(request, 'editar_proveedor.html', {'form': form, 'proveedor': proveedor})

def eliminar_proveedor(request, proveedor_id):
    proveedor = get_object_or_404(Proveedor, pk=proveedor_id)
    if request.method == 'POST':
        proveedor.delete()
        return redirect('proveedores')
    return render(request, 'eliminar_proveedor.html', {'proveedor': proveedor})

def crud(request):
    productos = Producto.objects.all()
    form = ProductoForm()
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('crud')
    context = {'productos': productos, 'form': form}
    return render(request, 'crud.html', context)

def update(request, pk):
    producto = Producto.objects.get(id=pk)
    form = ProductoForm(instance=producto)
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('crud')
    context = {'form': form, 'producto': producto}
    return render(request, 'crud.html', context)

def delete(request, pk):
    producto = Producto.objects.get(id=pk)
    if request.method == 'POST':
        producto.delete()
        return redirect('crud')
    context = {'producto': producto}
    return render(request, 'delete.html', context)






def productos_medicamento_capsulas(request):
    if request.method == 'GET':
        productos = Producto.objects.filter(categoria='Medicamento/capsulas')
        paginator = Paginator(productos, 18)  # 18 productos por página
        page_number = request.GET.get('page')  # Obtiene el número de página actual
        page_obj = paginator.get_page(page_number)  # Obtiene el objeto de página actual
        return render(request, 'medicamento_capsulas.html', {'page_obj': page_obj, 'productos':productos})
    else:
        productos = Producto.objects.filter(Q(nombre__icontains=request.POST['buscar']) & Q(categoria='Medicamento/capsulas'))
        paginator = Paginator(productos, 18)  # 18 productos por página
        page_number = request.GET.get('page')  # Obtiene el número de página actual
        page_obj = paginator.get_page(page_number)  # Obtiene el objeto de página actual
    return render(request, 'medicamento_capsulas.html', {'page_obj': page_obj, 'productos':productos})

def productos_medicamento_liquido(request):
    if request.method == 'GET':
        productos = Producto.objects.filter(categoria='Medicamento/liquido')
        paginator = Paginator(productos, 18)  # 18 productos por página
        page_number = request.GET.get('page')  # Obtiene el número de página actual
        page_obj = paginator.get_page(page_number)  # Obtiene el objeto de página actual
        return render(request, 'medicamento_liquido.html', {'page_obj': page_obj, 'productos':productos})
    else:
        productos = Producto.objects.filter(Q(nombre__icontains=request.POST['buscar']) & Q(categoria='Medicamento/liquido'))
        paginator = Paginator(productos, 18)  # 18 productos por página
        page_number = request.GET.get('page')  # Obtiene el número de página actual
        page_obj = paginator.get_page(page_number)  # Obtiene el objeto de página actual
    return render(request, 'medicamento_liquido.html', {'page_obj': page_obj, 'productos':productos})


def productos_cuidado_per(request):
    if request.method == 'GET':
        productos = Producto.objects.filter(categoria='Cuidado/per')
        paginator = Paginator(productos, 18)  # 18 productos por página
        page_number = request.GET.get('page')  # Obtiene el número de página actual
        page_obj = paginator.get_page(page_number)  # Obtiene el objeto de página actual
        return render(request, 'cuidado_per.html', {'page_obj': page_obj, 'productos':productos})
    else:
        productos = Producto.objects.filter(Q(nombre__icontains=request.POST['buscar']) & Q(categoria='Cuidado/per'))
        paginator = Paginator(productos, 18)  # 18 productos por página
        page_number = request.GET.get('page')  # Obtiene el número de página actual
        page_obj = paginator.get_page(page_number)  # Obtiene el objeto de página actual
    return render(request, 'cuidado_per.html', {'page_obj': page_obj, 'productos':productos})



def productos_maternidad(request):
    if request.method == 'GET':
        productos = Producto.objects.filter(categoria='Maternidad')
        paginator = Paginator(productos, 18)  # 18 productos por página
        page_number = request.GET.get('page')  # Obtiene el número de página actual
        page_obj = paginator.get_page(page_number)  # Obtiene el objeto de página actual
        return render(request, 'maternidad.html', {'page_obj': page_obj, 'productos':productos})
    else:
        productos = Producto.objects.filter(Q(nombre__icontains=request.POST['buscar']) & Q(categoria='Maternidad'))
        paginator = Paginator(productos, 18)  # 18 productos por página
        page_number = request.GET.get('page')  # Obtiene el número de página actual
        page_obj = paginator.get_page(page_number)  # Obtiene el objeto de página actual
    return render(request, 'maternidad.html', {'page_obj': page_obj, 'productos':productos})


def productos_belleza(request):
    if request.method == 'GET':
        productos = Producto.objects.filter(categoria='Belleza')
        paginator = Paginator(productos, 18)  # 18 productos por página
        page_number = request.GET.get('page')  # Obtiene el número de página actual
        page_obj = paginator.get_page(page_number)  # Obtiene el objeto de página actual
        return render(request, 'belleza.html', {'page_obj': page_obj, 'productos':productos})
    else:
        productos = Producto.objects.filter(Q(nombre__icontains=request.POST['buscar']) & Q(categoria='Belleza'))
        paginator = Paginator(productos, 18)  # 18 productos por página
        page_number = request.GET.get('page')  # Obtiene el número de página actual
        page_obj = paginator.get_page(page_number)  # Obtiene el objeto de página actual
    return render(request, 'belleza.html', {'page_obj': page_obj, 'productos':productos})

def otros(request):
    if request.method == 'GET':
        productos = Producto.objects.filter(categoria='Otros')
        paginator = Paginator(productos, 18)  # 18 productos por página
        page_number = request.GET.get('page')  # Obtiene el número de página actual
        page_obj = paginator.get_page(page_number)  # Obtiene el objeto de página actual
        return render(request, 'otros.html', {'page_obj': page_obj, 'productos':productos})
    else:
       buscar_palabra = request.POST.get('buscar', '')
    productos = Producto.objects.filter(nombre__icontains=buscar_palabra, categoria='Otros')
    paginator = Paginator(productos, 18)  # 18 productos por página
    page_number = request.GET.get('page')  # Obtiene el número de página actual
    page_obj = paginator.get_page(page_number)  # Obtiene el objeto de página actual
    return render(request, 'otros.html', {'page_obj': page_obj, 'productos':productos})

def agregar_productos(request, id):
    producto = Producto.objects.get(id=id)
    disponibilidad = producto.cantidad
    carrito = request.session.get('carrito', [])
    for item in carrito:
        if item['id'] == id:
            cantidad_total = item['cantidad'] + 1
            if cantidad_total <= disponibilidad:
                item['cantidad'] = cantidad_total
            break
    else:
        if disponibilidad >= 1:
            carrito.append({'id': id, 'cantidad': 1}) 
    request.session['carrito'] = carrito
    return redirect(request.META.get('HTTP_REFERER', '/'))

def eliminar_producto(request, id):
    carrito = request.session.get('carrito', [])
    for item in carrito:
        if item['id'] == id:
            if item['cantidad'] > 1:
                item['cantidad'] -= 1
            else:
                carrito.remove(item)
            break
    request.session['carrito'] = carrito
    return JsonResponse({'message': 'Producto eliminado del carrito'})

def carrito(request):
    carrito = request.session.get('carrito', [])
    carrito_con_cantidad = []

    for item in carrito:
        producto = Producto.objects.get(id=item['id'])
        item['producto'] = producto
        item['cantidad_carrito'] = item['cantidad']
        carrito_con_cantidad.append(item)

    total = sum(item['cantidad_carrito'] * item['producto'].precio for item in carrito_con_cantidad)

    return carrito_con_cantidad, total


    