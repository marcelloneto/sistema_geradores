from django.urls import path
from .views import MaterialListView, MaterialCreateView, MaterialUpdateView, MaterialDeleteView, MaterialBulkDeleteView

app_name = "materiais"

urlpatterns = [
    path('', MaterialListView.as_view(), name='lista_materiais'),
    path('novo/', MaterialCreateView.as_view(), name='material_novo'),
    path('<int:pk>/editar/', MaterialUpdateView.as_view(), name='material_editar'),
    path('<int:pk>/remover/', MaterialDeleteView.as_view(), name='material_remover'),
    path('materiais/excluir-lote/', MaterialBulkDeleteView.as_view(), name='material_bulk_delete'),
]