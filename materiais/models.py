from decimal import Decimal
from django.core.exceptions import ValidationError
from django.db import models
from cadastros.models import Fornecedor, UnidadeMedida

class ClasseTermica(models.TextChoices):
    Y = "Y", "Classe Y (90 °C)"
    A = "A", "Classe A (105 °C)"
    E = "E", "Classe E (120 °C)"
    B = "B", "Classe B (130 °C)"
    F = "F", "Classe F (155 °C)"
    H = "H", "Classe H (180 °C)"
    N = "N", "Classe N (200 °C)"
    R = "R", "Classe R (220 °C)"
    C = "C", "Classe C (> 220 °C)"

class Material(models.Model):
    class TipoMaterial(models.TextChoices):
        CONDUTOR = "condutor", "Condutor"
        ISOLACAO = "isolacao", "Isolação"
        FITA = "fita", "Fita / Cadarço"
        RESINA_VERNIZ = "resina_verniz", "Resina / Verniz / Massa"
        CORDAO_PAVIO = "cordao_pavio", "Pavio / Camisa / Aro"
        CALCO = "calco", "Calço"
        CUNHA = "cunha", "Cunha"
        SENSOR = "sensor", "Sensor de Temperatura"
        AUXILIAR = "auxiliar", "Material Auxiliar / Conexão"

    TIPO_FIXO = None  # Sobrescrito pelas subclasses

    codigo_material = models.CharField(
        "Código interno",
        max_length=150,
        unique=True,
        null=True,
        blank=True
    )
    codigo_fornecedor = models.CharField(
        "Ref. do fornecedor",
        max_length=150,
        blank=True
    )
    nome = models.CharField("Nome", max_length=150)
    tipo_material = models.CharField(
        "Família / Tipo",
        max_length=30,
        choices=TipoMaterial.choices,
        db_index=True
    )
    descricao = models.TextField("Descrição técnica", blank=True)
    fornecedor = models.ForeignKey(
        Fornecedor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="materiais_v2",
        verbose_name="Fornecedor"
    )
    prioridade = models.PositiveSmallIntegerField(
        "Prioridade",
        default=1,
        help_text="1 = Preferencial"
    )
    preco = models.DecimalField(
        "Preço unitário",
        max_digits=12,
        decimal_places=4,
        null=True,
        blank=True
    )
    unidade_preco = models.ForeignKey(
        UnidadeMedida,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="+",
        verbose_name="Unidade de preço"
    )
    data_atualizacao_preco = models.DateField(
        "Data da cotação",
        null=True,
        blank=True
    )
    ativo = models.BooleanField("Ativo", default=True)
    data_registro = models.DateTimeField("Data de registro", auto_now_add=True)
    data_atualizacao = models.DateTimeField("Última atualização", auto_now=True)

    class Meta:
        verbose_name = "Material"
        verbose_name_plural = "Materiais"
        ordering = ("tipo_material", "prioridade", "nome")
        indexes = [
            models.Index(fields=["codigo_material"]),
            models.Index(fields=["nome"]),
            models.Index(fields=["ativo"]),
        ]

    def __str__(self):
        prefixo = f"[{self.codigo_material}] " if self.codigo_material else ""
        sufixo = f" ({self.fornecedor})" if self.fornecedor else ""
        return f"{prefixo}{self.nome}{sufixo}"

    def clean(self):
        if self.codigo_material is not None:
            self.codigo_material = self.codigo_material.strip().upper() or None
        if self.nome:
            self.nome = self.nome.strip()

    def save(self, *args, **kwargs):
        if self.TIPO_FIXO:
            self.tipo_material = self.TIPO_FIXO
        if self.codigo_material is not None:
            self.codigo_material = self.codigo_material.strip().upper() or None
        super().save(*args, **kwargs)

    @property
    def instancia_especifica(self):
        """Retorna o objeto da subclasse filha correspondente."""
        mapa_relacoes = {
            self.TipoMaterial.CONDUTOR: "condutor",
            self.TipoMaterial.ISOLACAO: "isolacao",
            self.TipoMaterial.FITA: "fita",
            self.TipoMaterial.RESINA_VERNIZ: "resinaverniz",
            self.TipoMaterial.CORDAO_PAVIO: "cordaopavio",
            self.TipoMaterial.CALCO: "calco",
            self.TipoMaterial.CUNHA: "cunha",
            self.TipoMaterial.SENSOR: "sensortemperatura",
            self.TipoMaterial.AUXILIAR: "materialauxiliar",
        }
        relacao = mapa_relacoes.get(self.tipo_material)
        if relacao and hasattr(self, relacao):
            return getattr(self, relacao)
        return self


