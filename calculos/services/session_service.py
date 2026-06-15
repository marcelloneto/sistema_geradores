


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

    def verificar_mudanca_pagina(self,request,material):

        """verifica se existiu mudança de página e atualiza os dados temporários"""

        if request.session['resultados']['pagina_atual'] == request.session['resultados']['pagina_anterior']:
            pass
        else:
            request.session['resultados'][f'{self.secao}_selecionado'] = material['material_utilizado']['id']

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

        if request.method == "POST":
            acao = request.POST.get("acao")
            secao = request.POST.get(self.secao)
            request.session['resultados'][f'{self.secao}_selecionado'] = int(secao)
            print(f"Condutor escolhido: {secao}")