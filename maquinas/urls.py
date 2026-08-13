from django.urls import path
from . import views

app_name = 'maquinas'

urlpatterns = [
    path('', views.MaquinaListView.as_view(), name='lista'),
    path('nova/', views.NovaMaquinaView.as_view(), name='nova_maquina'), # <- Nova Rota
    
    path('<int:pk>/', views.MaquinaHomeView.as_view(), name='home'),
    path('<int:pk>/os/', views.ListaOSView.as_view(), name='lista_os'),
    path('<int:pk>/estator/', views.EstatorView.as_view(), name='estator'),
    path('<int:pk>/geometricos/', views.GeometricosView.as_view(), name='geometricos'),
    path('<int:pk>/perifericos/', views.PerifericosView.as_view(), name='perifericos'),
    path('<int:pk>/construtivos/', views.ConstrutivosView.as_view(), name='construtivos'),
    path('<int:pk>/ensaios/', views.EnsaiosView.as_view(), name='ensaios'),
    path('<int:pk>/bobinagem-roebel/', views.BobinagemRoebelView.as_view(), name='bobinagem_roebel'),
    path('<int:pk>/deletar/', views.DeletarMaquinaView.as_view(), name='deletar_maquina'),
]