class Condutor(Material):
    TIPO_FIXO = Material.TipoMaterial.CONDUTOR

    class Forma(models.TextChoices):
        RETANGULAR = "retangular", "Retangular"
        QUADRADO = "quadrado", "Quadrado"
        REDONDO = "redondo", "Redondo"
        ROEBEL = "roebel", "Barra Transposta (Roebel)"

    forma = models.CharField(
        "Forma",
        max_length=20,
        choices=Forma.choices,
        default=Forma.RETANGULAR
    )
    largura_mm = models.DecimalField(
        "Largura cobre nu (mm)",
        max_digits=8,
        decimal_places=3,
        null=True,
        blank=True
    )
    altura_mm = models.DecimalField(
        "Altura cobre nu (mm)",
        max_digits=8,
        decimal_places=3,
        null=True,
        blank=True
    )
    lado_mm = models.DecimalField(
        "Lado cobre nu (mm)",
        max_digits=8,
        decimal_places=3,
        null=True,
        blank=True
    )
    diametro_mm = models.DecimalField(
        "Diâmetro cobre nu (mm)",
        max_digits=8,
        decimal_places=3,
        null=True,
        blank=True
    )
    largura_isolacao_mm = models.DecimalField(
        "Largura com isolação (mm)",
        max_digits=8,
        decimal_places=3,
        null=True,
        blank=True
    )
    altura_isolacao_mm = models.DecimalField(
        "Altura com isolação (mm)",
        max_digits=8,
        decimal_places=3,
        null=True,
        blank=True
    )
    lado_isolacao_mm = models.DecimalField(
        "Lado com isolação (mm)",
        max_digits=8,
        decimal_places=3,
        null=True,
        blank=True
    )
    diametro_isolacao_mm = models.DecimalField(
        "Diâmetro com isolação (mm)",
        max_digits=8,
        decimal_places=3,
        null=True,
        blank=True
    )
    densidade_kg_m3 = models.DecimalField(
        "Densidade (kg/m³)",
        max_digits=10,
        decimal_places=2,
        default=Decimal("8960.00")
    )
    tipo_isolacao = models.CharField(
        "Tipo de isolação",
        max_length=100,
        blank=True,
        help_text="Ex.: Coralglas, Coraltherm HG, Poliglas ER1, Esmaltado"
    )
    classe_termica = models.CharField(
        "Classe térmica",
        max_length=20,
        choices=ClasseTermica.choices,
        blank=True
    )

    class Meta:
        verbose_name = "Condutor"
        verbose_name_plural = "Condutores"

    def clean(self):
        super().clean()
        if self.forma == self.Forma.REDONDO:
            self.largura_mm = None
            self.altura_mm = None
            self.largura_isolacao_mm = None
            self.altura_isolacao_mm = None
            self.lado_mm = None
            self.lado_isolacao_mm = None
        elif self.forma == self.Forma.QUADRADO:
            self.largura_mm = None
            self.altura_mm = None
            self.largura_isolacao_mm = None
            self.altura_isolacao_mm = None
            self.diametro_mm = None
            self.diametro_isolacao_mm = None
        else:
            self.diametro_mm = None
            self.diametro_isolacao_mm = None
            self.lado_mm = None
            self.lado_isolacao_mm = None

    @property
    def area_cobre_mm2(self):
        if self.forma in (self.Forma.RETANGULAR, self.Forma.ROEBEL) and self.largura_mm and self.altura_mm:
            return self.largura_mm * self.altura_mm
        if self.forma == self.Forma.QUADRADO and self.lado_mm:
            return self.lado_mm * self.lado_mm
        if self.forma == self.Forma.REDONDO and self.diametro_mm:
            raio = self.diametro_mm / Decimal("2")
            return Decimal("3.14159265") * raio * raio
        return None

    @property
    def massa_linear_kg_m(self):
        area = self.area_cobre_mm2
        if area and self.densidade_kg_m3:
            return (area * Decimal("0.000001")) * self.densidade_kg_m3
        return None


