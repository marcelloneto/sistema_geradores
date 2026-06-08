# Create your models here.
from django.db import models


class Fornecedor(models.Model):
    
    nome = models.CharField("Nome", max_length=150, unique=True)

    razao_social = models.CharField(
        "Razão Social",
        max_length=200,
        blank=True
    )

    cnpj = models.CharField(
        "CNPJ",
        max_length=20,
        blank=True
    )

    email = models.EmailField(
        "E-mail",
        max_length=150,
        blank=True
    )

    telefone = models.CharField(
        "Telefone",
        max_length=50,
        blank=True
    )

    site = models.URLField(
        "Site",
        max_length=200,
        blank=True
    )

    observacoes = models.TextField(
        "Observações",
        blank=True
    )

    ativo = models.BooleanField(
        "Ativo",
        default=True
    )

    data_registro = models.DateTimeField(
        "Data de Registro",
        auto_now_add=True
    )

    data_atualizacao = models.DateTimeField(
        "Última Atualização",
        auto_now=True
    )

    class Meta:
        verbose_name = "Fornecedor"
        verbose_name_plural = "Fornecedores"

    def __str__(self):
        return self.nome

class Cliente(models.Model):
    nome = models.CharField(max_length=150, unique=True)
    localizacao = models.CharField(max_length=200, blank=True)

    meio_contato_1 = models.CharField(max_length=50, blank=True)
    contato_1 = models.CharField(max_length=150, blank=True)

    meio_contato_2 = models.CharField(max_length=50, blank=True)
    contato_2 = models.CharField(max_length=150, blank=True)

    data_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"

class OrdemServico(models.Model):
    numero = models.CharField(max_length=50, unique=True)

    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.PROTECT,
        related_name="ordens_servico"
    )

    maquina = models.ForeignKey(
        "Maquina",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="ordens_servico"
    )

    localizacao = models.CharField(max_length=200, blank=True)
    tipo_servico = models.CharField(max_length=100, blank=True)
    data_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.numero
    
    class Meta:
        verbose_name = "Ordem de Serviço"
        verbose_name_plural = "Ordens de Serviço"

class CategoriaMaterial(models.Model):
    nome = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nome
    class Meta:
        verbose_name = "Categoria de Material"
        verbose_name_plural = "Categorias de Material"

class UnidadeMedida(models.Model):
    nome = models.CharField("Nome", max_length=50)

    simbolo = models.CharField(
        "Símbolo",
        max_length=20,
        unique=True
    )

    grandeza = models.CharField(
        "Grandeza",
        max_length=50
    )

    fator_base = models.DecimalField(
        "Fator para unidade base",
        max_digits=20,
        decimal_places=10,
        default=1
    )

    ativa = models.BooleanField("Ativa", default=True)

    class Meta:
        verbose_name = "Unidade"
        verbose_name_plural = "Unidades"

    def __str__(self):
        return self.simbolo

class Maquina(models.Model):
    class Tipo(models.TextChoices):
        HORIZONTAL = "horizontal", "Horizontal"
        VERTICAL = "vertical", "Vertical"

    numero_serie = models.CharField(
        "Nº de série",
        max_length=100,
        unique=True,
    )

    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='dados_maquina'
    )

    tipo = models.CharField(
        "Tipo",
        max_length=20,
        choices=Tipo.choices,
        default=Tipo.VERTICAL
    )

    potencia_kva = models.DecimalField("Potência (kVA)", max_digits=12, decimal_places=2, null=True, blank=True)
    tensao_v = models.DecimalField("Tensão (V)", max_digits=12, decimal_places=2, null=True, blank=True)
    corrente_a = models.DecimalField("Corrente (A)", max_digits=12, decimal_places=2, null=True, blank=True)

    rotacao_rpm = models.DecimalField("Rotação (rpm)", max_digits=10, decimal_places=2, null=True, blank=True)
    numero_polos = models.PositiveIntegerField("Nº de polos", null=True, blank=True)
    fator_potencia = models.DecimalField("Fator de potência", max_digits=5, decimal_places=2, null=True, blank=True)

    excitatriz = models.CharField("Excitatriz", max_length=100, blank=True)
    tensao_excitatriz_v = models.DecimalField("Tensão da excitatriz (V)", max_digits=12, decimal_places=2, null=True, blank=True)
    corrente_excitatriz_a = models.DecimalField("Corrente da excitatriz (A)", max_digits=12, decimal_places=2, null=True, blank=True)

    frequencia_hz = models.DecimalField("Frequência (Hz)", max_digits=8, decimal_places=2, default=60)

    data_registro = models.DateTimeField("Data de registro", auto_now_add=True)
    data_atualizacao = models.DateTimeField("Última atualização", auto_now=True)

    class Meta:
        verbose_name = "Máquina"
        verbose_name_plural = "Máquinas"

    def __str__(self):
        return self.numero_serie

