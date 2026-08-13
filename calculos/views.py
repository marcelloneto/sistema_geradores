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
from calculos.services.inicializacao_service import Iniciar


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
        
        dms = DadosMaquinaService(secao)

        iniciar = Iniciar(request,secao)

        rss = iniciar.rss

        d_material_s = DadosMaterialService(secao)
        dados_material_iso = DadosMaterialService('isolamento_principal')
        
        if iniciar.ordem_selecionada is None:
            return render(request, f"calculos/{secao}.html", {
                          "ordens": iniciar.ordens,
                          })
        else:

            material_iso = dados_material_iso.obter_dados(iniciar.ordem_selecionada.maquina)
            dados = dms.obter_dados(iniciar.ordem_selecionada)
            material = d_material_s.obter_dados(iniciar.ordem_selecionada.maquina)

            iso_principal = material_iso['material_utilizado']
             
            rss.verificar_secao(request, dados,secao,material["materiais_disponiveis"])
            rss.verificar_secao(request, dados,'isolacao_cond',material_iso['materiais_disponiveis'])
            
            opcoes = rss.obter_opcoes_secao( material["materiais_disponiveis"])
            if request.method == "POST":
                processar = rss.processar_post(request)
            opcoes_iso = rss.obter_opcoes_secao(material_iso["materiais_disponiveis"])
             
            escolhido = rss.escolha(request,dados,material['materiais_disponiveis'],secao)
            index_cond = ResultadosCondutor.selecao_cond(escolhido,rss,material)
            iso_escolhido = rss.escolha(request,dados,material_iso['materiais_disponiveis'],'isolacao_cond')
            
            index_iso = ResultadosCondutor.selecao_iso(iso_escolhido,rss,material_iso)
            coeficiente_seguranca = request.session['resultados'].get(
                "coeficiente_seguranca_bobinas",
                "1.10"
            )

            folga_dados = dados['dados_geometricos']['folga_ranhura']

            folga = request.session['resultados'].get(
                "folga_ran",
                str(folga_dados)
            )
            
            calculoservice = Filtros(dados,iso_sel=iso_escolhido,condutor=escolhido,folga=folga,iso_principal=iso_principal)
            
            resultados = calculoservice.calcular_condutor(coeficiente_seguranca)
            print(resultados)
            return render(request, f"calculos/{secao}.html", {
                    "ordens": iniciar.ordens,
                    "ordem_selecionada": iniciar.ordem_selecionada,
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
    
    def isolamento(self,request):
        secao = 'isolacao'
        fita = 'isolamento_principal'
        request.session['resultados']['pagina_atual'] = "resultados_isolamento"
        
        iniciar = Iniciar(request,secao)
        
        if iniciar.ordem_selecionada is None:
                    return render(request, f"calculos/isolamento.html", {
                                  "ordens": iniciar.ordens,
                                  })
        else:
            rss = iniciar.rss

            dados = DadosMaquinaService(secao).obter_dados(iniciar.ordem_selecionada)
            d_material_s = DadosMaterialService(fita)
            material = d_material_s.obter_dados(iniciar.ordem_selecionada.maquina) 
            
            d_material_cond = DadosMaterialService('condutor')
            condutor = d_material_cond.obter_dados(iniciar.ordem_selecionada.maquina)
                

            d_material_condutiva = DadosMaterialService('fita_condutiva')
            fita_condutiva = d_material_condutiva.obter_dados(iniciar.ordem_selecionada.maquina)

            d_material_semicondutiva = DadosMaterialService('fita_semicondutiva')
            fita_semicondutiva = d_material_semicondutiva.obter_dados(iniciar.ordem_selecionada.maquina)
            
            d_material_acabamento = DadosMaterialService('fita_acabamento')
            fita_acabamento = d_material_acabamento.obter_dados(iniciar.ordem_selecionada.maquina)

            rss.verificar_secao(request, dados,secao,material["materiais_disponiveis"])
            
            opcoes = rss.obter_opcoes_secao( material["materiais_disponiveis"])

            opcoes_fitas = rss.obter_opcoes_secao(fita_condutiva)
            
            if request.method == "POST":
                processar = rss.processar_post(request)

            cond_escolhido = rss.escolha(request,dados,condutor['materiais_disponiveis'],'condutor')
            iso_escolhido = rss.escolha(request,dados,material['materiais_disponiveis'],secao)
            index_iso = ResultadosCondutor.selecao_iso(iso_escolhido,rss,material)

            iso_cond = rss.escolha(request,dados,material['materiais_disponiveis'],'isolacao_cond')
            index_iso = ResultadosCondutor.selecao_iso(iso_escolhido,rss,material)

            fita_condutiva_escolhida = rss.escolha(request,dados,fita_condutiva['materiais_disponiveis'],'fita_condutiva')
            index_fita_condutiva = ResultadosIsolamento.selecao_fita(fita_condutiva_escolhida,rss,fita_condutiva)

            fita_semicondutiva_escolhida = rss.escolha(request,dados,fita_semicondutiva['materiais_disponiveis'],'fita_semicondutiva')
            index_fita_semicondutiva = ResultadosIsolamento.selecao_fita(fita_semicondutiva_escolhida,rss,fita_semicondutiva)

            fita_acabamento_escolhida = rss.escolha(request,dados,fita_acabamento['materiais_disponiveis'],'fita_acabamento')
            index_fita_acabamento = ResultadosIsolamento.selecao_fita(fita_acabamento_escolhida,rss,fita_acabamento)
            
            index_fitas = {
                "index_fita_condutiva": index_fita_condutiva,
                "index_fita_semicondutiva": index_fita_semicondutiva,
                "index_fita_acabamento": index_fita_acabamento,
            }

            folga_dados = dados['dados_geometricos']['folga_ranhura']
            sobreposicao_dados = dados['dados_geometricos']['sobreposicao_isolante']

            coeficiente_seguranca = request.session['resultados'].get(
                "coeficiente_seguranca_isolacao",
                "1.10"
            )
            fator_sobreposicao = str(Decimal(request.session['resultados'].get(
                "sobreposicao",
                str(sobreposicao_dados)
            ))*100)

            coeficiente_seguranca_bobinas = request.session['resultados'].get(
                "coeficiente_seguranca_bobinas",
                "1.10"
            )
            folga = request.session['resultados'].get(
                "folga_ran",
                str(folga_dados)
            )

            fitas = {"fita_condutiva":{"escolhida":fita_condutiva_escolhida, "label": "Fita Condutiva"},
            "fita_semicondutiva": {"escolhida":fita_semicondutiva_escolhida, "label": "Fita Semicondutiva"},
            "fita_acabamento":{"escolhida":fita_acabamento_escolhida, "label": "Fita de Acabamento"}}

            for chave in fitas:
                if fitas[chave]['escolhida'] != None:
                    fitas[chave]['coeficiente_seguranca'] = request.session['resultados'].get(
                        f"coeficiente_seguranca_{chave}",
                        "1.10"
                    )
                    if chave != "fita_condutiva":
                        sobreposicao = "0.30"
                    else:
                        sobreposicao = "0.50"
                    fitas[chave]['sobreposicao'] = str(Decimal(request.session['resultados'].get(
                        f"sobreposicao_{chave}",
                        sobreposicao
                    ))*100)

            resultados = Filtros(dados,
                                 iso_principal=iso_escolhido,
                                 condutor=cond_escolhido,iso_sel=iso_cond,
                                 sobreposicao=fator_sobreposicao,
                                 folga=folga,
                                 fitas=fitas)
            resultados_isolacao = resultados.calcular_isolacao(coeficiente_seguranca)
            resultados_fitas = resultados.calcular_fitas(coeficiente_seguranca)
            
            for chave in fitas:
                if fitas[chave]['escolhida'] != None:
                    fitas[chave]['resultados'] = resultados_fitas[chave]
            
            return render(request, "calculos/isolamento.html", {
                    "ordens": iniciar.ordens,
                    "ordem_selecionada": iniciar.ordem_selecionada,
                    "secao": secao,
                    "opcoes": opcoes,
                    "iso_escolhido": iso_escolhido,
                    "index_iso": str(index_iso),
                    "coeficiente_seguranca": coeficiente_seguranca,
                    "sobreposicao": fator_sobreposicao,
                    "resultados": resultados_isolacao,
                    "fitas":fitas,
                    "opcoes_fitas": opcoes_fitas[1],
                    "index_fitas": index_fitas,
                })

    @staticmethod
    def selecao_fita(fita_escolhida,rss,material_fita):
        if fita_escolhida is None:
            index = "-1"
        elif fita_escolhida == -1:
            index = "-1"
            
        else:
            index = rss.obter_indice_por_id(material_fita['materiais_disponiveis'],fita_escolhida['id'])

        return index

class ResultadosPintura(View):
    @staticmethod
    def pintura(request):
        secao = 'pintura'
        dados = DadosMaquinaService(secao)
        material='verniz_condutivo'

        request.session['resultados']['pagina_atual'] = "resultados_pintura"

        

        iniciar = Iniciar(request,secao)

        if iniciar.ordem_selecionada is None:
            return render(request, f"calculos/isolamento.html", {
                            "ordens": iniciar.ordens,
                            })
        else:
            dados = dados.obter_dados(iniciar.ordem_selecionada)
            d_material_s = DadosMaterialService(material)

            verniz = d_material_s.obter_dados(iniciar.ordem_selecionada.maquina)
            
            dados_verniz = {
                'condutivo':  {},
                'semicondutivo':  {},
                'isolante':  {},
            }
            for tipo in dados_verniz:
                if tipo != "isolante": #retirar esse if quando definir onde será escolhido o verniz isolante
                    opcoes_verniz = DadosMaterialService.separacao_verniz(verniz)[f'opcoes_{tipo}']
                    
                    verniz_escolhido = iniciar.rss.escolha(request,dados,opcoes_verniz,f'verniz_{tipo}')
                    
                    opcoes = iniciar.rss.obter_opcoes_secao(opcoes_verniz)
        
                    index = ResultadosPintura.selecao(verniz_escolhido,iniciar.rss,opcoes_verniz)

                    dados_verniz[tipo] = {
                        "escolhido": verniz_escolhido,
                        "opcoes": opcoes,
                        "index": index,
                    }
            
        return render(request, "calculos/pintura.html", {
                "ordens": iniciar.ordens,
                "ordem_selecionada": iniciar.ordem_selecionada,
                "secao": secao,
                "verniz_escolhido": verniz_escolhido,
                "opcoes_condutivo": opcoes,
                "index_condutivo": index,
                "dados": dados_verniz
            })

    @staticmethod
    def selecao(iso_escolhido,rss,opcoes):
        if iso_escolhido is None:
            index_iso = "-1"
        elif iso_escolhido == -1:
            index_iso = "-1"
            print(f"iso_escolhido: {type(iso_escolhido)}")
        else:
            index_iso = rss.obter_indice_por_id(opcoes,iso_escolhido['id'])

        return index_iso
