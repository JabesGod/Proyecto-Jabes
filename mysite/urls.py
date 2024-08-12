from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from proyecto_sena import views 
from django.conf import settings
from django.urls import path, include
from django.contrib.auth import views as auth_views
    

urlpatterns = [
    path('admin/', admin.site.urls),
    path('administrador/', views.adminMenu, name='administrador'),
    path('', views.home, name='home'),
    path('desarrollador/', views.desarrollador, name='desarrollador'),
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
    path('singup/', views.singup, name='singup'),
    path('usuarios/', views.usuarios, name='usuarios'),
    path('proveedores/', views.proveedores, name='proveedores'),
    path('nuevo_proveedor/', views.nuevo_proveedor, name='nuevo_proveedor'),
    path('editar_proveedor/<int:proveedor_id>/', views.editar_proveedor, name='editar_proveedor'),
    path('eliminar_proveedor/<int:proveedor_id>/', views.eliminar_proveedor, name='eliminar_proveedor'),
    path('agregar_productos/', views.agregar_productos, name='agregar_productos'),
    path('password_reset/', views.recuperarcontrasena, name='password_reset'),
    path('cambiar-contrasena/', views.cambiarcontrasena, name='cambiarcontrasena'),
    path('medicamento_capsulas/', views.productos_medicamento_capsulas, name='productos_medicamento_capsulas'),
    path('medicamento_liquido/', views.productos_medicamento_liquido, name='productos_medicamento_liquido'),
    path('cuidado_per/', views.productos_cuidado_per, name='productos_cuidado_per'),
    path('maternidad/', views.productos_maternidad, name='productos_maternidad'),
    path('belleza/', views.productos_belleza, name='productos_belleza'),
    path('otros/', views.otros, name='otros'),
    path('producto/<int:producto_id>/', views.detalle_producto, name='detalle_producto'),
    path('crud/', views.crud, name='crud'),
    path('update/<int:pk>/', views.update, name='update'),
    path('delete/<int:pk>/', views.delete, name='delete'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
