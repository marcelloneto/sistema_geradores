from django.urls import path
from . import views


app_name = "operacao"

urlpatterns = [
    path("", views.home.home, name="home"),
    path("estator/", views.EstatorView.estator, name="estator"),
    path("geometricos/", views.GeometricosView.geometricos, name="geometricos"),
    path("perifericos/", views.PerifericosView.perifericos, name="perifericos"),
    path("contrutivos/", views.ConstrutivosView.construtivos, name="construtivos"),
    path("ensaios/", views.EnsaioIsolamentoView.ensaios, name="ensaios"),
    path("registrar_os/", views.Registro.registrar_os, name="registrar_os"),
    path("registrar_cliente/", views.Registro.registrar_cliente, name="registrar_cliente"),
    path("registrar_maquina/", views.Registro.registrar_maquina, name="registrar_maquina"),
    path("bobinagem_roebel/", views.BobinagemView.bobinagem_roebel, name="bobinagem_roebel"),
]