from django.db.models import Model

class SessionService:
    def __init__(self,secao):
        self.secao = secao
        

    @staticmethod
    def obter_os(request):
        return request.session.get("os")

    @staticmethod
    def definir_os(request, os_numero):
        request.session["os"] = os_numero
        request.session.modified = True
    
    @staticmethod
    def atualizar_os_anterior(request):
        os_atual = request.session.get("os")
        if os_atual:
            request.session["os_anterior"] = os_atual
            request.session.modified = True