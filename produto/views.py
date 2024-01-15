from django.shortcuts import render
from django.views.generic.list import ListView
from django.views import View
from django.http import HttpResponse


class ListaProdutos(View):
    def get(self, *args, **kwargs):
        return HttpResponse('ListaProdutos')


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


