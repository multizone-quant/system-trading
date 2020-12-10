# jwt encoder를 찾지 못하는 오류가 나오면 아래와 같이 pyjwt 설치가 필요함
# pip uninstall jwt
# pip install -U pyjwt

import pyupbit
from pyupbit.exchange_api import *
from jpy_basic_ex import *

UPBIT_TRADING_FEE = 0.035

# 거래소별 공통으로 데이터를 주고 받을 수 있도록 wrapper 추가
# upbit 거래소 lib는 pyupbit 사용함
# https://github.com/sharebook-kr/pyupbit

class MyUpbit(Exchange):
    def __init__(self, access, secret):
        super().__init__()
        self.access = access
        self.secret = secret
        self.name = 'upbit'
        self.exchange = Upbit(access, secret)

    def get_balances(self, ticker="KRW"):
        """
        특정 혹은 전체 코인 잔고 조회
        기존 pyupbit에서는 주문 가능한 잔고만 넘어옴. 
            bal 형태로 돌려주도록 수정함
        :param ticker: 모든 ticker를 원하면 'all' 아니면 특정 ticker
        :return 
        :       [bal1, bal2, ...] :  bal = {'ticker':ticker, 'total':0, 'orderable':0}
        :           ['total']은 전체 잔고, ['orderable']은 주문 가능 수량
        :           오류인 경우에는 ret[0] 번째 bal 안에 'error' 필드가 추가되어 있음. 'error' 유무에 따라 오류 판단
        :
        : 사용법
        :   ret = get_balance('BTC'):
        :   print(ret[0])
        :
        :   ret = get_balance('all'):
        :   print(ret)
        """

        return self.exchange.get_balances(ticker)



    def pending_order(self, uuid):
        """
        현재 미체결 주문 조회
        :param uuid : 주문 번호
        :return 
        :    아래 구조로 돌려줌
        :    [{'time':ord_time, 'ticker':ord_code, 'uuid':ord_no, 'bid_ask':side_type, 'price':ord_price, 'executed_price':done_price, 'volume':org_qty, 'executed_volume':done_qty},
        :    오류인 경우에는 [0]에 오류메세지
        orders = self.exchange.get_order(ticker, state='wait', kind='normal', contain_req=False)
        # {'created_at': '2020-11-24T14:25:47+09:00', 'executed_volume': '0.0', 'locked': '100000.0', 'market': 'KRW-TRX', 'ord_type': 'limit',
        #  'paid_fee': '0.0', 'price': '44.7', 'remaining_fee': '0.0', 'remaining_volume': '100000.0', 'reserved_fee': '0.0', 
        #  'side': 'ask', 'state': 'wait', 'trades_count': 0, 'uuid': 'c3b8e35e-d13e-42d5-...de1f482a6', ...}
        """

        orders = self.pending_orders()
        if orders == None :
            # 오류
            return [{'error':{'message':'err pending_orders'}}]
        elif 'error' in orders[0] :
            # 오류
            return orders
        else :
            for ord in orders[0] :  # orders[0] 번째 order list가 들어있음. 내가 만든 코드이므로 그냥 해당 ord를 돌려주면 된다.
                if ord['uuid'] != uuid :
                    continue
                if self.testing :
                    return [{'error':{'message':'not existing order'}}]
                return [ord]
        return [{'error':{'message':'not existing order'}}]

    def pending_orders(self, ticker='all'):
        """
        현재 미체결 주문 조회
        :param ticker: 모든 ticker를 워하면 'all' 아니면 특정 ticker
        :return 
        :    아래 구조로 돌려줌
        :    [
        :      [{'time':ord_time, 'ticker':ord_code, 'uuid':ord_no, 'bid_ask':side_type, 'price':ord_price, 'executed_price':done_price, 'volume':org_qty, 'executed_volume':done_qty},
        :       {'time':ord_time, 'ticker':ord_code, 'uuid':ord_no, 'bid_ask':side_type, 'price':ord_price, 'executed_price':done_price, 'volume':org_qty, 'executed_volume':done_qty},
        :       {'time':ord_time, 'ticker':ord_code, 'uuid':ord_no, 'bid_ask':side_type, 'price':ord_price, 'executed_price':done_price, 'volume':org_qty, 'executed_volume':done_qty}]

        :      [{'ord_total':ord_total, 'ord_fee':ord_fee, 'ord_tax':ord_tax})]
        :    ]
        :    오류인 경우에는 [0]에 오류메세지
        """
        orders = self.exchange.get_order(ticker, state='wait', kind='normal', contain_req=False)
        # {'created_at': '2020-11-24T14:25:47+09:00', 'executed_volume': '0.0', 'locked': '100000.0', 'market': 'KRW-TRX', 'ord_type': 'limit',
        #  'paid_fee': '0.0', 'price': '44.7', 'remaining_fee': '0.0', 'remaining_volume': '100000.0', 'reserved_fee': '0.0', 
        #  'side': 'ask', 'state': 'wait', 'trades_count': 0, 'uuid': 'c3b8e35e-d13e-42d5-...de1f482a6', ...}
        result1 = []
        result2 = []


        if orders == None :
            # 오류
            return [{'error':{'message':'err pending_orders'}}]
        elif 'error' in orders[0] :
            # 오류
            return orders

        else :
            for ord in orders :
                if ticker != 'all' :
                    if ord['market'] != ticker :
                        continue
                side_type = 'sell'
                if ord['side'] == 'bid' : # 매수
                    side_type = 'buy'
                org_qty = float(ord['remaining_volume']) + float(ord['executed_volume'])

                order = {'time':ord['created_at'], 'ticker':ord['market'], 'uuid':ord['uuid'], 'ask_bid':side_type, 'price':float(ord['price']), 'executed_price':0, 'qty':org_qty, 'executed_qty':float(ord['executed_volume'])}
                result1.append(order)

