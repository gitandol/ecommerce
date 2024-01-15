from django.urls import path
from . import views

app_name = 'produto'

urlpatterns = [
    path('', views.ListaProdutos.as_view(), name='lista'),
    path('<slug>', views.DetalheProduto.as_view(), name='detalhe'),
    path('adicionaraocarrinho/', views.AdicionarAoCarrinhoProduto.as_view(), name='adicionaraocarrinho'),
    path('removerdocarrinho/', views.RemoverDoCarrinhoProduto.as_view(), name='removerdocarrinho'),
    path('carrinho/', views.CarrinhoProduto.as_view(), name='carrinho'),
    path('finalizar/', views.FinalizarProduto.as_view(), name='finalizar'),
]
