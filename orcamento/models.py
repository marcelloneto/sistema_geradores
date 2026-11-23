from datetime import timedelta
from django.db import models
from django.utils import timezone
from cadastros.models import Cliente, Material


def validade_padrao():
    return timezone.localdate() + timedelta(days=30)


class Orcamento(models.Model):
    class TipoBobina(models.TextChoices):
        BARRA_ROEBEL = "barra_roebel", "Barra Roebel"
        MULTIESPIRAS = "multiespiras", "Bobina Multiespira"

    class TipoBobinado(models.TextChoices):
        IMBRICADO = "imbricado", "Imbricado"
        ONDULADO = "ondulado", "Ondulado"

    class Status(models.TextChoices):
        ATIVO = "ativo", "Ativo"
        APROVADO = "aprovado", "Aprovado"
        REPROVADO = "reprovado", "Reprovado"
        VENCIDO = "vencido", "Vencido"

    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.PROTECT,
        related_name="orcamentos",
        verbose_name="Cliente"
    )

    quantidade_barras = models.PositiveIntegerField(
        "Quantidade de barras / bobinas",
        default=1
    )

    tipo_bobina = models.CharField(
        "Tipo de bobina",
        max_length=20,
        choices=TipoBobina.choices
    )

    tipo_bobinado = models.CharField(
        "Tipo de bobinado",
        max_length=20,
        choices=TipoBobinado.choices,
        blank=True
    )

    status = models.CharField(
        "Status",
        max_length=20,
        choices=Status.choices,
        default=Status.ATIVO
    )

    data_criacao = models.DateTimeField("Data de criação", auto_now_add=True)
    data_atualizacao = models.DateTimeField("Última atualização", auto_now=True)
    data_validade = models.DateField("Validade", default=validade_padrao)

    observacoes = models.TextField("Observações", blank=True)

    class Meta:
        verbose_name = "Orçamento"
        verbose_name_plural = "Orçamentos"
        ordering = ("-data_criacao",)

    @property
    def esta_vencido(self):
        return self.status == self.Status.VENCIDO or (
            self.status == self.Status.ATIVO and self.data_validade < timezone.localdate()
        )

    def __str__(self):
        return f"ORC-{self.id:04d} | {self.cliente.nome}"


class DadosGeometricosRoebel(models.Model):
    class TipoParametroRanhura(models.TextChoices):
        FOLGA = "folga", "Folga na ranhura"
        ISOLACAO = "isolacao", "Espessura da isolação"

    orcamento = models.OneToOneField(
        Orcamento,
        on_delete=models.CASCADE,
        related_name="dados_roebel"
    )

    # --- BARRA DE FUNDO ---
    fundo_a = models.DecimalField("Fundo - Cabeceira superior A (mm)", max_digits=10, decimal_places=2, null=True, blank=True)
    fundo_b = models.DecimalField("Fundo - Cabeceira inferior B (mm)", max_digits=10, decimal_places=2, null=True, blank=True)
    fundo_c = models.DecimalField("Fundo - Ponta exposta inferior C (mm)", max_digits=10, decimal_places=2, null=True, blank=True)
    fundo_d = models.DecimalField("Fundo - Ponta exposta superior D (mm)", max_digits=10, decimal_places=2, null=True, blank=True)
    fundo_l = models.DecimalField("Fundo - Comprimento parte reta L (mm)", max_digits=10, decimal_places=2, null=True, blank=True)

    fundo_num_condutores = models.PositiveIntegerField("Fundo - Nº de condutores", null=True, blank=True)
    fundo_num_espiras = models.PositiveIntegerField("Fundo - Nº de espiras", null=True, blank=True)
    fundo_condutores_por_espira = models.PositiveIntegerField("Fundo - Nº de condutores por espira", null=True, blank=True)

    fundo_condutor = models.ForeignKey(
        Material,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="+",
        verbose_name="Condutor - Barra de Fundo"
    )

    # --- BARRA DE TOPO ---
    topo_a = models.DecimalField("Topo - Cabeceira superior A (mm)", max_digits=10, decimal_places=2, null=True, blank=True)
    topo_b = models.DecimalField("Topo - Cabeceira inferior B (mm)", max_digits=10, decimal_places=2, null=True, blank=True)
    topo_c = models.DecimalField("Topo - Ponta exposta inferior C (mm)", max_digits=10, decimal_places=2, null=True, blank=True)
    topo_d = models.DecimalField("Topo - Ponta exposta superior D (mm)", max_digits=10, decimal_places=2, null=True, blank=True)
    topo_l = models.DecimalField("Topo - Comprimento parte reta L (mm)", max_digits=10, decimal_places=2, null=True, blank=True)

    topo_num_condutores = models.PositiveIntegerField("Topo - Nº de condutores", null=True, blank=True)
    topo_num_espiras = models.PositiveIntegerField("Topo - Nº de espiras", null=True, blank=True)
    topo_condutores_por_espira = models.PositiveIntegerField("Topo - Nº de condutores por espira", null=True, blank=True)

    topo_condutor = models.ForeignKey(
        Material,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="+",
        verbose_name="Condutor - Barra de Topo"
    )

    # --- MEDIDAS DA RANHURA (mm) ---
    ranhura_a = models.DecimalField("Ranhura - altura total A (mm)", max_digits=10, decimal_places=2, null=True, blank=True)
    ranhura_b = models.DecimalField("Ranhura - largura B (mm)", max_digits=10, decimal_places=2, null=True, blank=True)
    ranhura_c = models.DecimalField("Ranhura - altura útil C (mm)", max_digits=10, decimal_places=2, null=True, blank=True)
    ranhura_d = models.DecimalField("Ranhura - altura abertura D (mm)", max_digits=10, decimal_places=2, null=True, blank=True)

    tipo_parametro_ranhura = models.CharField(
        "Parâmetro adicional da ranhura",
        max_length=20,
        choices=TipoParametroRanhura.choices,
        default=TipoParametroRanhura.FOLGA
    )
    folga_ranhura = models.DecimalField("Folga na ranhura (mm)", max_digits=10, decimal_places=2, null=True, blank=True)
    espessura_isolacao = models.DecimalField("Espessura da isolação (mm)", max_digits=10, decimal_places=2, null=True, blank=True)

    class Meta:
        verbose_name = "Dados Geométricos Roebel"
        verbose_name_plural = "Dados Geométricos Roebel"

    def __str__(self):
        return f"Geometria Roebel - {self.orcamento}"

