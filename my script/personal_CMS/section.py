# -*- coding: utf-8 -*-
"""
Created on 7/22/2019

@author: Jerry
"""
from NVUSdatabase import TS_DICT, SALES_DICT, PRICE_DICT

class quote(object):
    def __init__(self, info):
        self.searchObj = [a.strip() for a in info.split("\t")]
        #quote information
        self.var_quoteinfo = self.searchObj[1]
        self.quote_temp = self.searchObj[2]

    def product_check(self):
        '''get type of service'''
        if self.quote_temp.lower() in (s.lower() for s in PRICE_DICT.keys()):
            return self.quote_temp.lower()
        else:
            raise RuntimeError(
                f"product type {self.quote_temp} not found. Accepted products: " + ', ' .join(s for s in PRICE_DICT.keys()))