class Isolacao(Material):
    TIPO_FIXO = Material.TipoMaterial.ISOLACAO

    class Aplicacao(models.TextChoices):
        PRINCIPAL = "principal", "Isolação Principal"
        PANQUECA = "panqueca", "Isolação de Panqueca"
        CONDUTORES = "condutores", "Isolação de Condutores"
        RANHURA = "ranhura", "Forração de Ranhura / Fase"
        GERAL = "geral", "Uso Geral"

    class Substrato(models.TextChoices):
        VIDRO = "vidro", "Mica / Filme de Vidro"
        POLIESTER = "poliester", "Mica / Filme de Poliéster"
        ARAMIDA = "aramida", "Papel Aramida (Nomex)"
        PREPREG_NOMEX = "prepreg_nomex", "Nomex Impregnado (Prepreg)"
        OUTRO = "outro", "Outro"

    aplicacao = models.CharField(
        "Aplicação principal",
        max_length=20,
        choices=Aplicacao.choices,
        default=Aplicacao.PRINCIPAL
    )
    substrato = models.CharField(
        "Substrato / Composição",
        max_length=20,
        choices=Substrato.choices,
        blank=True
    )
    espessura_mm = models.DecimalField(
        "Espessura (mm)",
        max_digits=8,
        decimal_places=3
    )
    largura_mm = models.DecimalField(
        "Largura (mm)",
        max_digits=8,
        decimal_places=2
    )
    comprimento_rolo_m = models.DecimalField(
        "Comprimento do rolo (m)",
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True
    )
    tensao_maxima_kv = models.DecimalField(
        "Tensão nominal máx. (kV)",
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True
    )
    classe_termica = models.CharField("Classe térmica", max_length=20, blank=True)

    class Meta:
        verbose_name = "Isolação"
        verbose_name_plural = "Isolações"


class Fita(Material):
    TIPO_FIXO = Material.TipoMaterial.FITA

    class Finalidade(models.TextChoices):
        CONDUTIVA = "condutiva", "Condutiva"
        SEMICONDUTIVA = "semicondutiva", "Semicondutiva"
        SACRIFICIO = "sacrificio", "Sacrifício / Contração"
        ACABAMENTO = "acabamento", "Acabamento"
        CADARCO = "cadarco", "Cadarço / Amarração"

    finalidade = models.CharField(
        "Finalidade",
        max_length=20,
        choices=Finalidade.choices
    )
    espessura_mm = models.DecimalField(
        "Espessura (mm)",
        max_digits=8,
        decimal_places=3,
        null=True,
        blank=True
    )
    largura_mm = models.DecimalField(
        "Largura (mm)",
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True
    )
    comprimento_rolo_m = models.DecimalField(
        "Comprimento do rolo (m)",
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True
    )
    material_base = models.CharField(
        "Material base",
        max_length=100,
        blank=True,
        help_text="Ex.: Fibra de vidro, Poliéster, Mica"
    )
    classe_termica = models.CharField("Classe térmica", max_length=20, blank=True)

    class Meta:
        verbose_name = "Fita / Cadarço"
        verbose_name_plural = "Fitas e Cadarços"


