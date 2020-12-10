import time
import json
import datetime

import logging


class Exchange:
    def __init__(self):
        self.login = 0
        self.id = ''
        self.passwd = ''
        self.cert_passwd = ''
        self.account_number = ''
        self.account_pwd = ''
        self.testing = 0
    def set_testing(self, t):
        self.testing = t
    def get_balance(self, ticker):
        pass
    def pending_order(self, uuid):
        pass
    def pending_orders(self, ticker):
        pass
    def buy_market_order(self, ticker, price, qty, contain_req=False):
        pass
    def buy_limit_order(self, ticker, price, qty, contain_req=False):
        pass
    def sell_market_order(self, ticker, price, qty, contain_req=False):
        pass
    def sell_limit_order(self, ticker, price, qty, contain_req=False):
        pass
    def get_orderbook(self, tickers):
        pass
    def get_min_qty(self, qty):
        return qty



class Exchange1:
    def __init__(self):
        self.login = 0
        self.id = ''
        self.passwd = ''
        self.cert_passwd = ''
        self.account_number = ''
        self.account_pwd = ''
        self.event_dispatcher = None
        self.real_dispatcher = None
        self.type = 'unknown'
        self.name = ''
        
    def set_account_info(self, acc, pwd) :
        self.account_number = acc
        self.account_pwd = pwd

    def get_name(self) : 
        return self.name # 거래소 이름



    def get_balance(self, ticker):
        pass
    
    def pending_order(self, uuid) : # uuid 값을 갖는 미체결 주문을 돌려줌
        return [{'error':{'message':'not existing order'}}]
    def pending_orders(self, ticker='all'): # 모든 미체결 주문을 돌려줌
        return [{'error':{'message':'not existing order'}}]

    def buy_limit_order(self, ticker, price, volume):
        pass
    def sell_limit_order(self, ticker, price, volume):
        pass
    def get_orderbook(self, tickers):
        pass
    def get_min_qty(self, qty):
        return qty
    def get_tick_size(self, price, up=0):
        return 0
    def op_time(self) :
        return 1
    def has_time(self) :
        return 0
    def set_type(self, type) :
        self.type = type
    def get_type(self) :
        return self.type
