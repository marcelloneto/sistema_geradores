from django.urls import path
from .views import (
    UnidadeGeradoraPainelCreateView,
    UnidadeGeradoraPainelDeleteView,
    UsinaListView,
    UsinaNovoPainelView,
    UsinaPainelView,
)

app_name = "usinas"

urlpatterns = [
    path("", UsinaListView.as_view(), name="lista_usinas"),
    path("novo/painel/", UsinaNovoPainelView.as_view(), name="usina_novo_painel"),
    path("<int:pk>/painel/", UsinaPainelView.as_view(), name="usina_painel"),
    path(
        "<int:pk>/unidades/nova/",
        UnidadeGeradoraPainelCreateView.as_view(),
        name="ug_nova_painel",
    ),
    path(
        "<int:pk>/unidades/<int:ug_pk>/remover/",
        UnidadeGeradoraPainelDeleteView.as_view(),
        name="ug_remover_painel",
    ),
]