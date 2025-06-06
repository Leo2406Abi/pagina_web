from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('admin-login/', views.admin_login, name='admin_login'),
    path('logout/', views.admin_logout, name='admin_logout'),

    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),

    # Vistas de consulta
    path('dashboard/ver-usuarios/', views.ver_usuarios, name='ver_usuarios'),
    path('dashboard/ver-productos/', views.ver_productos, name='ver_productos'),
    path('dashboard/ver-pedidos/', views.ver_pedidos, name='ver_pedidos'),
    path('dashboard/ver-categorias/', views.ver_categorias, name='ver_categorias'),
    path('dashboard/ver-detalles/', views.ver_detalles, name='ver_detalles'),

    # Vistas de eliminación, modificación y verificación
    path('dashboard/eliminar/', views.eliminar_elemento, name='eliminar_elemento'),
    path('dashboard/modificar/', views.modificar_elemento, name='modificar_elemento'),
    path('dashboard/verificar/', views.verificar_elemento, name='verificar_elemento'),
    path('dashboard/ver-pagos/', views.ver_pagos, name='ver_pagos'),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