class MateriaisOrcamentoRoebel(models.Model):
    orcamento = models.OneToOneField(
        Orcamento,
        on_delete=models.CASCADE,
        related_name="materiais_roebel"
    )

    isolacao_panqueca = models.ForeignKey(Material, on_delete=models.PROTECT, null=True, blank=True, related_name="+")
    consolidacao_condutores = models.ForeignKey(Material, on_delete=models.PROTECT, null=True, blank=True, related_name="+")
    massa_enchimento = models.ForeignKey(Material, on_delete=models.PROTECT, null=True, blank=True, related_name="+")
    isolacao_condutores = models.ForeignKey(Material, on_delete=models.PROTECT, null=True, blank=True, related_name="+")
    isolacao_principal = models.ForeignKey(Material, on_delete=models.PROTECT, null=True, blank=True, related_name="+")
    fita_sacrificio = models.ForeignKey(Material, on_delete=models.PROTECT, null=True, blank=True, related_name="+")
    verniz_condutivo = models.ForeignKey(Material, on_delete=models.PROTECT, null=True, blank=True, related_name="+")
    fita_condutiva = models.ForeignKey(Material, on_delete=models.PROTECT, null=True, blank=True, related_name="+")
    verniz_semicondutivo = models.ForeignKey(Material, on_delete=models.PROTECT, null=True, blank=True, related_name="+")
    fita_semicondutiva = models.ForeignKey(Material, on_delete=models.PROTECT, null=True, blank=True, related_name="+")
    cadarco_fibra_vidro = models.ForeignKey(Material, on_delete=models.PROTECT, null=True, blank=True, related_name="+")
    fita_acabamento = models.ForeignKey(Material, on_delete=models.PROTECT, null=True, blank=True, related_name="+")
    calcos_radiais = models.ForeignKey(Material, on_delete=models.PROTECT, null=True, blank=True, related_name="+")
    calcos_tangenciais = models.ForeignKey(Material, on_delete=models.PROTECT, null=True, blank=True, related_name="+")
    conexoes = models.ForeignKey(Material, on_delete=models.PROTECT, null=True, blank=True, related_name="+")
    barramentos_ligacao = models.ForeignKey(Material, on_delete=models.PROTECT, null=True, blank=True, related_name="+")
    pavio_central = models.ForeignKey(Material, on_delete=models.PROTECT, null=True, blank=True, related_name="+")
    cunhagem = models.ForeignKey(Material, on_delete=models.PROTECT, null=True, blank=True, related_name="+")
    sensor = models.ForeignKey(Material, on_delete=models.PROTECT, null=True, blank=True, related_name="+")
    aros_amarracao = models.ForeignKey(Material, on_delete=models.PROTECT, null=True, blank=True, related_name="+")

    sobressalente_bobinas = models.DecimalField("Sobressalente de bobinas", max_digits=6, decimal_places=2, default=0)
    coeficiente_seguranca_bobinas = models.DecimalField("Coeficiente de segurança", max_digits=6, decimal_places=2, default=1)

    class Meta:
        verbose_name = "Materiais Orçamento Roebel"
        verbose_name_plural = "Materiais Orçamento Roebel"

    def __str__(self):
        return f"Materiais Roebel - {self.orcamento}"