import time
import json
import datetime
import logging

from jpy_basic_ex import Exchange

seq_uuid = 1256789

class DummyExchange(Exchange):
    def __init__(self):
        super().__init__()
        self.type = ''
        self.name = 'dummy'
        self.holding = []

    def get_current_price(self, ticker):
        return 0

    def get_balance(self, ticker):
        bal = 0 
        for each in self.holding :
            if ticker == each['ticker'] and each['sold'] != 0 :
                bal += each['qty']

        return 1, {'total':bal}

    def get_balances(self):
        return {}

    def buy_limit_order(self, ticker, price, volume, order_type):
        global seq_uuid
        result = []
        result.append({'uuid':seq_uuid})
        seq_uuid += 1

        self.holding.append({'ticker':ticker, 'price':price, 'qty':volume, 'sold':0})
        
        return result

    def sell_limit_order(self, ticker, price, volume, order_type):
        global seq_uuid
        result = []
        result.append({'uuid':seq_uuid})
        seq_uuid += 1

        for each in self.holding :
            if ticker == each['ticker'] :
                if each['qty'] == volume and each['sold'] != 0 :
                    each['sold'] = volume

        return result

    def cancel_order(self, uuid, code='', qty=0):
        result = []
        result.append({'uuid':uuid})

        for each in self.holding :
            if ticker == each['ticker'] :
                if each['qty'] == volume and each['sold'] != 0 :
                    each['sold'] = volume

        return result

    def enlist_real_stock_code(self, code, ty):
        return 1
        
    def delist_real_stock_code(self, code):
        return 1
