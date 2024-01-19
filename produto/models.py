from django.db import models
from base.functions.image.resize import crop_image
from django.utils.text import slugify
from base.utils import moeda
from base.models import BaseModel


class Produto(BaseModel):
    class Meta:
        db_table = "produto"
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'
        ordering = ["nome"]

    CHOICE_TIPO = [
        ['V', 'Variável'],
        ['S', 'Simples'],
    ]

    nome = models.CharField(max_length=100)
    descricao_curta = models.TextField(max_length=255)
    descricao_longa = models.TextField(max_length=2500)
    imagem = models.ImageField(upload_to='produto_imagens/%Y/%m/', blank=True, null=True)
    slug = models.SlugField(unique=True, null=True, blank=True, max_length=255)
    preco_marketing = models.FloatField(verbose_name='Preço')
    preco_marketing_promocional = models.FloatField(verbose_name='Preço Promo.')
    tipo = models.CharField(default='V', max_length=1, choices=CHOICE_TIPO)

    def get_preco_formatado(self):
        return moeda.formata(self.preco_marketing)
    get_preco_formatado.short_description = 'Preço'

    def get_preco_promocional_formatado(self):
        return moeda.formata(self.preco_marketing_promocional)
    get_preco_promocional_formatado.short_description = 'Preço Promo.'

    def __str__(self):
        return self.nome

    def save(self, *args, **kwargs):
        slug = None
        if not self.slug and self.pk:
            slug = f'{slugify(self.nome)}-{self.pk}'
            self.slug = slug

        super().save(*args, **kwargs)
        if not slug:
            slug = f'{slugify(self.nome)}-{self.pk}'
            self.slug = slug
            super().save(*args, **kwargs)

        if self.imagem:
            crop_image(img=self.imagem)  # corta imagem para ficar com mesmo width e hight


class Variacao(BaseModel):
    class Meta:
        db_table = "variacao"
        verbose_name = 'Variação'
        verbose_name_plural = 'Variações'
        ordering = ["ordem", "nome"]

    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)  # ao deletar o produto, delata as variações
    nome = models.CharField(max_length=100, blank=True, null=True)
    preco = models.FloatField()
    preco_promocional = models.FloatField(default=0)
    estoque = models.PositiveIntegerField(default=1)
    ordem = models.IntegerField(default=0)

    def __str__(self):
        return self.nome or self.produto.nome
