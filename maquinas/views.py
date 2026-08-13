from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.db import transaction
from cadastros.models import (Maquina, DadosEstator, DadosGeometricosMaquina, 
                              DadosPerifericos, DadosConstrutivosBobina, 
                              ResIsolamento, MateriaisBobinagemRoebel)
from .forms import (DadosMaquinaForm, DadosEstatorForm, DadosGeometricosForm, 
                    DadosPerifericosForm, DadosBobinaForm, DadosEnsaiosForm, 
                    MateriaisBobinagemRoebelForm, NovaMaquinaForm)

from cadastros.models import (Maquina, DadosEstator, DadosGeometricosMaquina, 
                              DadosPerifericos, DadosConstrutivosBobina, 
                              ResIsolamento, MateriaisBobinagemRoebel, Cliente, OrdemServico)


class MaquinaListView(View):
    def get(self, request):
        maquinas = Maquina.objects.select_related('cliente').all().order_by('numero_serie')
        clientes = Cliente.objects.all().order_by('nome')
        form_nova_maquina = NovaMaquinaForm()
        
        return render(request, 'maquinas/lista.html', {
            'maquinas': maquinas,
            'clientes': clientes,
            'form_nova_maquina': form_nova_maquina
        })

class ListaOSView(View):
    def get(self, request, pk):
        maquina = get_object_or_404(Maquina, pk=pk)
        
        # Busca todas as Ordens de Serviço vinculadas a esta máquina
        # select_related('cliente') otimiza a consulta ao banco
        ordens = OrdemServico.objects.filter(maquina=maquina).select_related('cliente').order_by('-numero')
        
        return render(request, 'maquinas/lista_os.html', {
            'maquina': maquina,
            'ordens': ordens
        })

class MaquinaHomeView(View):
    def get(self, request, pk):
        maquina = get_object_or_404(Maquina, pk=pk)
        form = DadosMaquinaForm(instance=maquina)
        return render(request, 'maquinas/home.html', {'maquina': maquina, 'form_maquina': form})

    def post(self, request, pk):
        maquina = get_object_or_404(Maquina, pk=pk)
        form = DadosMaquinaForm(request.POST, instance=maquina)
        if form.is_valid():
            form.save()
            return redirect('maquinas:home', pk=maquina.id)
        return render(request, 'maquinas/home.html', {'maquina': maquina, 'form_maquina': form})


class EstatorView(View):
    def get(self, request, pk):
        maquina = get_object_or_404(Maquina, pk=pk)
        dados, _ = DadosEstator.objects.get_or_create(maquina=maquina)
        form = DadosEstatorForm(instance=dados)
        
        context = {
            'maquina': maquina, 'form': form,
            'campos_bobinado': form.obter_bobinado(),
            'campos_nucleo': form.obter_nucleo(),
        }
        return render(request, 'maquinas/estator.html', context)

    def post(self, request, pk):
        maquina = get_object_or_404(Maquina, pk=pk)
        dados = DadosEstator.objects.get(maquina=maquina)
        form = DadosEstatorForm(request.POST, instance=dados)
        if form.is_valid():
            form.save()
            return redirect('maquinas:estator', pk=maquina.id)
        # Em caso de erro, recarrega com os avisos
        return self.get(request, pk)

class GeometricosView(View):
    def get(self, request, pk):
        maquina = get_object_or_404(Maquina, pk=pk)
        dados, _ = DadosGeometricosMaquina.objects.get_or_create(maquina=maquina)
        form = DadosGeometricosForm(instance=dados)
        
        context = {
            'maquina': maquina, 'form': form,
            'campos_ranhura': form.obter_ranhura(), 'campos_bobina': form.obter_bobina(),
            'campos_condutor': form.obter_condutor(), 'campos_calco': form.obter_calco(),
        }
        return render(request, 'maquinas/geometricos.html', context)

    def post(self, request, pk):
        maquina = get_object_or_404(Maquina, pk=pk)
        dados = DadosGeometricosMaquina.objects.get(maquina=maquina)
        form = DadosGeometricosForm(request.POST, instance=dados)
        if form.is_valid():
            form.save()
            return redirect('maquinas:geometricos', pk=maquina.id)
        return self.get(request, pk)

class PerifericosView(View):
    def get(self, request, pk):
        maquina = get_object_or_404(Maquina, pk=pk)
        dados, _ = DadosPerifericos.objects.get_or_create(maquina=maquina)
        form = DadosPerifericosForm(instance=dados)
        context = {
            'maquina': maquina, 'form': form,
            'campos_aro': form.obter_aro(), 'campos_calco': form.obter_n_calco(),
            'campos_obs_calco': form.obter_obs_calco(), 'campos_inferior': form.obter_inferior(),
        }
        return render(request, 'maquinas/perifericos.html', context)

    def post(self, request, pk):
        maquina = get_object_or_404(Maquina, pk=pk)
        dados = DadosPerifericos.objects.get(maquina=maquina)
        form = DadosPerifericosForm(request.POST, instance=dados)
        if form.is_valid():
            form.save()
            return redirect('maquinas:perifericos', pk=maquina.id)
        return self.get(request, pk)

class EnsaiosView(View):
    def get(self, request, pk):
        maquina = get_object_or_404(Maquina, pk=pk)
        dados, _ = ResIsolamento.objects.get_or_create(maquina=maquina)
        form = DadosEnsaiosForm(instance=dados)
        context = {'maquina': maquina, 'form': form, 'campos_parte1': form.obter_parte1(), 'campos_parte2': form.obter_parte2()}
        return render(request, 'maquinas/ensaios.html', context)

    def post(self, request, pk):
        maquina = get_object_or_404(Maquina, pk=pk)
        dados = ResIsolamento.objects.get(maquina=maquina)
        form = DadosEnsaiosForm(request.POST, instance=dados)
        if form.is_valid():
            form.save()
            return redirect('maquinas:ensaios', pk=maquina.id)
        return self.get(request, pk)

