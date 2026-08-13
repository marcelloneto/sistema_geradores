from django.urls import path
from . import views

app_name = 'operacao'

urlpatterns = [
    # 1. Painel Principal / Detalhes da OS comercial selecionada (?os=NUMERO)
    path('', views.HomeOSView.as_view(), name='home'),
    
    # 2. Tela dedicada para Abertura de Nova OS
    path('nova-os/', views.NovaOrdemView.nova_os, name='nova_os'),
    
    # 3. Endpoint JSON para filtrar máquinas por cliente via JavaScript (no formulário de Nova OS)
    path('api/maquinas-cliente/', views.ApiOperacaoView.carregar_maquinas_cliente, name='api_maquinas_cliente'),
    
    # 4. Registros rápidos via formulários/modais (se ainda utilizados)
    path('registrar-os/', views.Registro.registrar_os, name='registrar_os'),
    path('registrar-cliente/', views.Registro.registrar_cliente, name='registrar_cliente'),
    path('registrar-maquina/', views.Registro.registrar_maquina, name='registrar_maquina'),
    path('<int:pk>/deletar/', views.DeletarOSView.as_view(), name='deletar_os'),
]