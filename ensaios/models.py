from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import User
from cadastros.models import Maquina, OrdemServico

class TipoEnsaio(models.Model):
    nome = models.CharField("Nome do Ensaio", max_length=100, unique=True)
    norma_referencia = models.CharField("Norma de Referência (Ex: IEEE 43)", max_length=100, blank=True)
    descricao = models.TextField("Descrição/Procedimento", blank=True)

    class Meta:
        verbose_name = "Tipo de Ensaio"
        verbose_name_plural = "Tipos de Ensaios"

    def __str__(self):
        return self.nome

class RegistroEnsaio(models.Model):
    # Relacionamentos Obrigatórios
    maquina = models.ForeignKey(
        Maquina, 
        on_delete=models.CASCADE, 
        related_name="ensaios_realizados"
    )
    ordem_servico = models.ForeignKey(
        OrdemServico, 
        on_delete=models.CASCADE, 
        related_name="ensaios_da_os"
    )
    tipo_ensaio = models.ForeignKey(
        TipoEnsaio, 
        on_delete=models.PROTECT, 
        related_name="registros"
    )
    
    # Rastreabilidade
    data_realizacao = models.DateTimeField("Data e Hora da Realização")
    responsavel = models.ForeignKey(
        User, 
        on_delete=models.PROTECT, 
        verbose_name="Responsável Técnico"
    )

    # Resultados e Documentação
    RESULTADO_CHOICES = [
        ('AP', 'Aprovado'),
        ('RP', 'Reprovado'),
        ('AR', 'Aprovado com Ressalvas'),
        ('AN', 'Apenas Análise/Coleta'),
    ]
    resultado_geral = models.CharField(
        "Resultado Geral", 
        max_length=2, 
        choices=RESULTADO_CHOICES, 
        default='AN'
    )
    observacoes = models.TextField("Observações Técnicas", blank=True)
    
    # Anexo do Laudo gerado pelos equipamentos (Megger, Baker, etc.)
    laudo_anexo = models.FileField(
        "Laudo / Relatório (PDF)", 
        upload_to="ensaios/laudos/%Y/%m/", 
        blank=True, 
        null=True
    )

    class Meta:
        verbose_name = "Registro de Ensaio"
        verbose_name_plural = "Registros de Ensaios"
        ordering = ['-data_realizacao']

    def __str__(self):
        return f"{self.tipo_ensaio.nome} - OS: {self.ordem_servico.numero} ({self.get_resultado_geral_display()})"

from django.db import models

# ... (Suas classes TipoEnsaio e RegistroEnsaio ficam aqui em cima) ...

class DadosTensaoAplicada(models.Model):
    """
    Também conhecido como Hipot (High Potential Test).
    Mede a rigidez dielétrica do isolamento.
    """
    registro = models.OneToOneField(
        RegistroEnsaio, 
        on_delete=models.CASCADE, 
        related_name="dados_tensao_aplicada"
    )
    
    # Parâmetros de Entrada
    fase_testada = models.CharField(
        "Fase/Circuito Testado", 
        max_length=50, 
        help_text="Ex: Fase U contra Carcaça, Fases U+V+W contra Carcaça"
    )
    tensao_ensaio_volts = models.PositiveIntegerField("Tensão de Ensaio (V)")
    tempo_aplicacao_segundos = models.PositiveIntegerField("Tempo de Aplicação (s)", default=60)
    
    # Leituras
    corrente_fuga_ma = models.DecimalField(
        "Corrente de Fuga (mA)", 
        max_digits=8, 
        decimal_places=3,
        help_text="Corrente de fuga medida ao final do tempo estabilizado."
    )

    class Meta:
        verbose_name = "Dados de Tensão Aplicada"
        verbose_name_plural = "Dados de Tensão Aplicada"

    def __str__(self):
        return f"Hipot - {self.registro}"


