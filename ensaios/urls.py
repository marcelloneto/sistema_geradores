from django.urls import path
from . import views

app_name = 'ensaios'

urlpatterns = [
    path('', views.EnsaioListView.as_view(), name='lista'),
    path('novo/', views.EnsaioCreateView.as_view(), name='novo'),
    path('<int:pk>/detalhe/', views.EnsaioDetailView.as_view(), name='detalhe'),
    path('<int:pk>/editar/', views.EnsaioUpdateView.as_view(), name='editar'),
    path('<int:pk>/excluir/', views.EnsaioDeleteView.as_view(), name='excluir'),
    path('api/carregar-dados-maquina/', views.carregar_dados_maquina_api, name='api_dados_maquina'),
]