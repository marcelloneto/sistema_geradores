from django.urls import path
from . import views

app_name = "calculos"

urlpatterns = [
    path("", views.home_calculos, name="home"),
    path("condutor/", views.ResultadosCondutor.condutor, name="condutor"),
    path("isolamento/", views.ResultadosIsolamento().isolamento, name="isolamento"),
    path("pintura/", views.ResultadosPintura.pintura, name="pintura"),
]