class DadosSurgeTest(models.Model):
    """
    Ensaio de Surto/Impulso.
    Verifica o isolamento entre espiras da mesma bobina/fase.
    """
    registro = models.OneToOneField(
        RegistroEnsaio, 
        on_delete=models.CASCADE, 
        related_name="dados_surge_test"
    )
    
    # Parâmetros
    tensao_pico_volts = models.PositiveIntegerField("Tensão de Pico Aplicada (V)")
    
    # Leituras
    ear_porcentagem = models.DecimalField(
        "EAR - Error Area Ratio (%)", 
        max_digits=5, 
        decimal_places=2,
        help_text="Diferença percentual de área entre as formas de onda.",
        null=True, 
        blank=True
    )
    
    RESULTADO_ONDA_CHOICES = [
        ('SIM', 'Ondas Simétricas / Sobrepostas'),
        ('ASS', 'Ondas Assimétricas / Deslocadas'),
        ('CUR', 'Curto-circuito detectado'),
    ]
    analise_onda = models.CharField(
        "Análise da Forma de Onda", 
        max_length=3, 
        choices=RESULTADO_ONDA_CHOICES
    )

    class Meta:
        verbose_name = "Dados de Surge Test"
        verbose_name_plural = "Dados de Surge Tests"


class DadosBumpTest(models.Model):
    """
    Teste de Impacto / Ressonância.
    Identifica as frequências naturais de vibração (geralmente nas cabeças de bobina).
    """
    registro = models.OneToOneField(
        RegistroEnsaio, 
        on_delete=models.CASCADE, 
        related_name="dados_bump_test"
    )
    
    local_impacto = models.CharField(
        "Local do Impacto/Medição", 
        max_length=100,
        help_text="Ex: Cabeça de bobina lado acoplado - Fase U, Posição 12h"
    )
    
    # Leituras
    frequencia_natural_hz = models.DecimalField(
        "Frequência Natural 1 (Hz)", 
        max_digits=6, 
        decimal_places=2
    )
    frequencia_natural_2_hz = models.DecimalField(
        "Frequência Natural 2 (Hz)", 
        max_digits=6, 
        decimal_places=2, 
        null=True, 
        blank=True
    )
    amortecimento_porcentagem = models.DecimalField(
        "Fator de Amortecimento (%)", 
        max_digits=5, 
        decimal_places=2,
        null=True, 
        blank=True
    )

    class Meta:
        verbose_name = "Dados de Bump Test"
        verbose_name_plural = "Dados de Bump Tests"

class DadosLoopTest(models.Model):
    """
    Ensaio de Fluxo no Núcleo (Loop Test).
    Verifica a integridade da isolação entre chapas magnéticas do estator.
    """
    registro = models.OneToOneField(
        RegistroEnsaio, 
        on_delete=models.CASCADE, 
        related_name="dados_loop_test"
    )
    
    # --- Parâmetros de Configuração do Núcleo (Específicos do Teste) ---
    numero_dutos_ar = models.PositiveIntegerField(
        "Número de Dutos de Ar", 
        default=0
    )
    altura_duto_ar_mm = models.DecimalField(
        "Altura do Duto de Ar (mm)", 
        max_digits=5, 
        decimal_places=2, 
        default=0
    )
    fator_empilhamento = models.DecimalField(
        "Fator de Empilhamento do Núcleo", 
        max_digits=3, 
        decimal_places=2,
        help_text="Ex: 0.95"
    )
    densidade_especifica_laminacao = models.DecimalField(
        "Densidade Específica da Laminação (kg/dm³)", 
        max_digits=4, 
        decimal_places=2,
        help_text="Geralmente 7.65 kg/dm³ para aço silício."
    )
    diametro_furos_chapa_mm = models.DecimalField(
        "Diâmetro dos Furos na Chapa (mm)", 
        max_digits=5, 
        decimal_places=2, 
        default=0
    )
    numero_furos_chapa = models.PositiveIntegerField(
        "Número de Furos na Chapa", 
        default=0
    )
    
    # --- Parâmetros Elétricos do Ensaio ---
    densidade_fluxo_nominal_t = models.DecimalField(
        "Densidade de Fluxo Nominal (Tesla)", 
        max_digits=4, 
        decimal_places=2,
        help_text="Valor alvo para o ensaio (Ex: 1.0 ou 1.4 Tesla)"
    )
    perdas_especificas_chapa = models.DecimalField(
        "Perdas Específicas da Chapa (W/kg)", 
        max_digits=5, 
        decimal_places=2,
        help_text="Referência do fabricante para a chapa siliciosa tipo A"
    )

    class Meta:
        verbose_name = "Dados de Loop Test"
        verbose_name_plural = "Dados de Loop Tests"

    def __str__(self):
        return f"Loop Test - {self.registro}"
        
    # Exemplo de como a engenharia será acessada na View/Service depois:
    # area_ranhura = self.registro.maquina.dados_estator.ranhura_a * self.registro.maquina.dados_estator.ranhura_d
    # O teste lê da máquina, faz o cálculo, e gera o resultado.