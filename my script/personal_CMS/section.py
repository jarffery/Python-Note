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
        self.var_quoteinfo = self.searchObj[6]
        self.quote_temp = self.searchObj[10]

    def product_check(self):
        '''get type of service'''
        if self.quote_temp.lower() in (s.lower() for s in PRICE_DICT.keys()):
            return self.quote_temp.lower()
        else:
            raise RuntimeError(
                f"product type {self.quote_temp} not found. Accepted products: " + ', ' .join(s for s in PRICE_DICT.keys()))

    def people_check(self):  # '''check if the person in the database'''
        self.varTS = self.searchObj[13]
        self.varsales = self.searchObj[8]
        try:
            self.TS_name, self.TS_email, self.TS_OMS = TS_DICT[self.varTS.lower(
            ).strip()]
        except KeyError as e:
            raise KeyError("TS name " + str(e) + "is not found, valid TS names are " + ", ".join(
                s.capitalize() for s in TS_DICT.keys()))
        try:
            self.sales_name, self.sales_email = SALES_DICT[self.varsales]
        except KeyError as e:
            raise KeyError("sales name " + str(e) + " is not found, valid sales names are " + ", ".join(
                s.capitalize() for s in SALES_DICT.keys()))
        return self.TS_name, self.TS_email, self.TS_OMS, self.sales_name, self.sales_email
