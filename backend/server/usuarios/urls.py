from django.urls import re_path
from . import views

urlpatterns = [
    re_path('login', views.login),
    re_path('logout', views.logout),
    re_path('register', views.register),
    re_path('profile', views.profile),
    re_path('getAll', views.get_users),
    re_path('enviarCodigo', views.enviar_codigo),
    re_path('validarCodigo', views.validar_codigo),
    re_path('restartPass', views.cambiar_contrasena),
]
