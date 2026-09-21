from django.db import models


class Cliente(models.Model):

    nome = models.CharField(
        max_length=100,
        verbose_name='Nome'
    )

    cpf_cnpj = models.CharField(
        max_length=18,
        unique=True,
        verbose_name='CPF/CNPJ'
    )

    telefone = models.CharField(
        max_length=20,
        verbose_name='Telefone'
    )

    email = models.EmailField(
        blank=True,
        null=True,
        verbose_name='E-mail'
    )

    endereco = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name='Endereço'
    )

    data_cadastro = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Data de cadastro'
    )

    

    def __str__(self):
        return self.nome


class Veiculo(models.Model):

    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.PROTECT,
        related_name='veiculos',
        verbose_name='Cliente',
        null=True,
        blank=True
    )

    TIPOS_VEICULO = [
        ('carro', 'Carro'),
        ('moto', 'Motocicleta'),
        ('caminhao', 'Caminhão'),
    ]

    COMBUSTIVEIS = [
        ('gasolina', 'Gasolina'),
        ('etanol', 'Etanol'),
        ('diesel', 'Diesel'),
        ('flex', 'Flex'),
        ('eletrico', 'Elétrico'),
        ('hibrido', 'Híbrido'),
    ]

    tipo = models.CharField(
        max_length=20,
        choices=TIPOS_VEICULO,
        verbose_name='Tipo'
    )

    marca = models.CharField(
        max_length=100,
        verbose_name='Marca'
    )

    modelo = models.CharField(
        max_length=100,
        verbose_name='Modelo'
    )

    placa = models.CharField(
        max_length=10,
        unique=True,
        verbose_name='Placa'
    )

    ano = models.IntegerField(
        verbose_name='Ano'
    )

    cor = models.CharField(
        max_length=50,
        verbose_name='Cor'
    )

    combustivel = models.CharField(
        max_length=20,
        choices=COMBUSTIVEIS,
        verbose_name='Combustível'
    )

    quilometragem = models.IntegerField(
        default=0,
        verbose_name='Quilometragem'
    )

    observacoes = models.TextField(
        blank=True,
        null=True,
        verbose_name='Observações'
    )

    imagem = models.ImageField(
        upload_to='veiculos/',
        blank=True,
        null=True,
        verbose_name='Imagem do veículo'
    )

    data_cadastro = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Data de cadastro'
    )

    def __str__(self):
        return f'{self.marca} {self.modelo} - {self.placa}'


TIPOS_SERVICO = [
    ("troca_oleo", "Troca de óleo"),
    ("revisao", "Revisão"),
    ("freios", "Sistema de freios"),
    ("suspensao", "Suspensão"),
    ("motor", "Motor"),
    ("eletrica", "Elétrica"),
    ("pneus", "Pneus"),
    ("outros", "Outros"),
]

STATUS_SERVICO = [
    ("aguardando", "Aguardando"),
    ("andamento", "Em andamento"),
    ("concluido", "Concluído"),
    ("cancelado", "Cancelado"),
]


class OrdemServico(models.Model):

    veiculo = models.ForeignKey(
        Veiculo,
        on_delete=models.CASCADE,
        related_name="ordens_servico"
    )

    tipo_servico = models.CharField(
        max_length=50,
        choices=TIPOS_SERVICO
    )

    descricao = models.TextField(
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_SERVICO,
        default="aguardando"
    )

    valor = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    data_entrada = models.DateTimeField(
        auto_now_add=True
    )

    data_conclusao = models.DateTimeField(
        null=True,
        blank=True
    )

    def save(self, *args, **kwargs):

        if self.status == "concluido" and self.data_conclusao is None:
            from django.utils import timezone
            self.data_conclusao = timezone.now()

        if self.status != "concluido":
            self.data_conclusao = None

        super().save(*args, **kwargs)

    def __str__(self):
        return f"OS #{self.id} - {self.veiculo}"


class Contato(models.Model):

    nome = models.CharField(max_length=100)

    email = models.EmailField()

    telefone = models.CharField(max_length=20, blank=True)

    assunto = models.CharField(max_length=150)

    mensagem = models.TextField()

    data_envio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nome} - {self.assunto}"
