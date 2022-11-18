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
    

    def validador_trade(self, moeda): 
            ultimo_trade = client.get_my_trades(symbol=f"{moeda}", limit=1)
            qtd = len(ultimo_trade)

            for ultimas_compras in ultimo_trade:
                if ultimas_compras['isBuyer'] == False:
                    valor_de_venda = float(ultimas_compras['price'])
                    self.buy.buy_coin(moeda, valor_de_venda)

                if ultimas_compras['isBuyer'] == True:
                    vl_gasto = float(ultimas_compras['quoteQty'])
                    valor_de_compra = float(ultimas_compras['price'])
                    quantidade = float(ultimas_compras['qty'])
                    self.sell.sell_coin(moeda, vl_gasto, valor_de_compra, quantidade)

                if qtd == 0:
                    print('Moeda sem histórico de compra/venda')
                    self.buy.buy_new_coin(moeda)


    def get_monitoracao(self):
        try:
            time.sleep(2)  
            MOEDA = self.coin.get_coin_pair()
            print(MOEDA)
            vl_coin = self.coin.get_value_current_coin(MOEDA)
            list_fechamento = []
            cont = 0
            d1 = client.get_historical_klines(MOEDA, TIME_INTERVAL, '5 day ago UTC')
            s1 = json.dumps(d1)
            json_message = json.loads(s1)
            qtd = len(json_message)-1
            while cont <= qtd:
                    fechamento = float(json_message[cont][4].rstrip('0'))
                    list_fechamento.append(fechamento)
                    media = sum(list_fechamento)/qtd
                    cont+=1

            if media > vl_coin and media > 2:
                        variacao = float((media - vl_coin)/vl_coin*100)
                        print(f'Tendência de alta: {variacao:.2f}%')
                        self.validador_trade(MOEDA)
                    
            if media < vl_coin:
                        variacao = float((vl_coin - media)/media*100)
                        print(f'Tendência de baixa: -{variacao:.2f}%')
                        self.get_monitoracao()

           
        except:
            print('erro')
        finally:
            self.get_monitoracao()



      
        




    
