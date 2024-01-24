from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views import View
from django.http import HttpResponse
from django.contrib import messages
from . import models
from pprint import pprint


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
        #  TODO: Remover linhas abaixo
        # if self.request.session.get('carrinho'):
        #     del self.request.session["carrinho"]
        #     self.request.session.save()

        url_retorno = self.request.META.get('HTTP_REFERER', reverse('produto:lista'))
        variacao_id = self.request.GET.get('vid')
        sem_estoque = 'Estoque insuficiente!'

        if not variacao_id:
            messages.error(self.request, 'Produto não existe!')
            return redirect(url_retorno)

        variacao = get_object_or_404(models.Variacao, pk=variacao_id)
        variacao_estoque = variacao.estoque

        if variacao_estoque < 1:
            messages.error(self.request, sem_estoque)
            return redirect(url_retorno)

        produto = variacao.produto
        imagem = produto.imagem
        imagem = imagem.name if imagem else ''

        item = {
            'produto_id': produto.id,
            'produto_nome': produto.nome,
            'variacao_nome': variacao.nome or '',
            'preco_unitario': variacao.preco,
            'preco_quantitativo': variacao.preco,
            'preco_unitario_promocional': variacao.preco_promocional,
            'preco_quantitativo_promocional': variacao.preco_promocional,
            'quantidade': 1,
            'slug': produto.slug,
            'imagem': imagem,
        }

        if not self.request.session.get('carrinho'):
            self.request.session['carrinho'] = {}
            self.request.session.save()

        carrinho = self.request.session['carrinho']

        if variacao_id in carrinho:
            quantidade_carrinho = carrinho[variacao_id]["quantidade"]
            quantidade_carrinho += 1

            if variacao_estoque < quantidade_carrinho:
                messages.warning(self.request, sem_estoque + f'Foi adicionado {variacao_estoque}x no carrinho.')

            carrinho[variacao_id]["quantidade"] = quantidade_carrinho
            carrinho[variacao_id]["preco_quantitativo"] = item["preco_unitario"] * quantidade_carrinho

            p_q_promo = 'preco_quantitativo_promocional'  # Para reduziar o tamanho da multiplicação na linha abaixo
            carrinho[variacao_id][p_q_promo] = item[p_q_promo] * quantidade_carrinho

        else:
            carrinho[variacao_id] = item

        self.request.session.save()
        messages.success(self.request, f'{item["produto_nome"]} adicionado ao seu carrinho.')
        return redirect(url_retorno)


class RemoverDoCarrinhoProduto(View):
    def get(self, *args, **kwargs):
        return HttpResponse('RemoverDoCarrinhoProduto')


class CarrinhoProduto(View):
    def get(self, *args, **kwargs):
        return render(self.request, 'produto/carrinho.html')


class FinalizarProduto(View):
    def get(self, *args, **kwargs):
        return HttpResponse('FinalizarProduto')


