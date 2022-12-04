from env.keys import client
from binance.enums import * 
from pages.coins import CoinsPage
from pages.sell import SellPage
from pages.buy import BuyPage
import json
import time



TIME_INTERVAL = client.KLINE_INTERVAL_12HOUR
class ControlPage():

    coin = CoinsPage()
    sell = SellPage()
    buy = BuyPage()
    list_coins = ['BTCUSDT']
    

    def validador_trade(self, moeda):
        #try:
            time.sleep(5)
            #moeda = self.coin.get_coin_pair()
            print(f'Moeda: {moeda}')
            if moeda not in self.list_coins:
                print('Moeda sem histórico de compra/venda')
                self.list_coins.append(moeda)
                print(f'Lista atualizada: {self.list_coins}')
                self.buy.buy_new_coin(moeda)
                
            ultimo_trade = client.get_my_trades(symbol=f"{moeda}", limit=1)
            for ultimas_compras in ultimo_trade:
                if ultimas_compras['isBuyer'] == False and moeda in self.list_coins:
                    valor_de_venda = float(ultimas_compras['price'])
                    self.buy.buy_coin(moeda, valor_de_venda)

                if ultimas_compras['isBuyer'] == True and moeda in self.list_coins:
                    vl_gasto = float(ultimas_compras['quoteQty'])
                    valor_de_compra = float(ultimas_compras['price'])
                    quantidade = float(ultimas_compras['qty'])
                    self.sell.sell_coin(moeda, vl_gasto, valor_de_compra, quantidade)



        #except TypeError as e:
        #    print(e)
        #finally:
        #    self.validador_trade()

    def get_history(self):
            time.sleep(5)  
            MOEDA = self.coin.get_coin_pair()
            vl_coin = self.coin.get_value_current_coin(MOEDA)
            list_fechamento = []
            cont = 0
            d1 = client.get_historical_klines(MOEDA, TIME_INTERVAL, '10 day ago UTC')
            s1 = json.dumps(d1)
            json_message = json.loads(s1)
            qtd = len(json_message)-1
            while cont <= qtd:
                    fechamento = float(json_message[cont][4].rstrip('0'))
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
                    
            elif media < vl_coin:
                        variacao = float((vl_coin - media)/media*100)
                        print(f'Tendência de baixa: -{variacao:.2f}%')
                        

           
        except TypeError as e:
            print(e)
        finally:
            self.get_monitoracao()




      
        




    
