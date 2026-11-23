from django.urls import path
from . import views
from .views_edicao import editar_orcamento

app_name = "orcamento"

urlpatterns = [
    path("", views.lista_orcamentos, name="lista"),
    path("novo/", views.novo_orcamento, name="novo"),
    path("<int:pk>/detalhe/", views.detalhe_orcamento, name="detalhe"),
    path("<int:pk>/editar/", editar_orcamento, name="editar"),
]