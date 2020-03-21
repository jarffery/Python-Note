# -*- coding: utf-8 -*-
"""
Created on Wed Dec 19 22:05:40 2018

@author: Jerry, Yiwen
"""

import os
import re
import math
import csv
from docx import Document
from docxcompose.composer import Composer
from NVUSdatabase import TS_DICT, SALES_DICT, PRICE_DICT
from section import *
import time
import os
import shutil


def start(quote_info, price1, price2, BInumber, species, library_type, rRNAremoval_check):
    q = quote(quote_info, price1, price2, BInumber, species, library_type, rRNAremoval_check)
    sam_num_1, sam_num_2 = q.get_sam_num()
    compose_name, var_UP_1, var_UP_2, data_output, var_library_type, var_platform = q.service_type()
    q.people_check()

    if BInumber != '':
        sam_num_2 = int(BInumber)
    # find out the species
    if species == '':
        species = q.get_species()
    # get the price and data_output
    if price1 != '':
        var_UP_1 = int(price1)
    if price2 != '':
        var_UP_2 = int(price2)
    Total_1 = var_UP_1 * sam_num_1
    Total_2 = var_UP_2 * sam_num_2
    Total_final = Total_1 + Total_2
    # main script
    q.compose()
    doc = Document(q.composer_name)
    info_dict = {
        'VAR_CLIENT_NAME': str(q.var_client_name),
        'VAR_CLIENT_EMAIL': str(q.searchObj[5]),
        'VAR_CLIENT_SCHOOL': str(q.searchObj[4]),
        'VAR_QUOTE_NUM': q.searchObj[1],
        'VAR_ALY': str(q.bio_type()),
        'VAR_RIN': str(q.RIN_num()),
        'VAR_TAT': q.var_TAT,
        'VAR_UP_1': f'{var_UP_1:,}',
        'VAR_UP_2': f'{var_UP_2:,}',
        'VAR_SPECIES': str(species),
        'VAR_TS': str(q.people_check()[0]),
        'TS_EMAIL': str(q.people_check()[1]),
        'VAR_SALES': str(q.people_check()[3]),
        'SALES_EMAIL': str(q.people_check()[4]),
        'TOTAL_1': f'{Total_1:,}',
        'TOTAL_2': f'{Total_2:,}',
        'TOTAL_FINAL': f'{Total_final:,}',
        'SAM_NUM_1': str(sam_num_1),
        'SAM_NUM_2': str(sam_num_2),
        'DATA_OUTPUT': str(data_output),
        'VAR_LIBRARY_TYPE': str(var_library_type),
        'VAR_PLATFORM': str(var_platform),
        'SERVICE_NAME': str(q.service_name),
        'VAR_STRATEGY': str(q.seq_strategy),
        'VAR_GROUPEMAIL': str(q.var_groupemail),
    }
    # search and replace
    for i in info_dict:
        replace = info_dict.get(i)
        regex1 = re.compile(i)
        docx_replace_regex(doc, regex1, replace)
    pwd = GetDesktopPath()
    outpath = os.path.join(pwd, q.var_quoteinfo + '.docx')
    if os.path.exists(outpath):
        os.unlink(outpath)
    doc.save(outpath)

# for self usage
    if 'jerry' in info_dict.get('VAR_TS').lower():
        f = q.var_quoteinfo
        f_name = str(q.var_quoteinfo + ".docx")
        Time = time.strftime('%Y-%m', time.localtime())
        path_time = str('C:\\Users\\Jerry\\OneDrive - Novogene/Project/' + q.quote_temp.lower() + '\\' + Time)
        path = str('C:\\Users\\Jerry\\OneDrive - Novogene/Project/' + q.quote_temp.lower() + '\\' + Time + '\\' + str(f))
        if q.quote_temp.lower() in (s.lower() for s in PRICE_DICT.keys()):
            try:
                os.mkdir(path_time)
                os.mkdir(path)
                shutil.copy(outpath, path + '\\' + f_name)
                if "premade" in q.quote_temp.lower():
                    shutil.copy('C:\\Users\\Jerry\\Documents\\GitHub\\Quote_generator\\support-section\\OMS-SIF-library.xlsx',
                                path + '\\' + 'Sample_Information_Form-' + q.searchObj[1] + '.xlsx')
                else:
                    shutil.copy('C:\\Users\\Jerry\\Documents\\GitHub\\Quote_generator\\support-section\\OMS-SIF-DNA&RNA.xlsx',
                                path + '\\' + 'Sample_Information_Form-' + q.searchObj[1] + '.xlsx')
            except FileExistsError:
                os.mkdir(path)
                shutil.copy(outpath, path + '\\' + f_name)
                if "premade" in q.quote_temp.lower():
                    shutil.copy('C:\\Users\\Jerry\\Documents\\GitHub\\Quote_generator\\support-section\\OMS-SIF-library.xlsx',
                                path + '\\' + 'Sample_Information_Form-' + q.searchObj[1] + '.xlsx')
                else:
                    shutil.copy('C:\\Users\\Jerry\\Documents\\GitHub\\Quote_generator\\support-section\\OMS-SIF-DNA&RNA.xlsx',
                                path + '\\' + 'Sample_Information_Form-' + q.searchObj[1] + '.xlsx')
    else:
        pass
# for self usage PTO
    #if 'jerry' in info_dict.get('VAR_TS').lower():
    #    path = "./support-section/Jerry_PTO.csv"
    #    value = [q.searchObj[0], q.quote_number, q.firstname, q.lastname, q.var_school, q.var_client_email, q.var_quoteinfo, q.searchObj[7], q.searchObj[8], q.searchObj[9], q.searchObj[10], q.searchObj[11], q.searchObj[12], q.searchObj[13], q.searchObj[14], q.searchObj[15], q.searchObj[16], q.searchObj[17], q.searchObj[18]]
    #    try:
    #        with open(path, 'a', newline = '') as csvfile:
    #            writer = csv.writer(csvfile)
    #            writer.writerow(value)
    #        csvfile.close()
    #        print("record added")
    #    except:
    #        print("record didn't added")