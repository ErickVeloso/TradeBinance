import random
import json
from env.keys import client
from env.keys import COIN_MAIN


class CoinsPage():

    def get_coin_pair(self):
        list_coins = ['BTCUSDT','LTCUSDT']
        pair = list_coins[random.randint(0,len(list_coins)-1)]
        return pair

    def get_value_current_coin(self, coin):
        ultimo_preco = client.get_orderbook_ticker(symbol=f'{coin}')
        #print(f"Valor atual da moeda: {ultimo_preco['bidPrice']}")
        return float(ultimo_preco['bidPrice'])

    def get_main_coin_value(self):
        info = client.get_account()
        for lista_ativos in info["balances"]:
            if lista_ativos["asset"] == f'{COIN_MAIN}':
                coin = lista_ativos["asset"] 
                value_coin = float(lista_ativos['free'])
                print(f"Quantidade de {coin} na carteira: U$ {value_coin:.5f}\n\n")
                return value_coin * 0.99
    
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
        qtd_decimal = json_message['filters'][2]['minQty']
        att = qtd_decimal.rstrip('0').split('.')
        return len(att[1])
    

