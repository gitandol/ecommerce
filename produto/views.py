from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views import View
from django.http import HttpResponse
from . import models


class ListaProdutos(ListView):
    model = models.Produto
    template_name = 'produto/lista.html'
    context_object_name = 'produtos'
    paginate_by = 6
    extra_context = {"home": True}


class DetalheProduto(DetailView):
    model = models.Produto
    template_name = 'produto/detalhes.html'
    context_object_name = 'produto'
    slug_url_kwarg = 'slug'


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


