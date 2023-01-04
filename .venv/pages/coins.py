import random
import json
from env.keys import client
from env.keys import COIN_MAIN


class CoinsPage():
    

    def get_coin_pair(self):
        list_coins = ['BTCUSDT','ALGOUSDT','SPELLUSDT','LUNCUSDT','ZILUSDT','SANDUSDT']
        pair = list_coins[random.randint(0,len(list_coins)-1)]
        return pair

    def get_value_current_coin(self, coin):
        ultimo_preco = client.get_orderbook_ticker(symbol=f'{coin}')
        print(f"Moeda: {coin}\nValor atual da moeda: {ultimo_preco['bidPrice']}")
        return float(ultimo_preco['bidPrice'])

    def get_main_coin_value(self):
        money = 0
        info = client.get_account()
        for lista_ativos in info["balances"]:
            if lista_ativos["asset"] == f'{COIN_MAIN}':
                coin = lista_ativos["asset"] 
                value_coin = float(lista_ativos['free'])
                print(f"Quantidade de {coin} na carteira: U$ {value_coin:.5f}\n\n")
                if value_coin > 300:
                    money = value_coin * 0.20
                if value_coin > 250 and value_coin <= 300:
                    money = value_coin * 0.25
                if value_coin > 200 and value_coin <= 250:
                    money = value_coin * 0.30
                if value_coin > 150 and value_coin <= 200:
                    money = value_coin * 0.35
                if value_coin > 100 and value_coin <= 150:
                    money = value_coin * 0.40
                if value_coin > 15 and value_coin <= 100:
                    money = value_coin
                return money
    
    def get_qtd_asset_wallet(self, coin):
        info = client.get_account()
        for lista_ativos in info["balances"]:
            if lista_ativos["asset"] == coin:
                asset = lista_ativos["asset"] 
                qtd_asset = float(lista_ativos['free'])
                print(f"Quantidade de {asset} na carteira: U$ {qtd_asset:.4f}")
                return qtd_asset
    
    def get_decimal_pressision(self, par):
        print(f"Buscando casas decimais do par: {par}")
        d1 = client.get_symbol_info(symbol=f'{par}')
        s1 = json.dumps(d1)
        json_message = json.loads(s1)
        qtd_decimal = json_message['filters'][1]['minQty']
        att = qtd_decimal.rstrip('0').split('.')
        return len(att[1])
    

