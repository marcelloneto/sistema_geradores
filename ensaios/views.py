from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect
from django.http import JsonResponse
from cadastros.models import Maquina, OrdemServico
from .models import RegistroEnsaio, DadosTensaoAplicada, DadosSurgeTest, DadosBumpTest, TipoEnsaio
from django.db.models import Q
from datetime import datetime
from django.urls import reverse_lazy
from .forms import RegistroEnsaioForm, DadosTensaoAplicadaForm, DadosSurgeTestForm, DadosBumpTestForm, DadosLoopTestForm

class EnsaioListView(ListView):
    model = RegistroEnsaio
    template_name = 'ensaios/lista.html'
    context_object_name = 'ensaios'
    paginate_by = 20  # Adiciona paginação (20 itens por página)

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Captura os parâmetros da URL (Filtros)
        maquina_id = self.request.GET.get('maquina')
        os_numero = self.request.GET.get('os')
        tipo_id = self.request.GET.get('tipo')
        responsavel_id = self.request.GET.get('responsavel')
        data_inicio = self.request.GET.get('data_inicio')
        data_fim = self.request.GET.get('data_fim')

        # Aplica os filtros dinamicamente
        if maquina_id:
            queryset = queryset.filter(maquina_id=maquina_id)
        
        if os_numero:
            queryset = queryset.filter(ordem_servico__numero__icontains=os_numero)
            
        if tipo_id:
            queryset = queryset.filter(tipo_ensaio_id=tipo_id)
            
        if responsavel_id:
            queryset = queryset.filter(responsavel_id=responsavel_id)

        if data_inicio:
            # Converte a string do input type="date" para datetime
            queryset = queryset.filter(data_realizacao__gte=f"{data_inicio} 00:00:00")
            
        if data_fim:
            queryset = queryset.filter(data_realizacao__lte=f"{data_fim} 23:59:59")

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Passa os dados para popular os dropdowns de filtro no HTML
        context['maquinas'] = Maquina.objects.all()
        context['tipos_ensaio'] = TipoEnsaio.objects.all()
        context['responsaveis'] = User.objects.all() # Ou o seu modelo de Funcionário, se houver
        return context


class EnsaioDetailView(DetailView):
    model = RegistroEnsaio
    template_name = 'ensaios/detalhe.html'
    context_object_name = 'ensaio'
    
    # O DetailView envia automaticamente o objeto 'ensaio' para o HTML

class EnsaioCreateView(CreateView):
    model = RegistroEnsaio
    template_name = 'ensaios/form.html'
    form_class = RegistroEnsaioForm  # <-- Use a classe do formulário aqui
    success_url = reverse_lazy('ensaios:lista')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Novo Registro de Ensaio"
        return context

class EnsaioFormMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['form_tensao'] = DadosTensaoAplicadaForm(self.request.POST, instance=getattr(self.object, 'dados_tensao_aplicada', None))
            context['form_surge'] = DadosSurgeTestForm(self.request.POST, instance=getattr(self.object, 'dados_surge_test', None))
            context['form_bump'] = DadosBumpTestForm(self.request.POST, instance=getattr(self.object, 'dados_bump_test', None))
            # Novo form do Loop Test
            context['form_loop'] = DadosLoopTestForm(self.request.POST, instance=getattr(self.object, 'dados_loop_test', None))
        else:
            context['form_tensao'] = DadosTensaoAplicadaForm(instance=getattr(self.object, 'dados_tensao_aplicada', None))
            context['form_surge'] = DadosSurgeTestForm(instance=getattr(self.object, 'dados_surge_test', None))
            context['form_bump'] = DadosBumpTestForm(instance=getattr(self.object, 'dados_bump_test', None))
            # Novo form do Loop Test
            context['form_loop'] = DadosLoopTestForm(instance=getattr(self.object, 'dados_loop_test', None))
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        ensaio = form.save()
        tipo_nome = ensaio.tipo_ensaio.nome.lower()

        # Roteador de salvamento
        if 'tensão' in tipo_nome or 'hipot' in tipo_nome:
            form_esp = context['form_tensao']
        elif 'surge' in tipo_nome:
            form_esp = context['form_surge']
        elif 'bump' in tipo_nome:
            form_esp = context['form_bump']
        elif 'loop' in tipo_nome:
            form_esp = context['form_loop']
        else:
            form_esp = None

        if form_esp and form_esp.is_valid():
            dado_especifico = form_esp.save(commit=False)
            dado_especifico.registro = ensaio
            dado_especifico.save()

        messages.success(self.request, "Ensaio salvo com sucesso!")
        return super().form_valid(form)


class EnsaioCreateView(EnsaioFormMixin, CreateView):
    model = RegistroEnsaio
    form_class = RegistroEnsaioForm
    template_name = 'ensaios/form.html'
    success_url = reverse_lazy('ensaios:lista')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Novo Registro de Ensaio"
        return context


class EnsaioUpdateView(EnsaioFormMixin, UpdateView):
    model = RegistroEnsaio
    form_class = RegistroEnsaioForm
    template_name = 'ensaios/form.html'
    success_url = reverse_lazy('ensaios:lista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = f"Editando Ensaio: {self.object.tipo_ensaio.nome}"
        return context

    # --- ADICIONE ESTE MÉTODO ---
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Desabilita os campos base na página de edição para evitar inconsistências
        form.fields['maquina'].disabled = True
        form.fields['ordem_servico'].disabled = True
        form.fields['tipo_ensaio'].disabled = True
        return form


class EnsaioDeleteView(DeleteView):
    model = RegistroEnsaio
    template_name = 'ensaios/confirmar_exclusao.html'
    success_url = reverse_lazy('ensaios:lista')
    
    def form_valid(self, form):
        messages.success(self.request, "Ensaio excluído com sucesso.")
        return super().form_valid(form)

def carregar_dados_maquina_api(request):
    """
    Endpoint para alimentar o JavaScript com as OSs da Máquina 
    e os dados fixos para o Loop Test.
    """
    maquina_id = request.GET.get('maquina_id')
    
    if not maquina_id:
        return JsonResponse({'ordens': [], 'dados': {}})

    try:
        maquina = Maquina.objects.get(pk=maquina_id)
    except Maquina.DoesNotExist:
        return JsonResponse({'ordens': [], 'dados': {}})

    # Puxar as Ordens de Serviço vinculadas a essa máquina
    ordens_qs = OrdemServico.objects.filter(maquina=maquina).values('id', 'numero')
    
    # Prevenir erro caso a máquina ainda não tenha esses dados preenchidos
    dados_estator = getattr(maquina, 'dados_estator', None)
    dados_geometricos = getattr(maquina, 'dados_geometricos', None)

    # Dicionário com os dados geométricos
    dados_maquina = {
        'diam_ext': dados_estator.diametro_externo_nucleo if dados_estator else '-',
        'diam_int': dados_estator.diametro_interno_nucleo if dados_estator else '-',
        'alt_nuc': dados_estator.comprimento_nucleo_magnetico if dados_estator else '-',
        'canais': dados_estator.numero_canais_ventilacao if dados_estator else '-',
        'ranhura_a': dados_geometricos.ranhura_a if dados_geometricos else '-',
        'ranhura_d': dados_geometricos.ranhura_d if dados_geometricos else '-',
        'frequencia': getattr(maquina, 'frequencia_hz', '-'),
        'fator_potencia': getattr(maquina, 'fator_potencia', '-'),
    }

    return JsonResponse({
        'ordens': list(ordens_qs),
        'dados': dados_maquina
    })