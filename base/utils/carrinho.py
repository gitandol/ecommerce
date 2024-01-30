
def quantidade_itens(carrinho):
    return sum([item["quantidade"] for item in carrinho.values()])


def valor_itens(carrinho):
    return sum(
        [
            item.get('preco_quantitativo_promocional')
            if item.get('preco_quantitativo_promocional')
            else item.get('preco_quantitativo')
            for item in carrinho.values()
        ]
    )

