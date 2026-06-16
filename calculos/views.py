# Create your views here.
from django.shortcuts import render
from django.forms.models import model_to_dict
from django.views import View
from operacao.services.ordem_service import OrdemService
from calculos.services.dados_maquina_service import DadosMaquinaService
from calculos.services.dados_material_service import DadosMaterialService
from calculos.services.session_service import ResultadosSessionService as RSS
from calculos.calculos.condutor import ResultadosCondutor as calculos
from calculos.services.calculos_service import Filtros


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
        

class ResultadosCondutor:
    @staticmethod
    def condutor(request):
        secao = 'condutor'
        rss = RSS(secao)
        dms = DadosMaquinaService(secao)
        
        rss.validar_temp(request)
        d_material_s = DadosMaterialService(secao)
        dados_material_iso = DadosMaterialService('isolamento_principal')
        
        
        ordemservice = OrdemService("calculos")
            
        ordens = ordemservice.listar_ordens()
        
        ordem_selecionada = ordemservice.obter_ordem_selecionada(request)
        material_iso = dados_material_iso.obter_dados(ordem_selecionada.maquina)
        dados = dms.obter_dados(ordem_selecionada)
        material = d_material_s.obter_dados(ordem_selecionada.maquina)
        
        rss.atualizar_pagina(request)
        rss.verificar_mudanca_pagina(request)
        rss.verificar_secao(request, dados)
        rss.verificar_mudanca_os(request,ordem_selecionada)

        opcoes = rss.obter_opcoes_secao( material)
        if request.method == "POST":
            rss.processar_post(request)
        opcoes_iso = rss.obter_opcoes_secao(material_iso)

        escolhido = rss.escolha(request,dados,material,secao)

        iso_escolhido = rss.escolha(request,dados,material_iso,'isolacao')

        
        

        coeficiente_seguranca = request.session['resultados'].get(
            "coeficiente_seguranca_bobinas",
            1.10
        )

        calculoservice = Filtros(dados,escolhido)
        
        return render(request, f"calculos/{secao}.html", {
                "ordens": ordens,
                "ordem_selecionada": ordem_selecionada,
                "secao": secao,
                "dados": dados,
                "material": material,
                "opcoes": opcoes,
                "opcoes_iso": opcoes_iso,
                "escolhido": escolhido,
                "iso_escolhido": iso_escolhido,
                'resultados': calculoservice.calcularcondutor(coeficiente_seguranca),
                "coeficiente_seguranca": coeficiente_seguranca,
            })
        

class ResultadosIsolamento:
    @staticmethod
    def isolamento(request):
        secao = 'isolamento'
        fita = 'isolamento_principal'
        request.session['resultados']['pagina_atual'] = "resultados_isolamento"
        dados = DadosMaquinaService(secao)
        ordemservice = OrdemService("calculos")
        ordem_selecionada = ordemservice.obter_ordem_selecionada(request)
        d_material_s = DadosMaterialService(fita)
        material = d_material_s.obter_dados(ordem_selecionada.maquina) 
        rss = RSS(secao)    
        ordens = ordemservice.listar_ordens()
        rss.atualizar_pagina(request)
        rss.verificar_mudanca_pagina(request)

        print(f"Material: {material}")
        
        
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

