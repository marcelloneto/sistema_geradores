# Create your views here.
from django.shortcuts import render
from django.forms.models import model_to_dict
from operacao.services.ordem_service import OrdemService
from calculos.services.dados_maquina_service import DadosMaquinaService


def home_calculos(request):
    ordemservice = OrdemService("calculos")
    
    ordens = ordemservice.listar_ordens()
    
    ordem_selecionada = ordemservice.obter_ordem_selecionada(request)
    
    secao = request.GET.get("secao", "bobinas")
    request.session['secao_calculos'] = secao
    
    test = teste(secao,ordem_selecionada)
    
    return render(request, "calculos/home.html", {
        "ordens": ordens,
        "ordem_selecionada": ordem_selecionada,
        "secao": secao,
    })

class teste:
    def __init__ (self,secao,os):
        dados_maquina = DadosMaquinaService(secao)
        print(dados_maquina.obter_dados(os))