from binance.client import Client
from env.keys import api_secret, api_key
from binance.enums import * 
from pages.coins import CoinsPage
from pages.sell import SellPage
from pages.buy import BuyPage

import requests
import time

client = Client(api_key, api_secret)

class ControlPage():

    coin = CoinsPage()
    sell = SellPage()
    buy = BuyPage()

    def validador_trade(self):
        time.sleep(20)
        try:
            moeda = self.coin.get_coin_pair()
            qtd_c = len(moeda)
            if qtd_c == 7:
                asset = self.coin.get_qtd_asset_wallet(moeda[:-4])
            if qtd_c == 6:
                asset = self.coin.get_qtd_asset_wallet(moeda[:-3])

            ultimo_trade = client.get_my_trades(symbol=f"{moeda}", limit=1)
            for ultimas_compras in ultimo_trade:
                if ultimas_compras['isBuyer'] == False:
                    valor_de_venda = float(ultimas_compras['price'])
                    #quantidade = float(ultimas_compras['qty'])
                    self.buy.buy_coin(moeda, valor_de_venda, asset)
                if ultimas_compras['isBuyer'] == True:
                    vl_gasto = float(ultimas_compras['quoteQty'])
                    valor_de_compra = float(ultimas_compras['price'])
                    quantidade = float(ultimas_compras['qty'])
                    self.sell.sell_coin(moeda, vl_gasto, valor_de_compra, quantidade)
                if ultimo_trade == None:
                    print('Moeda sem histórico de compra/venda')
                    self.buy.buy_new_coin(moeda)
        except:
            print('erro')
        finally:
            self.validador_trade() 

    
