from django.urls import path
from . import views

app_name = "calculos"

urlpatterns = [
    path("", views.home_calculos, name="home"),
]