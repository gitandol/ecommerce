from django.db import models
from base.functions.image.resize import resize_image


class Produto(models.Model):
    class Meta:
        db_table = "produto"
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'
        ordering = ["nome"]

    CHOICE_TIPO = [
        ['V', 'Variação'],
        ['S', 'Simples'],
    ]

    nome = models.CharField(max_length=100)
    descricao_curta = models.TextField(max_length=255)
    descricao_longa = models.TextField(max_length=255)
    imagem = models.ImageField(upload_to='produto_imagens/%Y/%m/', blank=True, null=True)
    slug = models.SlugField(unique=True)
    preco_marketing = models.FloatField()
    preco_marketing_promocional = models.FloatField()
    tipo = models.CharField(default='V', max_length=1, choices=CHOICE_TIPO)

    def __str__(self):
        return self.nome

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        max_image_size = 800

        if self.imagem:
            status = resize_image(img=self.imagem, new_width=max_image_size)
            print(f'Imagem Redimencionada: {status}')


class Variacao(models.Model):
    class Meta:
        db_table = "variacao"
        verbose_name = 'Variação'
        verbose_name_plural = 'Variações'
        ordering = ["nome"]

    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)  # ao deletar o produto, delata as variações
    nome = models.CharField(max_length=100, blank=True, null=True)
    preco = models.FloatField()
    preco_promocional = models.FloatField(default=0)
    estoque = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.nome or self.produto.nome
