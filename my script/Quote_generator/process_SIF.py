'''
script can used to submit the SIF automatically. import library from process_submit.py
author: Jerry
date: 1/16/2020
'''

from process_submit import *
from NVUSdatabase import *
from SIF_CMS_json import process_SIF_dict, process_SIF_dict_library
import country_dict


class SIF(database):
    '''get database init'''

    def __init__(self):
        super().__init__()
        self.contract_post = ""

    def json_post(self, data: str):
        '''transfer data to json format'''
        try:
            obj = {
                "jsonString": json.dumps(data),
                "limit": 1,
            }
        except TypeError as e:
            print(e)
            print("Please check data type!")
        return obj

    def contract_search(self, quote: str):
        '''
        this module can search contract number and all info under this contract
        1. input is quote#
        2. will add all info as class value
        '''
        contract_search_url = "http://cms.novogene.com/crm/contract/contractkefu!queryContractInfoByCond.action"
        post = self.json_post({"cond": {"CONTRACTNAME": quote}})
        search = self.CMS_Session.post(contract_search_url, headers=self.header, data=post)
        statusCode = search.status_code
        print(f"statusCode = {statusCode}")
        try:
            self.search_text = json.loads(search.text)
            self.contractInfos = self.search_text['vmaps'][0]
            self.contractid = self.contractInfos['CONTRACTID']
            self.contractno = self.contractInfos['CONTRACTSNO']
            self.quotationid = self.contractInfos['QUOTATIONID']
        except (IndexError, KeyError):
            raise KeyError(f'the {quote} do not have contract yet')

    def information_update(self):
        '''
        this module will update the json form which can update to SIF submit
        '''
        NSHIP = re.compile(r'NVUS(\d+)')
        contractname = self.contractInfos['CONTRACTNAME']
        nshipcode = 'NSHIP' + NSHIP.search(contractname).group(1) + '01'
        try:
            self.update_dict = {
                'contractid': self.contractid,
                'contractno': self.contractno,
                'contractname': self.contractInfos['CONTRACTNAME'],
                'desc22': self.contractInfos['CORPNO'],
                'desc23': self.contractInfos["RECORDERCODE"],
                "corpcontact": self.contractInfos["RECORDERCODE"],
                "expresnumber": nshipcode,
                'corpname': self.contractInfos['DEPTDESC'],
                'projectnum': self.contractInfos["PROJECTNUM"],
                'projectname': self.contractInfos["CONTRACTNAME"],
                'ts_name': self.contractInfos["RECORDERCODE"],
                'salesname': self.contractInfos["SALESMAN"],
            }
        except KeyError as e:
            raise KeyError(f'please check the json name!!')
        try:
            self.update_dict.update({
                'salesemail': self.contractInfos["BEMAIL"],
                "corpemail": self.contractInfos["BEMAIL"],
            }
            )
        except KeyError as e:
            print("no email updated")

    def SIF_info_submit(self, quote: str):
        # check if this is a premade project
        self.quote_name = quote
        self.contract_search(quote)
        self.information_update()
        producttype_url = 'http://cms.novogene.com/nhzy/projectquotation/quotationproduct!selectQuotationproductInfosByCond.action'
        producttype_post = {
            "cond.kfquotationid": self.quotationid
        }
        producttype_search = self.CMS_Session.post(producttype_url, headers=self.header, data=producttype_post)
        try:
            self.producttype_search_text = json.loads(producttype_search.text)
            self.pcode = self.producttype_search_text['quotationproductInfos'][0]['pcode']
        except KeyError:
            raise KeyError(f'cant find the pcode, used SIF_info_submit module!')
        # submit the file to batch ID
        SIF_batchID_url = 'http://cms.novogene.com/nhzy/subproject/kfappointment!insertKfappointmentInfo.action'
        # SIF_batchID_search_url = "http://cms.novogene.com/nhzy/subproject/kfappointment!selectKfappointmentInfoById.action"
        # check if contract is library (different is the businesstype, library: 13, nonlibrary:12)
        library_code = ['AA0032', 'RSSQ00601', 'RSSQ01001', 'RSSQ00501', 'RSSQ01101', 'RSSQ00801', 'RSSQ00901',
                        'RSSQ00701' 'RSSQ01201']
        if list(filter(lambda x: x in library_code, [self.pcode])):
            self.update_SIF_json = process_SIF_dict_library
        else:
            self.update_SIF_json = process_SIF_dict
        # update the necessary info
        self.update_SIF_json['kfappointmentInfo'].update(self.update_dict)
        post = self.json_post(self.update_SIF_json)
        # post.update({"businesstype":12,"islocal":0,})
        search = self.CMS_Session.post(SIF_batchID_url, headers=self.header, data=post)
        statusCode = search.status_code
        print(f"statusCode = {statusCode}")
        try:
            self.batchID_text = json.loads(search.text)
            self.batchid = self.batchID_text['kfappointmentInfo'][0]['batchid']
            self.batchno = self.batchID_text['kfappointmentInfo'][0]['batchno']
            self.update_dict.update({"batchid": self.batchid, "batchno": self.batchno})
            self.project_info = dict({self.quote_name: self.update_dict})
        except json.decoder.JSONDecodeError as e:
            raise KeyError(f'cant get any info!')

    def file_submit(self, file_name: str, file_path: str):
        '''
        this module will upload file to CMS
        check this link for reference: https://blog.csdn.net/xuezhangjun0121/article/details/82023320
        :param file_name:
        :param file_path:
        :return:
        '''
        file_url = 'http://cms.novogene.com/nhzy/subproject/znzzsampleinfoimportexecl!importZnzzExeclsample.action'
        SIF_data = {
            "businesstype": self.batchID_text['kfappointmentInfo'][0]['businesstype'],
            "batchid": self.batchid,
            "contractid": self.contractid,
        }
        # form-data upload
        file_open = open(file_path, "rb")
        files = {
            "file": (
                file_name, file_open, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
        }
        self.file_response = self.CMS_Session.post(file_url, headers=self.header, data=SIF_data, files=files)
        self.file_message = json.loads(self.file_response.text)
        file_open.close()
        if self.file_message['success']:
            self.message = 'success :D'
        else:
            try:
                self.message = re.compile(r'(\d+\|\d+)').search(self.file_message["errors"]).group(1)
            except KeyError:
                raise
        statusCode = self.file_response.status_code
        print(f"statusCode = {statusCode}")

    def sample_check(self):
        from SIF_CMS_json import sample_update_dict
        '''under testing'''
        sample_url = 'http://cms.novogene.com/nhzy/subproject/kfsampleinfo!selectKfsampleinfoInfosByCond.action'
        product_type_url1 = 'http://cms.novogene.com/nhzy/subproject/subproject!selectSubprojectInfosByProjectnum.action'
        product_type_url2 = 'http://cms.novogene.com/nhzy/subproject/subprojectquoprocess!selectSubprojectquoprocessInfosByPcode.action'
        data_type_url = 'http://cms.novogene.com/nhzy/subproject/subprojectquoprocess!selectSubprojectquoprocessInfosByProcessname.action'
        sample_info_update_url = 'http://cms.novogene.com/nhzy/subproject/kfsampleinfo!checkKfsampleinfoInfo.action'
        batch_id = {
            "limit": 10000,
            "cond.batchid": self.batchid,
            "page": 1,
            "start": 0,
        }
        # check samples info
        self.sample_response = self.CMS_Session.post(sample_url, headers=self.header, data=batch_id)
        self.sample_list = json.loads(self.sample_response.text)["kfsampleinfoInfos"]
        post_product1 = {
            "cond.contractno": self.project_info[self.quote_name]['contractno']
        }
        search_product1 = self.CMS_Session.post(product_type_url1, headers=self.header, data=post_product1)
        self.sample_product_type1 = json.loads(search_product1.text)
        self.pcode = self.sample_product_type1['subprojectInfos'][0]['pcode']
        post_product2 = {
            "cond.contractno": self.project_info[self.quote_name]['contractno'],
            "cond.pcode": self.pcode
        }
        search_product2 = self.CMS_Session.post(product_type_url2, headers=self.header, data=post_product2)
        self.sample_product_type2 = json.loads(search_product2.text)
        post_data_type = {
            "cond.contractno": self.project_info[self.quote_name]['contractno'],
            "cond.pcode": self.pcode
        }
        search_data = self.CMS_Session.post(data_type_url, headers=self.header, data=post_data_type)
        self.sample_data = json.loads(search_data.text)
        self.sample_dict = {
            "desc10": self.sample_product_type1['subprojectInfos'][0]['pname'],
            "desc4": self.pcode,
            "desc16": self.sample_product_type2['vmaps'][0]['processtypecode'],
            "librariytype": self.sample_product_type2['vmaps'][0]['processtype'],  # library 还拼错了居然:(
            "datas": self.sample_data["infos"][0]["datasize"],
            "dataunit": self.sample_data["infos"][0]["dataunit"],
            "teststrategy": "PE150",
            # "samplestatus": "Dissolved in ddH2O",
            # "sampletype":"total RNA",
            # "speciestype" : "animal",
            "subprojectdesc": self.update_dict['projectname'],
            "subprojectnum": str(self.update_dict['projectnum']) + "-Z01",
        }
        self.sample_submit_dict = list()
        for i in range(len(self.sample_list)):
            self.sample_list[i].update(self.sample_dict)
            self.sample_submit_dict.append({key: self.sample_list[i][key] for key in (
                    sample_update_dict["kfsampleinfoInfos"][0].keys() & self.sample_list[i].keys())})
        post_sampleinfo = self.json_post({"kfsampleinfoInfos": self.sample_submit_dict})
        self.search_sampleinfo = self.CMS_Session.post(sample_info_update_url, headers=self.header,
                                                       data=post_sampleinfo)

#test use
#sys.path.extend(['C:\\Users\\Jerry\\Documents\\GitHub\\Note-Python\\my script', 'C:/Users/Jerry/Documents/GitHub'])
# path = 'C:/Users/jerry/onedrive-work/OneDrive - Novogene/Project/premade-hiseq/2020-05/Davis-US-CCHMC-1-premade-1-lane-WOBI-NVUS2020051818/NovoLibrarySIF-NVUS2020051818-filled.xlsx'
# quote = 'NVUS2020051818'
# test = SIF()
# test.login()
# test.SIF_info_submit(quote)
# test.file_submit('test', path)
# test.sample_check()
