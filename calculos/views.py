# Create your views here.
from django.shortcuts import render
from django.forms.models import model_to_dict
from django.views import View
from operacao.services.ordem_service import OrdemService
from calculos.services.dados_maquina_service import DadosMaquinaService
from calculos.services.dados_material_service import DadosMaterialService
from calculos.services.session_service import ResultadosSessionService as RSS
from calculos.calculos.condutor import ResultadosCondutor as calculos

def home_calculos(request):
    request.session['resultados']={}

    ordemservice = OrdemService("calculos")
    
    ordens = ordemservice.listar_ordens()
    
    ordem_selecionada = ordemservice.obter_ordem_selecionada(request)
    
    secao = request.GET.get("secao", "bobinas")
    request.session['resultados']['secao_calculos'] = secao
    
    test = teste(request, ordem_selecionada)
    
    return render(request, "calculos/home.html", {
        "ordens": ordens,
        "ordem_selecionada": ordem_selecionada,
        "secao": secao,
    })

class teste:
    def __init__ (self,secao,os):
        dados_maquina = DadosMaquinaService(secao)
        print(dados_maquina.obter_dados(os))

class ResultadosCondutor:
    @staticmethod
    def condutor(request):
        secao = 'condutor'
        rss = RSS(secao)
        dms = DadosMaquinaService(secao)
        
        rss.validar_temp(request)
        d_material_s = DadosMaterialService(secao)
        
        
        ordemservice = OrdemService("calculos")
            
        ordens = ordemservice.listar_ordens()
        
        ordem_selecionada = ordemservice.obter_ordem_selecionada(request)

        dados = dms.obter_dados(ordem_selecionada)
        material = d_material_s.obter_dados(ordem_selecionada.maquina)
        
        rss.atualizar_pagina(request)
        rss.verificar_mudanca_pagina(request, material)
        rss.verificar_secao(request, dados)

        opcoes = rss.obter_opcoes_secao( material)
        if request.method == "POST":
            condutor_1 = rss.processar_post(request)
        
        escolhido = material['materiais_disponiveis'][request.session['resultados']['condutor_selecionado']-1]

        print(f"escolhido: {escolhido}")
        condutor1 = calculos(escolhido)
        condutor2 = calculos(escolhido)

        condutor1.teste(request)
        condutor2.teste(request)
        
        return render(request, f"calculos/{secao}.html", {
                "ordens": ordens,
                "ordem_selecionada": ordem_selecionada,
                "secao": secao,
                "dados": dados,
                "material": material,
                f"{secao}_calculo": request.session['resultados'][f'{secao}_selecionado'],
                "opcoes": opcoes,
                "escolhido": escolhido,
            })
        

class ResultadosIsolamento:
    @staticmethod
    def isolamento(request):
        secao = 'isolamento'
        request.session['resultados']['pagina_atual'] = "resultados_isolamento"
        dados = DadosMaquinaService(secao)
        ordemservice = OrdemService("calculos")
            
        ordens = ordemservice.listar_ordens()
        
        ordem_selecionada = ordemservice.obter_ordem_selecionada(request)
        print(ordem_selecionada)
        print(f"Resultados Isolamento: {dados.obter_dados(ordem_selecionada)}")
        request.session['resultados']['pagina_anterior'] = "resultados_isolamento"
        return render(request, "calculos/isolamento.html", {
                "ordens": ordens,
                "ordem_selecionada": ordem_selecionada,
                "secao": secao,
            })

class ResultadosPintura(View):
    @staticmethod
    def pintura(request):
        secao = 'pintura'
        dados = DadosMaquinaService(secao)
        ordemservice = OrdemService("calculos")
            
        ordens = ordemservice.listar_ordens()
        
        ordem_selecionada = ordemservice.obter_ordem_selecionada(request)
        print(ordem_selecionada)
        print(f"Resultados Pintura: {dados.obter_dados(ordem_selecionada)}")
        return render(request, "calculos/pintura.html", {
                "ordens": ordens,
                "ordem_selecionada": ordem_selecionada,
                "secao": secao,
            })

