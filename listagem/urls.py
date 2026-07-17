from django.urls import path
from . import views

app_name = "listagem"

urlpatterns = [
    path("", views.home, name="home"),
]