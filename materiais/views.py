from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from cadastros.models import Material, CategoriaMaterial, CategoriaMaterialParametro, MaterialParametroValor
from .forms import MaterialForm, ParametroFormSet
from django.http import HttpResponseRedirect

class MaterialListView(ListView):
    model = Material
    template_name = 'materiais/lista.html'
    context_object_name = 'materiais'

    def get_queryset(self):
        queryset = super().get_queryset().select_related('categoria')
        categoria_id = self.request.GET.get('categoria')
        if categoria_id:
            queryset = queryset.filter(categoria_id=categoria_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = CategoriaMaterial.objects.all()
        return context

class MaterialUpdateView(UpdateView):
    model = Material
    form_class = MaterialForm
    template_name = 'materiais/material_form.html'

    def get_success_url(self):
        return reverse('material_editar', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Pega os parâmetros da categoria
        parametros_da_categoria = CategoriaMaterialParametro.objects.filter(
            categoria=self.object.categoria, 
            ativo=True
        )
        
        # Carrega os valores existentes
        valores_db = self.object.parametros_tecnicos.all()
        
        # DEBUG: Vamos ver no console se o Django encontra algo
        print(f"DEBUG: Encontrados {valores_db.count()} valores no banco para o material {self.object.id}")
        for v in valores_db:
            print(f"DEBUG: Valor salvo -> Param ID: {v.parametro_id} | Valor Texto: {v.valor_texto} | Valor Num: {v.valor_numero}")

        # Monta o dicionário de busca
        valores_existentes = {v.parametro_id: v for v in valores_db}
        
        lista_parametros_render = []
        for param in parametros_da_categoria:
            obj_valor = valores_existentes.get(param.id)
            
            num_formatado = ""
            if obj_valor and obj_valor.valor_numero is not None:
                # Formata para 2 casas decimais e converte para string usando ponto
                num_formatado = f"{obj_valor.valor_numero:.2f}".replace(',', '.')

            lista_parametros_render.append({
                'parametro': param,
                'valor_obj': obj_valor,
                'num_str': num_formatado, # String limpa com no máximo 2 casas decimais
            })
            
        context['lista_parametros_render'] = lista_parametros_render
        return context
    
    def form_valid(self, form):
        self.object = form.save()
        
        # Processa os parâmetros salvos ou preenchidos dinamicamente
        parametros_da_categoria = CategoriaMaterialParametro.objects.filter(categoria=self.object.categoria, ativo=True)
        for param in parametros_da_categoria:
            valor_enviado = self.request.POST.get(f'param_dinamico_{param.id}')
            
            if valor_enviado is not None: # Se o campo foi enviado no POST
                v_texto = valor_enviado if param.tipo in ['texto', 'lista'] else ''
                v_numero = valor_enviado if param.tipo == 'numero' and valor_enviado != '' else None
                v_bool = True if (param.tipo == 'checkbox' and valor_enviado == 'on') else False

                # Atualiza ou cria o registro técnico do material
                MaterialParametroValor.objects.update_or_create(
                    material=self.object,
                    parametro=param,
                    defaults={
                        'valor_texto': v_texto,
                        'valor_numero': v_numero,
                        'valor_booleano': v_bool,
                        'unidade': param.unidade
                    }
                )
        return super().form_valid(form)

class MaterialDeleteView(DeleteView):
    model = Material
    template_name = 'materiais/material_confirm_delete.html'
    success_url = reverse_lazy('lista_materiais')

class MaterialCreateView(CreateView):
    model = Material
    template_name = 'materiais/material_form.html'
    fields = ['codigo_material', 'nome', 'categoria', 'descricao', 'fornecedor', 'prioridade', 'preco', 'unidade_preco', 'ativo']
    success_url = reverse_lazy('lista_materiais')

    def get_initial(self):
        # Passa os dados que vieram via GET (parâmetros da URL) para preencher o form automaticamente
        initial = super().get_initial()
        if self.request.GET.get('categoria'):
            initial['categoria'] = self.request.GET.get('categoria')
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Pega a categoria selecionada (seja via GET ao trocar o select, ou inicial)
        categoria_id = self.request.GET.get('categoria')
        
        if not categoria_id and self.object and self.object.categoria_id:
            categoria_id = self.object.categoria_id
            
        parametros_da_categoria = []
        if categoria_id:
            parametros_da_categoria = CategoriaMaterialParametro.objects.filter(
                categoria_id=categoria_id, 
                ativo=True
            )
            
        lista_parametros_render = []
        for param in parametros_da_categoria:
            lista_parametros_render.append({
                'parametro': param,
                'valor_obj': None,
                'num_str': '',
            })
            
        context['lista_parametros_render'] = lista_parametros_render
        return context

    def form_valid(self, form):
        self.object = form.save()
        categoria = self.object.categoria
        if categoria:
            parametros = CategoriaMaterialParametro.objects.filter(categoria=categoria)
            for param in parametros:
                valor_enviado = self.request.POST.get(f'param_{param.id}')
                if valor_enviado:
                    v_texto = valor_enviado if param.tipo in ['texto', 'lista'] else ''
                    v_numero = valor_enviado if param.tipo == 'numero' else None
                    v_bool = True if (param.tipo == 'checkbox' and valor_enviado) else False

                    MaterialParametroValor.objects.create(
                        material=self.object,
                        parametro=param,
                        valor_texto=v_texto,
                        valor_numero=v_numero,
                        valor_booleano=v_bool,
                        unidade=param.unidade
                    )
        return redirect(self.success_url)

class MaterialBulkDeleteView(View):
    def post(self, request, *args, **kwargs):
        ids_selecionados = request.POST.getlist('material_ids')
        if ids_selecionados:
            Material.objects.filter(id__in=ids_selecionados).delete()
        return HttpResponseRedirect(reverse('lista_materiais'))