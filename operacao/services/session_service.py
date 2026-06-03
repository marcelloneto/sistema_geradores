class SessionService:

    @staticmethod
    def obter_os(request):
        return request.session.get("os")

    @staticmethod
    def definir_os(request, os_numero):
        request.session["os"] = os_numero
        request.session.modified = True

    @staticmethod
    def limpar_estator_temp(request):
        request.session.pop("estator_temp", None)
        request.session.modified = True

    @staticmethod
    def salvar_estator_temp(request, dados):
        request.session["estator_temp"] = {
            campo: None if valor is None else str(valor)
            for campo, valor in dados.items()
        }
        request.session.modified = True

    @staticmethod
    def obter_estator_temp(request):
        return request.session.get("estator_temp")

    @staticmethod
    def atualizar_os_anterior(request):
        os_atual = request.session.get("os")
        if os_atual:
            request.session["os_anterior"] = os_atual
            request.session.modified = True

    @staticmethod
    def limpar_temp_se_trocar_os(request, os_numero):
        os_anterior = request.session.get("os_anterior")

        if os_anterior and os_anterior != os_numero:
            SessionService.limpar_estator_temp(request)