#                result3.append([{'cont':last_order_num, 'total':nCount}])
                
            # 내가 정의한 형태로 변환하여 돌려줌
            result2.append({'ord_total':len(result1), 'ord_fee':UPBIT_TRADING_FEE, 'ord_tax':0.0})

            res = []
            res.append(result1)
            res.append(result2)

            return res

    def buy_market_order(self, ticker, price, qty, contain_req=False):
        return self.buy_order('market', ticker, price, qty, contain_req)

    def buy_limit_order(self, ticker, price, qty, contain_req=False):
        return self.buy_order('limit', ticker, price, qty, contain_req)

    def buy_order(self, ty, ticker, price, qty, contain_req=False):
        if ty == 'market' :
            ret = self.exchange.buy_market_order(ticker, price, contain_req)
        else :
            ret = self.exchange.buy_limit_order(ticker, price, qty, contain_req)

        if ret == None : # error
            return [{'error':{'message':'buying order failed: unknown err'}}]   
        elif 'error' in ret :
            # 오류
            return [{'error':{'message':'buying order failed: '+ret['error']['message']}}] 

        # 주문 성공
        # {'remaining_fee': '1.5', 'executed_volume': '0.0', 'created_at': '2020-11-25T01:14:36+09:00', 'paid_fee': '0.0', 
        #  'remaining_volume': '20.0', 'uuid': '9a59ce5b-090d-40c9-919e-bc32b302c131', 'market': 'KRW-STEEM', 'reserved_fee': '1.5', 
        #  'ord_type': 'limit', 'side': 'bid', 'volume': '20.0', 'state': 'wait', 'price': '150.0', 'trades_count': 0, 'locked': '3001.5'}

        result = []
        info = {'uuid':ret['uuid'], 'date':ret['created_at'], 'bid_ask': 'buy', 'status': 1, 'org_qty' : qty, 'done_qty' : 0.0, 'price':price}
        result.append(info)                                    

        return result

    def sell_market_order(self, ticker, price, qty, contain_req=False):
        return self.sell_order('market', ticker, price, qty, contain_req)

    def sell_limit_order(self, ticker, price, qty, contain_req=False):
        return self.sell_order('limit', ticker, price, qty, contain_req)

    def sell_order(self, ty, ticker, price, qty, contain_req=False):
        if ty == 'market' :
            ret = self.exchange.sell_market_order(ticker, qty, contain_req)
        else :
            ret = self.exchange.sell_limit_order(ticker, price, qty, contain_req)
        if ret == None : # error
            return [{'error':{'message':'selling order failed: unknown err'}}]   
        elif 'error' in ret :
            # 오류
            return [{'error':{'message':'sellinging order failed: '+ret['error']['message']}}] 

        # 주문 성공
        # {'remaining_fee': '1.5', 'executed_volume': '0.0', 'created_at': '2020-11-25T01:14:36+09:00', 'paid_fee': '0.0', 
        #  'remaining_volume': '20.0', 'uuid': '9a59ce5b-090d-40c9-919e-bc32b302c131', 'market': 'KRW-STEEM', 'reserved_fee': '1.5', 
        #  'ord_type': 'limit', 'side': 'ask', 'volume': '20.0', 'state': 'wait', 'price': '150.0', 'trades_count': 0, 'locked': '3001.5'}

        result = []
        info = {'uuid':ret['uuid'], 'date':ret['created_at'], 'bid_ask': 'sell', 'status': 1, 'org_qty' : qty, 'done_qty' : 0.0, 'price':price}
        result.append(info)                                    

        return result

    def cancel_order(self, uuid, contain_req=False):
        ret = self.exchange.cancel_order(uuid, contain_req)
        if ret == None : # error
            return [{'error':{'message':'canceling order failed: unknown err'}}]   
        elif 'error' in ret :
            # 오류
            return [{'error':{'message':'canceling order failed: '+ret['error']['message']}}] 

        result = []
        qty = ret['volume']
        done = float(ret['volume']) - float(ret['remaining_volume'])
        info = {'uuid':ret['uuid'], 'date':ret['created_at'], 'bid_ask': ret['side'], 'status': 1, 'org_qty' : qty, 'done_qty' : str(done), 'price':'0'}
        result.append(info)                                    

        return result

    def get_ohlcv(self, ticker="KRW-BTC", interval="day", count=200):
        return pyupbit.get_ohlcv(ticker, interval, count)

    # https://api.upbit.com/v1/ticker/?markets=KRW-STEEM,KRW-JST
    def get_cur_price_all(self, tickers):
        int_tickers = ''
        for tick in tickers :
            if int_tickers != '' :
                int_tickers += ','
            int_tickers += tick
        return pyupbit.get_current_ticker_info(int_tickers)

if __name__ == "__main__":
    print("jpy_upbit")
