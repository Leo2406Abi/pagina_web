from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('recover/', views.recover_password_view, name='recover_password'), 
    path('perfil/', views.perfil, name='perfil'),

]
