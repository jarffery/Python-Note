# -*- coding: utf-8 -*-
"""
Created on Wed Dec 19 22:05:40 2018

@author: Jerry
"""

import os
from section import quote
from NVUSdatabase import PRICE_DICT
import time
import os
import shutil

def start_folder(quote_info):
    # quote was downloaded in Download folder
    quote_path = 'C:\\Users\\Jerry\\Downloads\\PrintPDF.pdf'
    q = quote(quote_info)
    f = q.var_quoteinfo
    f_name = str(q.var_quoteinfo + ".pdf")
    Time = time.strftime('%Y-%m', time.localtime())
    path_time = str('C:\\Users\\Jerry\\OneDrive - Novogene/Project/' + q.quote_temp.lower() + '\\' + Time)
    path = str(
        'C:\\Users\\Jerry\\OneDrive - Novogene/Project/' + q.quote_temp.lower() + '\\' + Time + '\\' + str(
            f))
    if q.quote_temp.lower() in (s.lower() for s in PRICE_DICT.keys()):
        try:
            os.mkdir(path_time)
            os.mkdir(path)
            shutil.move(quote_path, path + '\\' + f_name)
            if "premade" in q.quote_temp.lower():
                shutil.copy(
                    'C:\\Users\\Jerry\\Downloads\\NovoLibrarySIF-.xlsx',
                    path + '\\' + 'NovoLibrarySIF-' + q.searchObj[0] + '.xlsx')
                shutil.copy(
                    'C:\\Users\\Jerry\\Downloads\\zjkENybexcel.xlsx', path + '\\' + 'zjkENybexcel.xlsx'
                )
            else:
                shutil.copy(
                    'C:\\Users\\Jerry\\Downloads\\NovoNucleicAcidSIF-.xlsx',
                    path + '\\' + 'NovoNucleicAcidSIF-' + q.searchObj[0] + '.xlsx')
                shutil.copy(
                    'C:\\Users\\Jerry\\Downloads\\hsENybexcel.xlsx', path + '\\' + 'hsENybexcel.xlsx'
                )
        except FileExistsError:
            os.mkdir(path)
            shutil.move(quote_path, path + '\\' + f_name)
            if "premade" in q.quote_temp.lower():
                shutil.copy(
                    'C:\\Users\\Jerry\\Downloads\\NovoLibrarySIF-.xlsx',
                    path + '\\' + 'NovoLibrarySIF-' + q.searchObj[0] + '.xlsx')
                shutil.copy(
                    'C:\\Users\\Jerry\\Downloads\\zjkENybexcel.xlsx', path + '\\' + 'zjkENybexcel.xlsx'
                )
            else:
                shutil.copy(
                    'C:\\Users\\Jerry\\Downloads\\NovoNucleicAcidSIF-.xlsx',
                    path + '\\' + 'NovoNucleicAcidSIF-' + q.searchObj[0] + '.xlsx')
                shutil.copy(
                    'C:\\Users\\Jerry\\Downloads\\hsENybexcel.xlsx', path + '\\' + 'hsENybexcel.xlsx'
                )