class ResinaVerniz(Material):
    TIPO_FIXO = Material.TipoMaterial.RESINA_VERNIZ

    class CategoriaQuimica(models.TextChoices):
        RESINA = "resina", "Resina"
        VERNIZ = "verniz", "Verniz / Tinta"
        MASSA = "massa", "Massa de Enchimento / Calafetação"

    class Finalidade(models.TextChoices):
        ISOLANTE = "isolante", "Isolante / Impregnação"
        CONDUTIVO = "condutivo", "Condutivo"
        SEMICONDUTIVO = "semicondutivo", "Semicondutivo"
        CONSOLIDACAO = "consolidacao", "Consolidação de Condutores"
        ENCHIMENTO = "enchimento", "Enchimento / Nivelamento"

    categoria_quimica = models.CharField(
        "Categoria",
        max_length=20,
        choices=CategoriaQuimica.choices
    )
    finalidade = models.CharField(
        "Finalidade",
        max_length=20,
        choices=Finalidade.choices
    )
    rendimento_kg_m = models.DecimalField(
        "Rendimento linear (kg/m)",
        max_digits=10,
        decimal_places=5,
        null=True,
        blank=True
    )
    rendimento_kg_m2 = models.DecimalField(
        "Rendimento superficial (kg/m²)",
        max_digits=10,
        decimal_places=5,
        null=True,
        blank=True
    )
    densidade_kg_m3 = models.DecimalField(
        "Densidade (kg/m³)",
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    proporcao_mistura = models.CharField(
        "Proporção de mistura",
        max_length=100,
        blank=True,
        help_text="Ex.: 100:40 em peso (Componente A:B)"
    )
    temperatura_cura_c = models.PositiveIntegerField(
        "Temperatura de cura (°C)",
        null=True,
        blank=True
    )
    classe_termica = models.CharField("Classe térmica", max_length=20, blank=True)

    class Meta:
        verbose_name = "Resina / Verniz / Massa"
        verbose_name_plural = "Resinas, Vernizes e Massas"


class CordaoPavio(Material):
    TIPO_FIXO = Material.TipoMaterial.CORDAO_PAVIO

    class TipoCordao(models.TextChoices):
        PAVIO = "pavio", "Pavio Central"
        CAMISA = "camisa", "Camisa / Espaguete"
        ARO = "aro", "Cordão para Aro de Amarração"

    tipo = models.CharField(
        "Tipo",
        max_length=20,
        choices=TipoCordao.choices
    )
    material_base = models.CharField(
        "Material base",
        max_length=100,
        default="Fibra de vidro"
    )
    diametro_mm = models.DecimalField(
        "Diâmetro (mm)",
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True
    )
    comprimento_rolo_m = models.DecimalField(
        "Comprimento do rolo (m)",
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = "Pavio / Camisa / Aro"
        verbose_name_plural = "Pavios, Camisas e Aros"


class Calco(Material):
    TIPO_FIXO = Material.TipoMaterial.CALCO

    class TipoCalco(models.TextChoices):
        RADIAL = "radial", "Calço Radial"
        TANGENCIAL = "tangencial", "Calço Tangencial"
        AMARRACAO = "amarracao", "Calço de Amarração"
        FELTRO = "feltro", "Feltro / Manta Compressível"

    tipo_calco = models.CharField(
        "Tipo de calço",
        max_length=20,
        choices=TipoCalco.choices,
        default=TipoCalco.RADIAL
    )
    material_base = models.CharField("Material base", max_length=100, blank=True)
    espessura_mm = models.DecimalField(
        "Espessura (mm)",
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True
    )
    largura_mm = models.DecimalField(
        "Largura (mm)",
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True
    )
    comprimento_mm = models.DecimalField(
        "Comprimento (mm)",
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = "Calço"
        verbose_name_plural = "Calços"


class Cunha(Material):
    TIPO_FIXO = Material.TipoMaterial.CUNHA

    class TipoCunha(models.TextChoices):
        ISOLANTE = "isolante", "Cunha Isolante (TVE / Laminado)"
        MAGNETICA = "magnetica", "Cunha Magnética"
        SUBCUNHA = "subcunha", "Subcunha / Calço de Cunha"
        ONDULADA = "ondulada", "Mola / Cunha Ondulada"

    tipo_cunha = models.CharField(
        "Tipo de cunha",
        max_length=20,
        choices=TipoCunha.choices,
        default=TipoCunha.ISOLANTE
    )
    material_base = models.CharField("Material base", max_length=100, blank=True)
    espessura_mm = models.DecimalField(
        "Espessura (mm)",
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True
    )
    largura_mm = models.DecimalField(
        "Largura (mm)",
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True
    )
    comprimento_mm = models.DecimalField(
        "Comprimento (mm)",
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True
    )
    desenho_referencia = models.CharField(
        "Desenho de referência",
        max_length=100,
        blank=True
    )

    class Meta:
        verbose_name = "Cunha"
        verbose_name_plural = "Cunhas"


class SensorTemperatura(Material):
    TIPO_FIXO = Material.TipoMaterial.SENSOR

    class TipoSensor(models.TextChoices):
        PT100 = "PT100", "PT100"
        PT1000 = "PT1000", "PT1000"
        TERMOPAR = "termopar", "Termopar"
        NTC = "NTC", "NTC / PTC"

    tipo_sensor = models.CharField(
        "Tipo de sensor",
        max_length=20,
        choices=TipoSensor.choices,
        default=TipoSensor.PT100
    )
    numero_fios = models.PositiveSmallIntegerField("Nº de fios", default=3)
    espessura_mm = models.DecimalField(
        "Espessura (mm)",
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True
    )
    largura_mm = models.DecimalField(
        "Largura (mm)",
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True
    )
    comprimento_mm = models.DecimalField(
        "Comprimento do elemento (mm)",
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True
    )
    comprimento_cabo_m = models.DecimalField(
        "Comprimento do cabo (m)",
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = "Sensor de Temperatura"
        verbose_name_plural = "Sensores de Temperatura"


class MaterialAuxiliar(Material):
    TIPO_FIXO = Material.TipoMaterial.AUXILIAR

    class Subtipo(models.TextChoices):
        BARRAMENTO_COBRE = "barramento_cobre", "Barramento / Chapa de Cobre"
        SOLDA_BRASAGEM = "solda_brasagem", "Solda / Liga de Brasagem"
        COMPONENTE_ISOLANTE = "componente_isolante", "Caixa / Componente Isolante"
        CONSUMIVEL_QUIMICO = "consumivel_quimico", "Consumível Químico / Carga"
        DISPOSITIVO_MONTAGEM = "dispositivo_montagem", "Ferramental / Dispositivo de Montagem"
        OUTRO = "outro", "Outro"

    subtipo = models.CharField(
        "Classificação",
        max_length=30,
        choices=Subtipo.choices,
        default=Subtipo.OUTRO
    )
    especificacao_dimensional = models.CharField(
        "Especificação / Dimensões",
        max_length=150,
        blank=True
    )

    class Meta:
        verbose_name = "Material Auxiliar / Conexão"
        verbose_name_plural = "Materiais Auxiliares e Conexões"