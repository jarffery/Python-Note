import requests
import http.cookiejar as cookielib
import json
import re
from section import quote
from NVUSdatabase import TS_DICT, SALES_DICT, PRICE_DICT
from process import process_data, process_dict_library, process_dict

#import the product dict
from AA_dict import *

class lead_submit(quote):
    def __init__(self, info, price1, price2, BInumber, species, library_type, rRNAremoval_check, password):
        super().__init__(info, price1, price2, BInumber, species, library_type, rRNAremoval_check)
        self.kfid = ""
        self.client_post = ""
        self.password = password
        #header and CMS_session save
        self.url = "http://cms.novogene.com/"
        self.CMS_Session = requests.session()
        self.CMS_Session.cookies = cookielib.LWPCookieJar(filename = "CMSCookies.txt")
        self.UserAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36"
        self.header = {
            #"Origin": "http://cms.novogene.com",
            "Referer": "http://cms.novogene.com/index.jsp",
            "User-Agent": self.UserAgent,
        }
    def login(self):
        print("login.....")
        postUrl = "http://cms.novogene.com/core/login/login!login.action"
        password = "1"
        if self.password:
            password = self.password
        else:
            pass
        try:
            postData = {
                "loginInfo.usercode": TS_DICT[self.searchObj[13].lower()][2] ,
                "loginInfo.userpass": password,
                "loginInfo.islocal": "1",
            }
            self.responseRes = self.CMS_Session.post(postUrl, data = postData, headers = self.header)
            print(f"statusCode = {self.responseRes.status_code}")
            print(f"text = {self.responseRes.text}")
            #CMS_Session.cookies.save(ignore_discard=True, ignore_expires=True)
        except KeyError as e:
            print(f"no such a person existed in database {self.searchObj[13].lower()}")
    def json_post(self, data):
        try:
            obj = {
                "jsonString": json.dumps(data)
            }
        except TypeError as e:
            print(e)
            print("Please check data type!")
        return obj
    def client_search(self):
        client_seach_url = "http://cms.novogene.com/mylims/enterpriseinfo/enterpriseinfo!selectCustomerForMyCustomer.action"
        institute_url = "http://cms.novogene.com/mylims/enterpriseinfo/enterpriseinfo!selectCustomerForMyCustomer.action"
        client_info = {"cond":{"corpdesc":"","corpemail":""}}
        client_info['cond']['corpemail'] = self.var_client_email
        post = self.json_post(client_info)
        search = self.CMS_Session.post(client_seach_url, headers = self.header, data = post)
        statusCode = search.status_code
        print(f"statusCode = {statusCode}")
        try:
            client_dict = json.loads(re.sub(',}','}',search.text))['enterpriseInfos'][0]
        except IndexError as e:
            try:
                client_info['cond']['corpdesc'] = self.var_client_name
                client_info['cond']['corpemail'] = ""
                post = self.json_post(client_info)
                search = self.CMS_Session.post(client_seach_url, headers=self.header, data=post)
                client_dict = json.loads(re.sub(',}', '}', search.text))['enterpriseInfos'][0]
            except IndexError as e:
                raise IndexError(f"{self.var_client_name} is not in CMS")
        self.client_post = {"corpno":client_dict['corpno'],"corpname":client_dict['corpdesc'],"linkmantel":"","linkmanmail":client_dict['corpemail'],"corpdesc":client_dict["firstcorpdesc"],"corpcode":client_dict["firstcorpcode"],"corpshippingaddress":client_dict["corpshippingaddress"]}
        return self.client_post

    def submit_quote(self):
        #submit lead
        save_url = "http://cms.novogene.com/nhzy/projectquotation/quotation!insertQuotationInfo.action?cond.pageI18n="
        #US quote json_dict
        submit_dict = {"quotationInfo": {
            "qtype": "1",
            "salesname": self.var_quoteinfo,
            "currencynow": "USD",
            "bcompany": "202",
            "zonearea": "US",
            "totalprice": "0",
            "afteroffersum": "",
            "taxcode": "CN VAT 0",
            "tax": "CN_VAT",
            "taxname": "中国增值税",
            "taxcontent": "海外税率",
            "validity": "30",
            "corpno": "",
            "corpname": "",
            "linkmantel": "",
            "linkmanmail": "",
            "corpdesc": "",
            "corpcode": "",
            "corpshippingaddress": ""
        }}
        for key, value in self.client_post.items():
            submit_dict["quotationInfo"].update({key:value})
        search = self.CMS_Session.post(save_url, headers = self.header, data = self.json_post(submit_dict))
        self.kfid = json.loads(search.text)['quotationInfo'][0]['kfquotationid']
    #submit the processtype
    def process_submit(self):
        new_process_url = 'http://cms.novogene.com/nhzy/projectquotation/quotationproduct!saveQuotationproductInfosNew.action'
        #kfid_url = "http://cms.novogene.com/nhzy/projectquotation/quotation!selectQuotationInfoById.action"
        #kfid = {"jsonString": '{quotationInfo:{kfquotationid:' + self.kfid + '}}'}
        #kfid_search = self.CMS_Session.post(kfid_url, headers = self.header, data = kfid)
        try:
            if "premade" in self.quote_temp.lower():
                self.process_data = process_dict_library
                pcode = self.process_dict[self.quote_temp.lower()][0]
                pname = AA_dict[pcode][pcode][pcode]
                self.process_data['quotationproductInfos'][0].update(
                    {'pcode': pcode, 'pname': pname})
                self.process_data['quotationproductInfos'][0].update(
                    {"kfquotationid": self.kfid})
                for i in range(len(self.process_dict[self.quote_temp.lower()][1])):
                    processname = self.process_dict[self.quote_temp.lower(
                    )][1][i]
                    processcode = AA_dict[pcode][processname][processname]
                    processtype = self.process_dict[self.quote_temp.lower(
                    )][2][i]
                    processtypename = AA_dict[pcode][processname][processtype]
                    self.process_data['quoprocessInfos'][i].update(
                        {"processname": processname, "processcode": processcode, "processtype": processtype, "processtypename": processtypename})
                    self.process_data['quoprocessInfos'][i].update(
                        {'pcode': pcode, 'pname': pname})
                    self.process_data['quoprocessInfos'][i].update(
                        {"kfquotationid": self.kfid})
                    self.process_data['quoprocessInfos'][i].update(
                        {"samnum": self.sam_num_2})
                #change the sample QC number
                self.process_data['quoprocessInfos'][0].update(
                    {"samnum": self.sam_num_1})
            else:
                self.process_data = process_data
                pcode = self.process_dict[self.quote_temp.lower()][0]
                pname = AA_dict[pcode][pcode][pcode]
                self.process_data['quotationproductInfos'][0].update(
                    {'pcode': pcode, 'pname': pname})
                self.process_data['quotationproductInfos'][0].update(
                    {"kfquotationid": self.kfid})
                self.process_data['quotationproductInfos'][0].update(
                    {"samplenum": self.sam_num_1, "datasize": self.data_output})
                for i in range(len(self.process_dict[self.quote_temp.lower()][1])):
                    processname = self.process_dict[self.quote_temp.lower()][1][i]
                    processcode = AA_dict[pcode][processname][processname]
                    processtype = self.process_dict[self.quote_temp.lower()][2][i]
                    processtypename = AA_dict[pcode][processname][processtype]
                    self.process_data['quoprocessInfos'][i].update(
                        {"processname": processname, "processcode": processcode, "processtype": processtype, "processtypename": processtypename})
                    self.process_data['quoprocessInfos'][i].update(
                        {'pcode': pcode, 'pname': pname})
                    self.process_data['quoprocessInfos'][i].update(
                        {"kfquotationid": self.kfid})
                    self.process_data['quoprocessInfos'][i].update(
                        {"samnum": self.sam_num_1})
                    if "GY0002" in processname:
                        self.process_data['quoprocessInfos'][i].update(
                            {"datasize": self.data_output})
                    else:
                        pass
        except KeyError as identifier:
            print(f"the process {identifier} is not acceptable so far")
            raise
        #submit the process details
        process_submit = self.CMS_Session.post(new_process_url, headers = self.header, data = self.json_post(self.process_data))
        print(f"statusCode = {process_submit.status_code}")


def run_it(quote_info, price1, price2, BInumber, species, library_type, rRNAremoval_check, password):
    lead = lead_submit(quote_info, price1, price2, BInumber, species, library_type, rRNAremoval_check, password)
    lead.login()
    lead.client_search()
    lead.submit_quote()
    lead.service_type()
    lead.process_submit()
    

