

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

    
    def limpar_temp_secao(self,request):
        request.session.pop(f"{self.secao}_temp", None)
        request.session.modified = True

    
    def limpar_temp_(self,request):
        
        request.session.pop(f"{self.secao}_temp", None)
        request.session.modified = True

    
    def salvar_temp_secao(self,request, dados):
        request.session[f"{self.secao}_temp"] = {
            campo: None if valor is None else str(valor)
            for campo, valor in dados.items()
        }
        request.session.modified = True
        

    
    def obter_temp_secao(self,request):
        return request.session.get(f"{self.secao}_temp")

    @staticmethod
    def atualizar_os_anterior(request):
        os_atual = request.session.get("os")
        if os_atual:
            request.session["os_anterior"] = os_atual
            request.session.modified = True

    @staticmethod
    def limpar_temp_se_trocar_os(request, os_numero,):
        os_anterior = request.session.get("os_anterior")
        SECOES  = ["estator","geometricos","isolacao","pintura","ensaios"]
        
        if os_anterior and os_anterior != os_numero:
            print(list(request.session.keys()))
            for secao in SECOES:
                print(secao)
                if f"{secao}_temp" in request.session:
                    print(request.session[f"{secao}_temp"])
                    request.session.pop(f"{secao}_temp", None)