from django.urls import path
from . import views

app_name = "ensaios"

urlpatterns = [
    path("", views.home, name="home"),
]