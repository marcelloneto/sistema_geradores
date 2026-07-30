


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

    def verificar_secao(self,request,dados,secao,material):
        """verifica se já existe valor temporário para a seção"""
        
        if f'{secao}_selecionado' in request.session['resultados']:
            pass
        else:
            if secao == 'isolacao_cond':
                request.session['resultados'][f'{secao}_selecionado'] = self.obter_indice_por_id(material,dados['dados_bobinagem_roebel']['isolacao_condutores'])
            elif secao == 'isolacao':
                request.session['resultados'][f'{secao}_selecionado'] = self.obter_indice_por_id(material,dados['dados_bobinagem_roebel']['isolacao_principal'])
            else:
                request.session['resultados'][f'{secao}_selecionado'] = self.obter_indice_por_id(material,dados['dados_bobinagem_roebel'][secao])

    def obter_opcoes_secao(self, material):
        """obtém as opções de materiais disponíveis para utilização e retorna em lista"""

        opcoes = []
        for opcao in material:
            opcoes.append(material[opcao])
        return opcoes

    def processar_post(self,request):
        """processa o evento para atualizar os dados do materiais"""
        #print(f"POST: {request.POST}")
        if "condutor_1" in request.POST:
            acao = request.POST.get("acao")
            secao = request.POST.get(f"{self.secao}_1")
            coeficiente = request.POST.get("coeficiente_seguranca")
            iso = request.POST.get("iso_espiras")
            folga = request.POST.get("folga_ran")
            
            request.session['resultados'][f'{self.secao}_selecionado'] = int(secao)
            request.session['resultados']['coeficiente_seguranca_bobinas'] = coeficiente
            request.session['resultados']['isolacao_selecionado'] = iso
            request.session['resultados']['folga_ran'] = folga

            return {
                'condutor': int(secao),
                'iso_espiras': iso,
                'folga_ranhura': folga,
                'coeficiente_seguranca': coeficiente,
                }

        if "isolacao_principal" in request.POST:
            coeficiente = request.POST.get("coeficiente_seguranca")
            iso = request.POST.get("isolacao_principal")
            sobreposicao = request.POST.get("sobreposicao")
            

            print(f"Sobreposição: {sobreposicao}")

            request.session['resultados']['isolacao_selecionado'] = iso
            request.session['resultados']['coeficiente_seguranca_isolacao'] = coeficiente
            request.session['resultados']['sobreposicao'] = str(float(sobreposicao)/100)
            


        if "fita_condutiva" in request.POST:
            fita_condutiva = request.POST.get("fita_condutiva")
            sobreposicao_fita_condutiva = request.POST.get("sobreposicao_fita_condutiva")
            coeficiente_seguranca_fita_condutiva = request.POST.get("coeficiente_seguranca_fita_condutiva")

            

            request.session['resultados']['fita_condutiva_selecionado'] = fita_condutiva
            request.session['resultados']['sobreposicao_fita_condutiva'] = str(float(sobreposicao_fita_condutiva)/100)
            request.session['resultados']['coeficiente_seguranca_fita_condutiva'] = coeficiente_seguranca_fita_condutiva


        if "fita_semicondutiva" in request.POST:
            fita_semicondutiva = request.POST.get("fita_semicondutiva")
            sobreposicao_fita_semicondutiva = request.POST.get("sobreposicao_fita_semicondutiva")
            coeficiente_seguranca_fita_semicondutiva = request.POST.get("coeficiente_seguranca_fita_semicondutiva")
            

            
            request.session['resultados']['fita_semicondutiva_selecionado'] = fita_semicondutiva
            request.session['resultados']['sobreposicao_fita_semicondutiva'] = str(float(sobreposicao_fita_semicondutiva)/100)
            request.session['resultados']['coeficiente_seguranca_fita_semicondutiva'] = coeficiente_seguranca_fita_semicondutiva

        if "fita_acabamento" in request.POST:
            fita_acabamento = request.POST.get("fita_acabamento")
            sobreposicao_fita_acabamento = request.POST.get("sobreposicao_fita_acabamento")
            coeficiente_seguranca_fita_acabamento = request.POST.get("coeficiente_seguranca_fita_acabamento")
            

            request.session['resultados']['fita_acabamento_selecionado'] = fita_acabamento
            request.session['resultados']['sobreposicao_fita_acabamento'] = str(float(sobreposicao_fita_acabamento)/100)
            request.session['resultados']['coeficiente_seguranca_fita_acabamento'] = coeficiente_seguranca_fita_acabamento

        if "verniz_condutivo" in request.POST:
            verniz_condutivo = request.POST.get("verniz_condutivo")
            
            request.session['resultados']['verniz_condutivo_selecionado'] = verniz_condutivo
            #print(f"Verniz Condutivo: {request.session['resultados']['verniz_condutivo_selecionado']}")

        if "verniz_semicondutivo" in request.POST:
            verniz_semicondutivo = request.POST.get("verniz_semicondutivo")
            
            request.session['resultados']['verniz_semicondutivo_selecionado'] = verniz_semicondutivo
            #print(f"Verniz SemiCondutivo: {request.session['resultados']['verniz_semicondutivo_selecionado']}")
           

        

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

    def verificar_dados(self,request,dados,material,secao):
        
        if 'dados_bobinagem_roebel' in dados:
            if secao == 'isolacao_cond':
                material_1 = dados['dados_bobinagem_roebel']['isolacao_condutores']
            elif secao == 'isolacao':
                material_1 = dados['dados_bobinagem_roebel']['isolacao_principal']
            elif secao == 'condutor':
                material_1 = dados['dados_bobinagem_roebel'][secao]
            elif secao == 'fita_condutiva':
                material_1 = dados['dados_bobinagem_roebel'][secao]
            elif secao == 'fita_semicondutiva':
                material_1 = dados['dados_bobinagem_roebel'][secao]
            elif secao == 'fita_acabamento':
                material_1 = dados['dados_bobinagem_roebel'][secao]
            else:
                material_1 = dados['dados_bobinagem_roebel'][secao]
            
            selecionado = self.obter_indice_por_id(material,material_1)
            
            if material_1 is None:
                return None
            else:
                if selecionado is None:
                    selecionado = "0"
                
                escolhido = material[str(int(selecionado))]
                
                return escolhido

    def escolha(self,request,dados,material,secao):
        
        
        if f'{secao}_selecionado' in request.session['resultados']:
            
            selecionado = request.session['resultados'][f'{secao}_selecionado']
            
            if request.session['resultados'][f'{secao}_selecionado'] is None:
                escolhido = material['0']
            else:
                if selecionado == "-1":
                    escolhido = int(selecionado)
                else:
                    escolhido = material[str(int(selecionado))]
                #print(f"ESCOLHA: {secao}")
        else:
            
            escolhido = self.verificar_dados(request, dados,material,secao)
        
        
        return escolhido

    @staticmethod
    def obter_indice_por_id(materiais, id_material):
        
        if id_material is None:
            return "1"
        for indice, material in materiais.items():
            
            if material["id"] == id_material:
                #print(f"obter_indice_por_id materiais: {id_material}")
                return indice
        
        return None

    