class Material(models.Model):
    codigo_material = models.CharField(max_length=150,null=True)
    
    nome = models.CharField(max_length=150)

    categoria = models.ForeignKey(
        CategoriaMaterial,
        on_delete=models.PROTECT,
        related_name="materiais"
    )

    descricao = models.CharField(max_length=150,blank=True,null=True)

    fornecedor = models.ForeignKey(
        Fornecedor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="materiais"
    )

    prioridade = models.PositiveIntegerField(null=True,blank=True)

    preco = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    unidade_preco = models.ForeignKey(
        UnidadeMedida,
        null=True,
        blank=True,
        on_delete=models.PROTECT
    )

    ativo = models.BooleanField(default=True)
    data_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nome} - {self.fornecedor}"
    
    class Meta:
        verbose_name = "Matéria Prima"
        verbose_name_plural = "Matérias Primas"

class MaterialPropriedade(models.Model):
    material = models.ForeignKey(
        Material,
        on_delete=models.CASCADE,
        related_name="propriedades"
    )

    nome = models.CharField(max_length=100)
    valor = models.CharField(max_length=150)
    unidade = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return f"{self.material} - {self.nome}"
    
    class Meta:
        verbose_name = "Propriedade do Material"
        verbose_name_plural = "Propriedades dos Materiais"

class DadosEstator(models.Model):
    TIPOS_BOBINA = [
        ("barra_roebel", "Barras Roebel"),
        ("multiespiras", "Bobinas Multiespiras")
    ]

    TIPOS_BOBINADO = [
            ("ondulado", "Ondulado"),
            ("imbricado", "Imbricado")
        ]


    maquina = models.OneToOneField(
        Maquina,
        on_delete=models.CASCADE,
        related_name="dados_estator"
    )

    tipo_bobina = models.CharField("Tipo bobina", max_length=100, choices=TIPOS_BOBINA, blank=True)
    tipo_bobinado = models.CharField("Tipo bobinado", max_length=100, choices=TIPOS_BOBINADO, blank=True)
    numero_bobinas = models.PositiveIntegerField("Nº de bobinas", null=True, blank=True)
    numero_condutores_por_espira = models.PositiveIntegerField("Nº cond./espira", null=True, blank=True)
    numero_espiras_por_bobina = models.PositiveIntegerField("Nº de espiras/bobina", null=True, blank=True)

    numero_series = models.PositiveIntegerField("Nº séries", null=True, blank=True)
    tipo_condutor = models.CharField("Tipo condutor", max_length=100, blank=True)
    numero_elementos = models.PositiveIntegerField("Nº de elementos", null=True, blank=True)
    numero_saidas = models.PositiveIntegerField("Nº saídas", null=True, blank=True)
    numero_paralelos = models.PositiveIntegerField("Nº paralelo", null=True, blank=True)

    tipo_ligacao = models.CharField("Tipo de ligação", max_length=20, blank=True)
    numero_sensores = models.PositiveIntegerField("Nº sensor", null=True, blank=True)
    tipo_cunha = models.CharField("Tipo de cunha", max_length=100, blank=True)

    passo = models.PositiveIntegerField("Passo", null=True, blank=True)
    tipo_sensor = models.CharField("Tipo de sensor", max_length=100, blank=True)
    local_sensor = models.CharField("Local do sensor", max_length=100, blank=True)

    peso_cobre_total = models.DecimalField("Peso cobre total", max_digits=12, decimal_places=2, null=True, blank=True)
    peso_bobina = models.DecimalField("Peso bobina", max_digits=12, decimal_places=2, null=True, blank=True)
    area_espira = models.DecimalField("Área da espira", max_digits=12, decimal_places=2, null=True, blank=True)

    comprimento_nucleo_magnetico = models.DecimalField("Comprimento do núcleo magnético", max_digits=12, decimal_places=2, null=True, blank=True)
    numero_canais_ventilacao = models.PositiveIntegerField("Nº canais de ventilação", null=True, blank=True)

    diametro_interno_nucleo = models.DecimalField("Diâmetro interno do núcleo", max_digits=12, decimal_places=2, null=True, blank=True)
    diametro_externo_nucleo = models.DecimalField("Diâmetro externo do núcleo", max_digits=12, decimal_places=2, null=True, blank=True)
    diametro_rotor = models.DecimalField("Diâmetro do rotor", max_digits=12, decimal_places=2, null=True, blank=True)
    entreferro_gerador = models.DecimalField("Entreferro do gerador", max_digits=12, decimal_places=2, null=True, blank=True)

    cor_estator = models.CharField("Cor do estator", max_length=50, blank=True)

    def __str__(self):
        return f"Dados do Estator da máquina {self.maquina}"

    class Meta:
        verbose_name = "Dados do Estator"
        verbose_name_plural = "Dados do Estator"

