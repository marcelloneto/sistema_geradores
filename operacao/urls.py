from django.urls import path
from . import views


app_name = "operacao"

urlpatterns = [
    path("", views.home.home, name="home"),
    path("estator/", views.EstatorView.estator, name="estator"),
    path("geometricos/", views.GeometricosView.geometricos, name="geometricos"),
    path("perifericos/", views.PerifericosView.perifericos, name="perifericos"),
    path("contrutivos/", views.ConstrutivosView.construtivos, name="construtivos")
]