from env.keys import client
from binance.enums import * 
from pages.coins import CoinsPage
from pages.sell import SellPage
from pages.buy import BuyPage
import json
import time



TIME_INTERVAL = client.KLINE_INTERVAL_15MINUTE
class ControlPage():

    coin = CoinsPage()
    sell = SellPage()
    buy = BuyPage()
    list_coins = ['BTCUSDT']
    

    def validador_trade(self, moeda):
        #try:
            time.sleep(5)
            variacao_med = self.get_variacao(moeda)               
            ultimo_trade = client.get_my_trades(symbol=f"{moeda}", limit=1)
            qtd = len(ultimo_trade)
            for ultimas_compras in ultimo_trade:
                if ultimas_compras['isBuyer'] == False and moeda in self.list_coins and variacao_med > 0.5:
                    valor_de_venda = float(ultimas_compras['price'])
                    self.buy.buy_coin(moeda, valor_de_venda)

                if ultimas_compras['isBuyer'] == True and moeda in self.list_coins:
                    vl_gasto = float(ultimas_compras['quoteQty'])
                    valor_de_compra = float(ultimas_compras['price'])
                    quantidade = float(ultimas_compras['qty'])
                    self.sell.sell_coin(moeda, vl_gasto, valor_de_compra, quantidade)

                if moeda not in self.list_coins and variacao_med > 0.5:
                    print('Moeda sem histórico de compra/venda')
                    self.list_coins.append(moeda)
                    print(f'Lista atualizada: {self.list_coins}')
                    self.buy.buy_new_coin(moeda)
    
    def get_variacao(self, moeda):
        list_maior_valor = []
        list_menor_valor = []
        cont = 0
        MOEDA = moeda
        TIME_INTERVAL_MED = client.KLINE_INTERVAL_1DAY
        d1 = client.get_historical_klines(MOEDA, TIME_INTERVAL_MED, '10 day ago UTC')
        s1 = json.dumps(d1)
        json_message = json.loads(s1)
        qtd = len(json_message)-1
        dias = qtd+1
        while cont <= qtd:
            high_price = float(json_message[cont][2])
            low_price = float(json_message[cont][3])
            list_maior_valor.append(high_price)
            list_menor_valor.append(low_price)
            maior = sum(list_maior_valor)/qtd
            menor = sum(list_menor_valor)/qtd
            variacao = float(((maior / menor)-1)*100)
            cont+=1
        print(f'Variação media de {dias} dias: {variacao:.2f}%')
        return variacao


    def get_history(self):
            cont = 0
            list_fechamento = []
            time.sleep(4)  
            MOEDA = self.coin.get_coin_pair()
            vl_coin = self.coin.get_value_current_coin(MOEDA)
            d1 = client.get_historical_klines(MOEDA, TIME_INTERVAL, '10 day ago UTC')
            time.sleep(4) 
            s1 = json.dumps(d1)
            json_message = json.loads(s1)
            qtd = len(json_message)-1
            while cont <= qtd:
                    fechamento = float(json_message[cont][4])
                    list_fechamento.append(fechamento)
                    media = sum(list_fechamento)/qtd
                    cont+=1
            return media, vl_coin, MOEDA

    def get_monitoracao(self):
        try:
            dados = self.get_history()
            media = dados[0]
            vl_coin = dados[1]
            moeda = dados[2]
            if media > vl_coin and media > 2:
                variacao = float((media - vl_coin)/vl_coin*100)
                print(f'Tendência de alta: {variacao:.2f}%')
                self.validador_trade(moeda)     
            if media < vl_coin:
                variacao = float((vl_coin - media)/media*100)
                print(f'Tendência de baixa: -{variacao:.2f}%')
                self.validador_trade(moeda)
        except TypeError as e:
            print(e)
        finally:
            self.get_monitoracao()



      
        




    