class DadosPerifericos(models.Model):
    maquina = models.OneToOneField(
        Maquina,
        on_delete=models.CASCADE,
        related_name="dados_perifericos"
    )

    aro_amarracao_ll = models.PositiveIntegerField("Aro de amarração LL", null=True, blank=True)
    aro_amarracao_lol = models.PositiveIntegerField("Aro de amarração LOL", null=True, blank=True)

    material_aro_ll = models.CharField("Material LL", max_length=150, blank=True)
    material_aro_lol = models.CharField("Material LOL", max_length=150, blank=True)

    calco_amarracao_inferior_ll = models.PositiveIntegerField("Calço amarração inferior LL", null=True, blank=True)
    obs_calco_amarracao_inferior_ll = models.CharField("Observação", max_length=150, blank=True)
    calco_amarracao_inferior_lol = models.PositiveIntegerField("Calço amarração inferior LOL", null=True, blank=True)
    obs_calco_amarracao_inferior_lol = models.CharField("Observação", max_length=150, blank=True)

    calco_amarracao_superior_ll = models.PositiveIntegerField("Calço amarração superior LL", null=True, blank=True)
    obs_calco_amarracao_superior_ll = models.CharField("Observação", max_length=150, blank=True)
    calco_amarracao_superior_lol = models.PositiveIntegerField("Calço amarração superior LOL", null=True, blank=True)
    obs_calco_amarracao_superior_lol = models.CharField("Observação", max_length=150, blank=True)

    material_calcos = models.CharField("Material dos calços", max_length=150, blank=True)
    campo_eletrico = models.DecimalField("Campo elétrico", max_digits=12, decimal_places=2, null=True, blank=True)

    densidade_corrente = models.DecimalField("Densidade de corrente", max_digits=12, decimal_places=2, null=True, blank=True)
    tensao_cabo = models.DecimalField("Tensão do cabo", max_digits=12, decimal_places=2, null=True, blank=True)

    classe_termica_cabo = models.CharField("Classe térmica do cabo", max_length=100, blank=True)
    comprimento_cabo_interno = models.CharField("Comprimento do cabo interno", max_length=100, blank=True)

    descricao_terminal = models.CharField("Descrição do terminal", max_length=150, blank=True)
    comprimento_cabo_externo = models.CharField("Comprimento do cabo externo", max_length=100, blank=True)

    data_registro = models.DateTimeField("Data de registro", auto_now_add=True)
    data_atualizacao = models.DateTimeField("Última atualização", auto_now=True)

    class Meta:
        verbose_name = "Dados Periféricos"
        verbose_name_plural = "Dados Periféricos"

    def __str__(self):
        return f"Periféricos - {self.maquina}"
    
