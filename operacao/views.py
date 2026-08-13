from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.http import JsonResponse
from django.urls import reverse_lazy
from cadastros.models import OrdemServico, Maquina, Cliente
from .forms import OrdemServicoForm, RegistroClienteForm, RegistroMaquinaForm

# 1. Página principal de Gestão de Ordens de Serviço
class HomeOSView(View):
    def get(self, request):
        ordens = OrdemServico.objects.select_related('cliente', 'maquina').all().order_by('-id')
        
        # Captura a OS selecionada via parâmetro ?os=NUMERO na URL (se houver)
        os_numero = request.GET.get('os')
        ordem_selecionada = None
        form = None

        if os_numero:
            ordem_selecionada = OrdemServico.objects.filter(numero=os_numero).first()
            if ordem_selecionada:
                form = OrdemServicoForm(instance=ordem_selecionada)

        return render(request, 'operacao/home.html', {
            'ordens': ordens,
            'ordem_selecionada': ordem_selecionada,
            'form': form,
        })

    def post(self, request):
        os_numero = request.GET.get('os')
        if os_numero:
            ordem_selecionada = get_object_or_404(OrdemServico, numero=os_numero)
            form = OrdemServicoForm(request.POST, instance=ordem_selecionada)
            if form.is_valid():
                form.save()
                return redirect(f"{request.path}?os={ordem_selecionada.numero}")
        
        return self.get(request)


# 2. Tela dedicada para Abertura de Nova OS
class NovaOrdemView:
    @staticmethod
    def nova_os(request):
        if request.method == "POST":
            numero = request.POST.get('numero')
            cliente_id = request.POST.get('cliente')
            maquina_id = request.POST.get('maquina')
            tipo_servico = request.POST.get('tipo_servico')
            localizacao = request.POST.get('localizacao', '')
            
            if numero and cliente_id and maquina_id:
                cliente = Cliente.objects.get(id=cliente_id)
                maquina = Maquina.objects.get(id=maquina_id)
                
                nova_os = OrdemServico.objects.create(
                    numero=numero,
                    cliente=cliente,
                    maquina=maquina,
                    tipo_servico=tipo_servico,
                    localizacao=localizacao
                )
                # Redireciona para o painel da OS já selecionando a OS recém-criada
                return redirect(f"{reverse_lazy('operacao:home')}?os={nova_os.numero}")

        clientes = Cliente.objects.all().order_by('nome')
        return render(request, "operacao/nova_os.html", {
            "clientes": clientes
        })


# 3. API JSON para popular máquinas no formulário de criação
class ApiOperacaoView:
    @staticmethod
    def carregar_maquinas_cliente(request):
        cliente_id = request.GET.get('cliente_id')
        if cliente_id:
            maquinas = Maquina.objects.filter(cliente_id=cliente_id).values('id', 'numero_serie')
            return JsonResponse(list(maquinas), safe=False)
        return JsonResponse([], safe=False)


# 4. Ações de Cadastro Rápido / Modais
class Registro:
    @staticmethod
    def registrar_os(request):
        if request.method == "POST":
            form = OrdemServicoForm(request.POST)
            if form.is_valid():
                nova_os = form.save()
                return redirect(f"{reverse_lazy('operacao:home')}?os={nova_os.numero}")
        return redirect(request.META.get("HTTP_REFERER", "operacao:home"))

    @staticmethod
    def registrar_cliente(request):
        if request.method == "POST":
            form = RegistroClienteForm(request.POST)
            if form.is_valid():
                form.save()
        return redirect(request.META.get("HTTP_REFERER", "operacao:home"))

    @staticmethod
    def registrar_maquina(request):
        if request.method == "POST":
            form = RegistroMaquinaForm(request.POST)
            if form.is_valid():
                form.save()
        return redirect(request.META.get("HTTP_REFERER", "operacao:home"))

class DeletarOSView(View):
    def post(self, request, pk):
        # TODO: Reservado para validações futuras de permissões do usuário
        ordem = get_object_or_404(OrdemServico, pk=pk)
        ordem.delete()
        return redirect('listagem:home') # Redireciona para a listagem principal após deletar