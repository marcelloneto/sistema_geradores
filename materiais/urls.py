from django.urls import path
from .views import (
    MaterialBulkDeleteView,
    MaterialCreateView,
    MaterialDeleteView,
    MaterialListView,
    MaterialNovoPainelView,
    MaterialPainelView,
    MaterialUpdateView,
)

app_name = "materiais"

urlpatterns = [
    path("", MaterialListView.as_view(), name="lista_materiais"),
    path("novo/", MaterialCreateView.as_view(), name="material_novo"),
    path("novo/painel/", MaterialNovoPainelView.as_view(), name="material_novo_painel"),
    path("<int:pk>/painel/", MaterialPainelView.as_view(), name="material_painel"),
    path("<int:pk>/editar/", MaterialUpdateView.as_view(), name="material_editar"),
    path("<int:pk>/remover/", MaterialDeleteView.as_view(), name="material_remover"),
    path("excluir-lote/", MaterialBulkDeleteView.as_view(), name="material_bulk_delete"),
]