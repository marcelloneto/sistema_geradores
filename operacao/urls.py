from django.urls import path
from . import views


app_name = "operacao"

urlpatterns = [
    path("", views.home, name="home"),
    path("estator/", views.EstatorView.estator, name="estator"),
]