from django.shortcuts import render
from django.views.generic.list import ListView
from django.views import View
from django.http import HttpResponse
from . import models


class ListaProdutos(ListView):
    model = models.Produto
    template_name = 'produto/lista.html'
    context_object_name = 'produtos'


class DetalheProduto(View):
    def get(self, *args, **kwargs):
        return HttpResponse('DetalheProduto')


class AdicionarAoCarrinhoProduto(View):
    def get(self, *args, **kwargs):
        return HttpResponse('AdicionarAoCarrinhoProduto')


class RemoverDoCarrinhoProduto(View):
    def get(self, *args, **kwargs):
        return HttpResponse('RemoverDoCarrinhoProduto')


class CarrinhoProduto(View):
    def get(self, *args, **kwargs):
        return HttpResponse('CarrinhoProduto')


class FinalizarProduto(View):
    def get(self, *args, **kwargs):
        return HttpResponse('FinalizarProduto')


