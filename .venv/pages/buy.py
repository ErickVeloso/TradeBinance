from env.keys import api_key_telegram, chat_id
from pages.control import client
from binance.enums import *
from pages.coins import CoinsPage
import requests

class BuyPage():

    coin = CoinsPage()

    def buy_coin(self, moeda, valor_de_venda):
        dec = self.coin.get_decimal_pressision(moeda)
        print(f"Verificando uma possível compra de: {moeda}")
        comparative_value = float(valor_de_venda - (valor_de_venda*0.0025))
        print(f"Valor estimado para compra: {comparative_value:.5f}")
        brl_carteira = self.coin.get_main_coin_value()
        value_current_coin = self.coin.get_value_current_coin(moeda)
        quantidade = float(brl_carteira/value_current_coin)
        qtd = float(round(quantidade, dec))
        valor_gasto = float(quantidade * value_current_coin)
        orders = client.get_open_orders(symbol=f'{moeda}')
        qtd_ordem = len(orders)
        if qtd_ordem < 1 and value_current_coin < comparative_value:
                client.create_order(
                symbol=f'{moeda}',
                side=SIDE_BUY,
                type=ORDER_TYPE_MARKET,
                quantity=qtd,
                #price=value_current_coin,
                #timeInForce=TIME_IN_FORCE_GTC,
                )
                compra = True
                if compra == True:
                        mensagem = f"🟢 ORDEM DE COMPRA 🟢\nCompra de {moeda} efetuada.\nValor de Compra: R$ {value_current_coin:.5f}\nReais na carteira: R$ {brl_carteira:.5f}\n💸 Valor gasto R$ {valor_gasto:.5f}"
                        url = f'https://api.telegram.org/bot{api_key_telegram}/sendMessage?chat_id={chat_id}&text={mensagem}'
                        requests.get(url)
    
    def buy_new_coin(self, moeda):
        dec = self.coin.get_decimal_pressision(moeda)
        brl_carteira = self.coin.get_main_coin_value()
        valor_atual_moeda = self.coin.get_value_current_coin(moeda)
        quantidade = float(brl_carteira/valor_atual_moeda)
        valor_gasto = quantidade*valor_atual_moeda
        qtd = float(round(quantidade, dec))
        orders = client.get_open_orders(symbol=f'{moeda}')
        qtd_ordem = len(orders)
        if qtd_ordem < 1:
                client.create_order(
                symbol=f'{moeda}',
                side=SIDE_BUY,
                type=ORDER_TYPE_MARKET,
                quantity=qtd,
                #price=valor_atual_moeda,
                #timeInForce=TIME_IN_FORCE_GTC,
                )
                compra = True
                if compra == True:
                        mensagem = f"🟢 ORDEM DE COMPRA 🟢\nCompra de {moeda} efetuada.\nValor de Compra: R$ {valor_atual_moeda:.5f}\nReais na carteira: R$ {brl_carteira:.5f}\n💸 Valor gasto R$ {valor_gasto:.5f}"
                        url = f'https://api.telegram.org/bot{api_key_telegram}/sendMessage?chat_id={chat_id}&text={mensagem}'
                        requests.get(url)