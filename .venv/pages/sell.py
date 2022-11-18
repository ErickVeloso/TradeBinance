from env.keys import api_key_telegram, chat_id
from binance.enums import *
from pages.coins import CoinsPage
import requests

class SellPage():

    coin = CoinsPage()

    def sell_coin(self, moeda, vl_gasto, valor_de_compra, quantidade):
            print(f"Verificando uma possível venda de: {moeda}")
            sale_value = float(valor_de_compra + (valor_de_compra*0.001))
            print(f'Valor estimado de venda - {sale_value:.5f}\n\n')
            value_current = int(self.coin.get_value_current_coin(moeda))
            lucro = float((quantidade*value_current) - vl_gasto)
            orders = client.get_open_orders(symbol=f'{moeda}')
            qtd_ordem = len(orders)
            if qtd_ordem < 1 and sale_value < value_current:
                client.create_order(
                symbol=f'{moeda}',
                side=SIDE_SELL,
                type=ORDER_TYPE_MARKET,
                #timeInForce=TIME_IN_FORCE_GTC,
                #price=value_current,
                quantity=quantidade,        
                )
                venda = True
                if venda == True:
                    print(f"\n💸 Valor BRL gasto: {vl_gasto:.5f}\nValor de compra: {valor_de_compra:.5f}\nQuantidade comprada: {quantidade:.5f}")
                    mensagem = f"🔴 ORDEM DE VENDA 🔴\nVenda de {moeda} efetuada\nValor de venda: {value_current:.5f}\nQuantidade vendida: {quantidade:.5f}\nLucro: {lucro:.5f} 💰"
                    url = f'https://api.telegram.org/bot{api_key_telegram}/sendMessage?chat_id={chat_id}&text={mensagem}'
                    requests.get(url)