class DadosGeometricosMaquina(models.Model):

    tipo_ranhura = [
        ("ranhura1", "Tipo 1"),
        ("ranhura2", "Tipo 2"),
        ("ranhura3", "Tipo 3")
    ]

    tipo_calco = [
            ("calco1", "Tipo 1"),
            ("calco2", "Tipo 2"),
            ("calco3", "Tipo 3"),
            ("calco4", "Tipo 4")
        ]

    maquina = models.OneToOneField(
        Maquina,
        on_delete=models.CASCADE,
        related_name="dados_geometricos"
    )

    # Ranhura
    tipo_ranhura = models.CharField(max_length=50, blank=True, choices=tipo_ranhura)

    ranhura_a = models.DecimalField('a',max_digits=10, decimal_places=2, null=True, blank=True)
    ranhura_b = models.DecimalField('b',max_digits=10, decimal_places=2, null=True, blank=True)
    ranhura_c = models.DecimalField('c',max_digits=10, decimal_places=2, null=True, blank=True)
    ranhura_d = models.DecimalField('d',max_digits=10, decimal_places=2, null=True, blank=True)
    ranhura_e = models.DecimalField('e',max_digits=10, decimal_places=2, null=True, blank=True)
    ranhura_f = models.DecimalField('f',max_digits=10, decimal_places=2, null=True, blank=True)

    # Seção da Bobina
    bobina_e = models.DecimalField('e',max_digits=10, decimal_places=2, null=True, blank=True)
    bobina_f = models.DecimalField('f',max_digits=10, decimal_places=2, null=True, blank=True)
    bobina_g = models.DecimalField('g',max_digits=10, decimal_places=2, null=True, blank=True)
    bobina_h = models.DecimalField('h',max_digits=10, decimal_places=2, null=True, blank=True)

    # Seção do Condutor
    condutor_e = models.DecimalField('e',max_digits=10, decimal_places=2, null=True, blank=True)
    condutor_f = models.DecimalField('f',max_digits=10, decimal_places=2, null=True, blank=True)
    condutor_E_iso = models.DecimalField('E',max_digits=10, decimal_places=2, null=True, blank=True)
    condutor_F_iso = models.DecimalField('F',max_digits=10, decimal_places=2, null=True, blank=True)

    # Calço
    tipo_calco = models.CharField(max_length=50, blank=True, choices=tipo_calco)

    calco_a = models.DecimalField('a',max_digits=10, decimal_places=2, null=True, blank=True)
    calco_b = models.DecimalField('b',max_digits=10, decimal_places=2, null=True, blank=True)
    calco_c = models.DecimalField('c',max_digits=10, decimal_places=2, null=True, blank=True)
    calco_d = models.DecimalField('d',max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"Dados do Geometricos da máquina {self.maquina}"

class DadosConstrutivosBobina(models.Model):
    maquina = models.OneToOneField(
        Maquina,
        on_delete=models.CASCADE,
        related_name="dados_bobina"
    )

    # Croqui
    croqui_g = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    croqui_h = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    croqui_i = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    croqui_j = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    croqui_k = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    croqui_l = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    # Amarração
    amarracao_a1 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    amarracao_a2 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    amarracao_b1 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    amarracao_b2 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    amarracao_c1 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    amarracao_c2 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    amarracao_d1 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    amarracao_d2 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    # Configuração
    configuracao_a1 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    configuracao_a2 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    configuracao_b1 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    configuracao_b2 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    configuracao_c1 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    configuracao_c2 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    configuracao_d1 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    configuracao_d2 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    # Bobina montada
    montada_a = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    montada_b = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    montada_c = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    montada_d = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    montada_e1 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    montada_e2 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    montada_f = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    montada_f_sem_isolacao = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

class MateriaisBobinagemRoebel(models.Model):
    maquina = models.OneToOneField(
        Maquina,
        on_delete=models.CASCADE,
        related_name="dados_bobinagem_roebel"
    )

    condutor = models.ForeignKey(Material, on_delete=models.PROTECT, null=True, blank=True, related_name="+")
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

    sobressalente_bobinas = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    coeficiente_seguranca_bobinas = models.DecimalField(max_digits=6, decimal_places=2, default=1)

    class Meta:
        verbose_name = "Materiais Bobinagem Roebel"
        verbose_name_plural = "Materiais Bobinagem Roebel"

    def __str__(self):
        return f"Materiais Roebel - {self.maquina}"
    
class ResIsolamento(models.Model):

    maquina = models.OneToOneField(
            Maquina,
            on_delete=models.CASCADE,
            related_name="dados_ensaios"
        )

    tensao = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    temperatura = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    umidade = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    tempo = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    Ø01xm = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    Ø02xm = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    Ø03xm = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    Ø04xm = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    res_ohmica_t = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    Ø01 = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    Ø02 = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    Ø03 = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    class Meta:
            verbose_name = "Resistência de isolamento"
            verbose_name_plural = "Resistências de isolamento"
    
    def __str__(self):
        return f"Resistência de Isolamento - {self.maquina}"

    