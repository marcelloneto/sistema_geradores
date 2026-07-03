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
from decimal import Decimal


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
        if ordem_selecionada is None:
            return render(request, f"calculos/{secao}.html", {
                          "ordens": ordens,
                          })
        else:

            material_iso = dados_material_iso.obter_dados(ordem_selecionada.maquina)
            dados = dms.obter_dados(ordem_selecionada)
            material = d_material_s.obter_dados(ordem_selecionada.maquina)
            
            rss.atualizar_pagina(request)
            rss.verificar_mudanca_pagina(request)
            rss.verificar_secao(request, dados,secao,material["materiais_disponiveis"])
            rss.verificar_secao(request, dados,'isolacao_cond',material_iso['materiais_disponiveis'])
            rss.verificar_mudanca_os(request,ordem_selecionada)

            opcoes = rss.obter_opcoes_secao( material)
            if request.method == "POST":
                processar = rss.processar_post(request)
            opcoes_iso = rss.obter_opcoes_secao(material_iso)
             
            escolhido = rss.escolha(request,dados,material,secao)
            index_cond = ResultadosCondutor.selecao_cond(escolhido,rss,material)
            iso_escolhido = rss.escolha(request,dados,material_iso,'isolacao_cond')
            index_iso = ResultadosCondutor.selecao_iso(iso_escolhido,rss,material_iso)
            coeficiente_seguranca = request.session['resultados'].get(
                "coeficiente_seguranca_bobinas",
                "1.10"
            )
            folga = request.session['resultados'].get(
                "folga_ran",
                "0.40"
            )

            calculoservice = Filtros(dados,iso_sel=iso_escolhido,condutor=escolhido)
            
            resultados = calculoservice.calcularcondutor(coeficiente_seguranca,folga)
            
            return render(request, f"calculos/{secao}.html", {
                    "ordens": ordens,
                    "ordem_selecionada": ordem_selecionada,
                    "secao": secao,
                    "dados": dados,
                    "material": material,
                    "opcoes": opcoes,
                    "opcoes_iso": opcoes_iso,
                    "escolhido": escolhido,
                    "index_cond": index_cond,
                    "iso_escolhido": iso_escolhido,
                    "index_iso": str(index_iso),
                    'resultados': resultados,
                    "coeficiente_seguranca": coeficiente_seguranca,
                    "folga_ran": folga,
                })

    @staticmethod
    def selecao_iso(iso_escolhido,rss,material_iso):
        if iso_escolhido is None:
            index_iso = "-1"
        elif iso_escolhido == -1:
            index_iso = "-1"
            print(f"iso_escolhido: {type(iso_escolhido)}")
        else:
            index_iso = rss.obter_indice_por_id(material_iso['materiais_disponiveis'],iso_escolhido['id'])

        return index_iso
    @staticmethod
    def selecao_cond(escolhido,rss,material):
        if escolhido is None:
            index_cond = "0"
        else:
            index_cond = rss.obter_indice_por_id(material['materiais_disponiveis'],escolhido['id'])

        return index_cond

class ResultadosIsolamento:
    @staticmethod
    def isolamento(request):
        secao = 'isolacao'
        fita = 'isolamento_principal'
        request.session['resultados']['pagina_atual'] = "resultados_isolamento"

        ordemservice = OrdemService("calculos")
        ordens = ordemservice.listar_ordens()
        ordem_selecionada = ordemservice.obter_ordem_selecionada(request)
        if ordem_selecionada is None:
                    return render(request, f"calculos/isolamento.html", {
                                  "ordens": ordens,
                                  })
        else:
            dados = DadosMaquinaService(secao).obter_dados(ordem_selecionada)
            d_material_s = DadosMaterialService(fita)
            material = d_material_s.obter_dados(ordem_selecionada.maquina) 
            rss = RSS(secao)    
            
            rss.atualizar_pagina(request)
            
            rss.verificar_mudanca_pagina(request)
            
            rss.verificar_secao(request, dados,secao,material["materiais_disponiveis"])
            
            rss.verificar_mudanca_os(request,ordem_selecionada)
            
            opcoes = rss.obter_opcoes_secao( material)
            
            if request.method == "POST":
                processar = rss.processar_post(request)
            
            iso_escolhido = rss.escolha(request,dados,material,secao)
            index_iso = ResultadosCondutor.selecao_iso(iso_escolhido,rss,material)
            coeficiente_seguranca = request.session['resultados'].get(
                "coeficiente_seguranca_isolacao",
                "1.10"
            )
            fator_sobreposicao = request.session['resultados'].get(
                "fator_sobreposicao",
                Decimal(50)
            )
            
            resultados = Filtros(dados,iso_principal=iso_escolhido)
            resultados.calcularisolacao(fator_sobreposicao,coeficiente_seguranca)

            print(index_iso)

            print(dados['dados_bobinagem_roebel'])


            return render(request, "calculos/isolamento.html", {
                    "ordens": ordens,
                    "ordem_selecionada": ordem_selecionada,
                    "secao": secao,
                    "opcoes": opcoes,
                    "iso_escolhido": iso_escolhido,
                    "index_iso": str(index_iso),
                    "coeficiente_seguranca": coeficiente_seguranca,
                    "sobreposicao": fator_sobreposicao,
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

