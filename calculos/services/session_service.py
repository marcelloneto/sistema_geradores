


class ResultadosSessionService:
    def __init__(self,secao):
        self.secao = secao

    def validar_temp (self,request):
        """valida se existe um estado de resultados na sessão"""

        if "resultados" not in request.session:
            request.session['resultados']={}
        
        
    def atualizar_pagina(self,request):
        """Atualiza os estados de página atual e página anterior"""

        request.session['resultados']['pagina_atual'] = f"resultados_{self.secao}"
        if 'pagina_anterior' in request.session['resultados']:
            pass
        else:
            request.session['resultados']['pagina_anterior'] = f"resultados_{self.secao}"

    def verificar_mudanca_pagina(self,request):

        """verifica se existiu mudança de página e atualiza os dados temporários"""
        
        if request.session['resultados']['pagina_atual'] == request.session['resultados']['pagina_anterior']:
            pass
        else:
            print("verificar mudança: diferente")
            
        request.session['resultados']['pagina_anterior'] = f"resultados_{self.secao}"

    def verificar_secao(self,request,dados):
        """verifica se já existe valor temporário para a seção"""

        if f'{self.secao}_selecionado' in request.session['resultados']:
            pass
        else:
            request.session['resultados'][f'{self.secao}_selecionado'] = dados['dados_bobinagem_roebel'][self.secao]

    def obter_opcoes_secao(self, material):
        """obtém as opções de materiais disponíveis para utilização e retorna em lista"""

        opcoes = []
        for opcao in material['materiais_disponiveis']:
            opcoes.append(opcao)
        return opcoes

    def processar_post(self,request):
        """processa o evento para atualizar os dados do materiais"""

        if "condutor_1" in request.POST:
            acao = request.POST.get("acao")
            secao = request.POST.get(f"{self.secao}_1")
            coeficiente = request.POST.get("coeficiente_seguranca")
            iso = request.POST.get("iso_espiras")
            
            request.session['resultados'][f'{self.secao}_selecionado'] = int(secao)
            request.session['resultados']['coeficiente_seguranca_bobinas'] = coeficiente
            request.session['resultados']['isolacao_selecionado'] = iso
            
            return secao

        if "iso_espiras" in request.POST:
            print("iso_espiras")

    def verificar_mudanca_os (self, request, ordem):
        if 'resultados' in request.session:
            request.session['resultados']['os_atual'] = ordem.numero
        

            if 'os_anterior' in request.session['resultados']:
                os_anterior = request.session['resultados']['os_anterior']

                if os_anterior == ordem.numero:
                    pass

                else:
                    request.session['resultados'] = {}
            
            request.session['resultados']['os_anterior'] = ordem.numero

    def verificar_dados(self,request,dados,material):
        
        if 'dados_bobinagem_roebel' in dados:
            if dados['dados_bobinagem_roebel'][self.secao] is None:
                return None
            else:
                escolhido = material['materiais_disponiveis'][dados['dados_bobinagem_roebel'][self.secao]-1]
                
                return escolhido

    def escolha(self,request,dados,material,secao):
        print(request.session['resultados'][f'{secao}_selecionado'])

        if f'{secao}_selecionado' in request.session['resultados']:
            if request.session['resultados'][f'{secao}_selecionado'] is None:
                escolhido = material['materiais_disponiveis'][0]
            else:
                escolhido = material['materiais_disponiveis'][int(request.session['resultados'][f'{secao}_selecionado'])-1]
        else:
            escolhido = self.verificar_dados(request, dados,material)

        return escolhido