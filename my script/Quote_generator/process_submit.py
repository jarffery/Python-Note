from AA_dict import AA_dict
from process import process_data
from section import quote
from NVUSdatabase import TS_DICT
import json
import re
import requests
import http.cookiejar as cookielib


class database(object):
    def __init__(self):
        '''header and CMS_session save'''
        self.url = "http://cms.novogene.com/"
        self.CMS_Session = requests.session()
        self.CMS_Session.cookies = cookielib.LWPCookieJar(filename="CMSCookies.txt")
        self.UserAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36"
        self.header = {
            # "Origin": "http://cms.novogene.com",
            "Referer": "http://cms.novogene.com/index.jsp",
            "User-Agent": self.UserAgent,
        }

    def login(self):
        '''CMS_Session.cookies.save(ignore_discard=True, ignore_expires=True)'''
        print("login.....")
        postUrl = "http://cms.novogene.com/core/login/login!login.action"
        try:
            postData = {
                "loginInfo.usercode": "jerry.jie",
                "loginInfo.userpass": "0128Xx@gina",
                "loginInfo.islocal": "1",
            }
            self.responseRes = self.CMS_Session.post(
                postUrl, data=postData, headers=self.header)
            print(f"statusCode = {self.responseRes.status_code}")
            print(f"text = {self.responseRes.text}")
        except KeyError as e:
            print(
                f"no such a person existed in database {self.searchObj[13].lower()}")

    def login_user(self, user: str, password: str):
        print("login.....")
        postUrl = "http://cms.novogene.com/core/login/login!login.action"
        pd = 1
        if password != '':
            pd = password
        else:
            pass
        try:
            if list(filter(lambda x: x in [TS_DICT[y][2] for y in TS_DICT], [user])):
                postData = {
                    "loginInfo.usercode": user,
                    "loginInfo.userpass": pd,
                    "loginInfo.islocal": "1",
                }
                self.responseRes = self.CMS_Session.post(postUrl, data=postData, headers=self.header)
                print(f"statusCode = {self.responseRes.status_code}")
                message = json.loads(self.responseRes.text)['loginMessage']
                if message == '该域用户无法访问系统，请联系系统管理员！':
                    raise KeyError(f'username or password is not correct')
                else:
                    pass
                print(f"text = {self.responseRes.text}")
                # CMS_Session.cookies.save(ignore_discard=True, ignore_expires=True)
            else:
                raise KeyError(f"no such a person existed in database")
        except KeyError as e:
            raise KeyError(f'{e}')

    def update_producttype(self):
        '''
        this module could help to generate the AA_dict,
        the AA_dict has all product type and AAcode in US
        '''
        print("trying to grab all the data.......")
        process_info_url = 'http://cms.novogene.com/nhzy/qmprocess/process!selectProcessInfosForProcessname.action'
        processtype_url = 'http://cms.novogene.com/nhzy/qmprocess/process!selectProcessInfosForProcesstype.action'
        AA_url = 'http://cms.novogene.com/nhzy/qmproduct/product!selectProductInfosByCond.action'
        AA_dict = {}
        # search AA
        AA_post = {
            "cond.auditflag": '2',
            "cond.bcompany": '202',
            "cond.isnewversion": 'Y',
            "cond.salesid": "",
            "jsonString": '{"cond":{"productcode":"AA"}}',
            "page": '1',
            "start": '0',
            "limit": '100'
        }
        # search product
        post = {
            "cond.productcode": "",
            "cond.isforprocess": "N",
            "cond.isstandard": "N",
            "page": '1',
            "start": '0',
            "limit": '25'
        }
        # search product_type
        post_type = {
            "cond.productcode": "",
            "cond.processname": "",
            "page": '1',
            "start": '0',
            "limit": '25'
        }
        # update AA list
        AA = self.CMS_Session.post(AA_url, headers=self.header, data=AA_post)
        # test if login
        assert (not ("sessionisnull" in AA.text)), "please login first"
        # update producttype and AA_list
        for i in json.loads(AA.text)['productInfos']:
            # print(i['productcode']+':'+i['productdesc'])
            AA_dict.update({i['productcode']: {i['productcode']: {
                i['productcode']: i['productdesc']}}})
        for x in AA_dict.keys():
            post.update({"cond.productcode": x})
            post_type.update({"cond.productcode": x})
            process = self.CMS_Session.post(
                process_info_url, headers=self.header, data=post)
            process_dict = json.loads(process.text)
            for i in process_dict['vmaps']:
                AA_dict[x].update(
                    {i['PROCESSNAME']: {i['PROCESSNAME']: i['PROCESSNAMEDESC']}})
                post_type.update({"cond.processname": i['PROCESSNAME']})
                processtype = self.CMS_Session.post(
                    processtype_url, headers=self.header, data=post_type)
                for p in json.loads(processtype.text)['vmaps']:
                    AA_dict[x][i['PROCESSNAME']].update(
                        {p['PROCESSTYPE']: p['PROCESSTYPEDESC']})
        with open("AA_dict.py", mode='w', encoding='utf-8') as i:
            i.write("AA_dict = " + str(AA_dict) + "\n")

    def country_dict_generator(self):
        country_dict = {}
        country_url = "http://cms.novogene.com/crm/addresscombo/addresscombo!selectAddresscomboInfoForCombo.action"
        post = {
            "cond.parentid": "122703",
            "cond.addrlevel": "crm_country"
        }
        search = self.CMS_Session.post(country_url, headers=self.header, data=post)
        country_list = json.loads(search.text)["addresscomboInfos"]
        for x in range(len(country_list)):
            country_dict.update({country_list[x]['addrdesc']: country_list[x]['addrid']})
        with open("country_dict.py", mode='w', encoding='utf-8') as i:
            i.write("country_dict = " + str(country_dict) + "\n")


if __name__ == "__main__":
    new_process = database()
    new_process.login_user('jerry.jie', '0128Xx@gina')
    new_process.update_producttype()
    new_process.country_dict_generator()
