from calculos.services.session_service import ResultadosSessionService
from operacao.services.ordem_service import OrdemService
from calculos.services.dados_maquina_service import DadosMaquinaService
from calculos.services.dados_material_service import DadosMaterialService

class Iniciar:
    def __init__(self,request,secao):
        ordemservice = OrdemService("calculos")

        self.rss = ResultadosSessionService(secao)

        self.ordens = ordemservice.listar_ordens()  

        self.ordem_selecionada = ordemservice.obter_ordem_selecionada(request)

        self.rss.validar_temp(request)

        self.rss.atualizar_pagina(request)
                
        self.rss.verificar_mudanca_pagina(request)
        
        self.rss.verificar_mudanca_os(request,self.ordem_selecionada)

        self.rss.processar_post(request)

        