from django.db import models
from django.contrib.auth.models import User


class Pedido(models.Model):
    class Meta:
        db_table = "pedido"
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'
        ordering = ["pk"]

    CHOICE_STATUS = [
        ['A', 'Aprovado'],
        ['C', 'Criado'],
        ['R', 'Reprovado'],
        ['P', 'Pendente'],
        ['E', 'Enviado'],
        ['F', 'Finalizado']
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.FloatField()
    status = models.CharField(max_length=1, default='C', choices=CHOICE_STATUS)

    def __str__(self):
        return f'Pedido N. {self.pk}'


class ItemPedido(models.Model):
    class Meta:
        db_table = "item_pedido"
        verbose_name = 'Item do Pedido'
        verbose_name_plural = 'Itens do Pedido'
        ordering = ["pedido"]

    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    produto = models.CharField(max_length=100)
    produto_id = models.PositiveIntegerField()
    variacao = models.CharField(max_length=255)
    variacao_id = models.PositiveIntegerField()
    preco = models.FloatField()
    preco_promocional = models.FloatField(default=0)
    imagem = models.CharField(max_length=2000)

    def __str__(self):
        return f'Item do {self.pedido}'