class ConstrutivosView(View):
    def get(self, request, pk):
        maquina = get_object_or_404(Maquina, pk=pk)
        dados, _ = DadosConstrutivosBobina.objects.get_or_create(maquina=maquina)
        form = DadosBobinaForm(instance=dados)
        
        # Lógica para descobrir o tipo de bobina a partir do Estator
        try:
            estator = DadosEstator.objects.get(maquina=maquina)
            tipo_bobina = estator.tipo_bobina or "barra_roebel"
            tipo_bobinado = estator.tipo_bobinado or "imbricado"
        except DadosEstator.DoesNotExist:
            tipo_bobina = "barra_roebel"
            tipo_bobinado = "imbricado"

        # Montagem dos blocos condicionais
        if tipo_bobina == "barra_roebel":
            if tipo_bobinado == "ondulado":
                croqui = {"titulo": "Croqui", "campos": form.obter_croqui(), "caminho_imagem": "operacao/img/croqui_roebel_ondulado.png"}
                amarracao = {"titulo": "Amarração", "campos": form.obter_amarracao(), "caminho_imagem": "operacao/img/amarracao_roebel_ondulado.png"}
            else: # imbricado
                croqui = {"titulo": "Croqui", "campos": form.obter_croqui(), "caminho_imagem": "operacao/img/croqui_roebel_imbricado.png"}
                amarracao = {"titulo": "Amarração", "campos": form.obter_amarracao(), "caminho_imagem": "operacao/img/amarracao_roebel_imbricado.png"}
            
            configuracao = {"titulo": "Configuração", "campos": form.obter_configuracao(), "caminho_imagem": "operacao/img/configuracao.png"}
            montada = {"titulo": "Bobina Montada", "campos": form.obter_montada(), "caminho_imagem": "operacao/img/montada.png"}
            
        else: # multiespiras
            croqui = {"titulo": "Croqui", "campos": form.obter_croqui(), "caminho_imagem": "operacao/img/croqui_multiespiras.png"}
            amarracao = {"titulo": "Amarração", "campos": form.obter_amarracao(), "caminho_imagem": "operacao/img/amarracao_multiespiras.png"}
            configuracao = {"titulo": "Configuração", "campos": form.obter_configuracao(), "caminho_imagem": "operacao/img/configuracao.png"}
            montada = {"titulo": "Bobina Montada", "campos": form.obter_montada(), "caminho_imagem": "operacao/img/montada.png"}

        context = {
            'maquina': maquina, 
            'form': form,
            'secoes': [croqui, amarracao, configuracao, montada]
        }
        return render(request, 'maquinas/construtivos.html', context)

    def post(self, request, pk):
        maquina = get_object_or_404(Maquina, pk=pk)
        dados = DadosConstrutivosBobina.objects.get(maquina=maquina)
        form = DadosBobinaForm(request.POST, instance=dados)
        
        if form.is_valid():
            form.save()
            return redirect('maquinas:construtivos', pk=maquina.id)
        
        # Em caso de erro, recarrega a view GET para mostrar as mensagens
        return self.get(request, pk)


class BobinagemRoebelView(View):
    def get(self, request, pk):
        maquina = get_object_or_404(Maquina, pk=pk)
        dados, _ = MateriaisBobinagemRoebel.objects.get_or_create(maquina=maquina)
        form = MateriaisBobinagemRoebelForm(instance=dados)
        
        context = {
            'maquina': maquina,
            'form': form,
            'campos_condutor_isolamento': form.obter_condutor_isolamento(),
            'campos_resinas': form.obter_resinas(),
            'campos_condutivo': form.obter_condutivo(),
            'campos_semicondutivo': form.obter_semicondutivo(),
            'campos_acabamento': form.obter_acabamento(),
            'campos_componentes': form.obter_componentes(),
            'campos_parametros': form.obter_parametros(),
        }
        return render(request, 'maquinas/bobinagem_roebel.html', context)

    def post(self, request, pk):
        maquina = get_object_or_404(Maquina, pk=pk)
        dados = MateriaisBobinagemRoebel.objects.get(maquina=maquina)
        form = MateriaisBobinagemRoebelForm(request.POST, instance=dados)
        
        if form.is_valid():
            form.save()
            return redirect('maquinas:bobinagem_roebel', pk=maquina.id)
            
        return self.get(request, pk)

class NovaMaquinaView(View):
    @transaction.atomic
    def post(self, request):
        form = NovaMaquinaForm(request.POST)
        if form.is_valid():
            # 1. Salva a nova máquina
            maquina = form.save()

            # 2. Inicializa automaticamente os registros de engenharia em branco
            DadosEstator.objects.get_or_create(maquina=maquina)
            DadosPerifericos.objects.get_or_create(maquina=maquina)
            DadosGeometricosMaquina.objects.get_or_create(maquina=maquina)
            DadosConstrutivosBobina.objects.get_or_create(maquina=maquina)
            ResIsolamento.objects.get_or_create(maquina=maquina)
            MateriaisBobinagemRoebel.objects.get_or_create(maquina=maquina)

            # 3. Redireciona DIRETAMENTE para o prontuário da máquina criada!
            return redirect('maquinas:home', pk=maquina.id)

        # Se houver erro de validação, recarrega a lista
        return redirect('maquinas:lista')

class DeletarMaquinaView(View):
    def post(self, request, pk):
        # TODO: No futuro, validar permissões do usuário aqui (ex: if not request.user.has_perm(...))
        maquina = get_object_or_404(Maquina, pk=pk)
        maquina.delete()
        return redirect('maquinas:lista')