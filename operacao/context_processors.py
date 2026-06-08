from .forms import RegistroOSForm, RegistroMaquinaForm, RegistroClienteForm


def formulario_registro_os(request):
    
    return {
        "form_registro_os": RegistroOSForm(),
        "form_cliente": RegistroClienteForm(),
        "registrar_maquina": RegistroMaquinaForm(),
    }