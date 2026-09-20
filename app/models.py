from django.core.validators import MinValueValidator
from django.db import models


class Fornecedor(models.Model):
    """Empresa/pessoa que emitiu a nota fiscal."""

    razao_social = models.CharField("Razão Social", max_length=255)
    nome_fantasia = models.CharField("Nome Fantasia", max_length=255, blank=True)
    cnpj = models.CharField("CNPJ", max_length=18, unique=True)

    class Meta:
        verbose_name = "Fornecedor"
        verbose_name_plural = "Fornecedores"
        ordering = ["razao_social"]

    def __str__(self):
        return self.nome_fantasia or self.razao_social


class Faturado(models.Model):
    """Pessoa física para quem a nota fiscal foi emitida."""

    nome_completo = models.CharField("Nome Completo", max_length=255)
    cpf = models.CharField("CPF", max_length=14, unique=True)

    class Meta:
        verbose_name = "Faturado"
        verbose_name_plural = "Faturados"
        ordering = ["nome_completo"]

    def __str__(self):
        return self.nome_completo


class TipoDespesa(models.Model):
    """
    Catálogo de classificações de despesa.

    Cada NotaFiscal usa, por enquanto, apenas uma classificação, mas o
    relacionamento é ManyToMany para já permitir múltiplas classificações
    por registro no futuro, sem precisar alterar a estrutura do banco.
    """

    nome = models.CharField("Classificação de Despesa", max_length=100, unique=True)

    class Meta:
        verbose_name = "Tipo de Despesa"
        verbose_name_plural = "Tipos de Despesa"
        ordering = ["nome"]

    def __str__(self):
        return self.nome


class NotaFiscal(models.Model):
    """Registro principal da nota fiscal/despesa."""

    fornecedor = models.ForeignKey(
        Fornecedor,
        on_delete=models.PROTECT,
        related_name="notas_fiscais",
        verbose_name="Fornecedor",
    )
    faturado = models.ForeignKey(
        Faturado,
        on_delete=models.PROTECT,
        related_name="notas_fiscais",
        verbose_name="Faturado",
    )
    numero = models.CharField("Número da Nota Fiscal", max_length=50)
    data_emissao = models.DateField("Data de Emissão")
    descricao_produtos = models.TextField("Descrição dos Produtos")
    valor_total = models.DecimalField(
        "Valor Total",
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )

    # Estrutura pronta para múltiplas classificações de despesa,
    # embora hoje seja usada apenas uma por registro.
    tipos_despesa = models.ManyToManyField(
        TipoDespesa,
        related_name="notas_fiscais",
        verbose_name="Classificação de Despesa",
    )

    criado_em = models.DateTimeField("Criado em", auto_now_add=True)
    atualizado_em = models.DateTimeField("Atualizado em", auto_now=True)

    class Meta:
        verbose_name = "Nota Fiscal"
        verbose_name_plural = "Notas Fiscais"
        ordering = ["-data_emissao"]
        constraints = [
            models.UniqueConstraint(
                fields=["fornecedor", "numero"],
                name="unique_numero_por_fornecedor",
            )
        ]

    def __str__(self):
        return f"NF {self.numero} - {self.fornecedor}"

    @property
    def quantidade_parcelas(self):
        """Quantidade de parcelas vinculadas a esta nota fiscal."""
        return self.parcelas.count()


class Parcela(models.Model):
    """
    Parcela de pagamento de uma NotaFiscal.

    Hoje o cenário de uso prevê uma única parcela por nota, mas a
    modelagem (FK de Parcela para NotaFiscal) já suporta N parcelas
    sem qualquer alteração estrutural.
    """

    nota_fiscal = models.ForeignKey(
        NotaFiscal,
        on_delete=models.CASCADE,
        related_name="parcelas",
        verbose_name="Nota Fiscal",
    )
    numero_parcela = models.PositiveSmallIntegerField(
        "Número da Parcela", default=1
    )
    data_vencimento = models.DateField("Data de Vencimento")
    valor = models.DecimalField(
        "Valor da Parcela",
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )
    pago = models.BooleanField("Pago", default=False)

    class Meta:
        verbose_name = "Parcela"
        verbose_name_plural = "Parcelas"
        ordering = ["nota_fiscal", "numero_parcela"]
        constraints = [
            models.UniqueConstraint(
                fields=["nota_fiscal", "numero_parcela"],
                name="unique_numero_parcela_por_nota",
            )
        ]

    def __str__(self):
        return f"Parcela {self.numero_parcela} - NF {self.nota_fiscal.numero}"