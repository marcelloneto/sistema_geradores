from calculos.services.session_service import ResultadosSessionService
from operacao.services.ordem_service import OrdemService
from calculos.services.dados_maquina_service import DadosMaquinaService
from calculos.services.dados_material_service import DadosMaterialService

class Iniciar:
    def __init__(self,request,secao):
        ordemservice = OrdemService("calculos")
        ordens = ordemservice.listar_ordens()
            
        ordem_selecionada = ordemservice.obter_ordem_selecionada(request)

        dados = DadosMaquinaService(secao).obter_dados(ordem_selecionada)
        rss.validar_temp(request)
        d_material_s = DadosMaterialService(secao)
        rss = ResultadosSessionService(secao)
        material = d_material_s.obter_dados(ordem_selecionada.maquina)
        rss.atualizar_pagina(request)
                
        rss.verificar_mudanca_pagina(request)
        
        rss.verificar_secao(request, dados,secao,material["materiais_disponiveis"])
        
        rss.verificar_mudanca_os(request,ordem_selecionada)