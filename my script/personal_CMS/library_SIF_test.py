from process_SIF import SIF
from requests_toolbelt.multipart.encoder import MultipartEncoder
import json
test = SIF()
test.login()
test.SIF_info_submit('NVUS2019121322')
path ='C:/Users/Jerry/OneDrive - Novogene/Project/Dec10-31 new projects/NVUS2019121322/zjkybznzzexcel -2nd.xlsx'
file_url = 'http://cms.novogene.com/nhzy/subproject/znzzsampleinfoimportexecl!importZnzzExeclsample.action'
SIF_data = {
    "businesstype": test.batchID_text['kfappointmentInfo'][0]['businesstype'],
    "batchid": test.batchid,
    "contractid": test.contractid,
    "pcode": "AA032",
    "pname": "Pre-made libraries Lane sequencing",
}
file_url = test.CMS_Session.post(file_url, params = SIF_data)
files = {
    "file": (
        "zjkybznzzexcel -2nd.xlsx", open(path, "rb"), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
}
test.file_response = test.CMS_Session.post(file_url, headers=test.header, data=SIF_data, files=files)
test.file_message = json.loads(test.file_response.text)



header = {
"Host": "cms.novogene.com",
"Connection": "keep-alive",
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
"Referer": "",
"Accept-Encoding": "gzip, deflate",
"Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
}
multipart_encoder = MultipartEncoder(
    fields={
        "businesstype": test.batchID_text['kfappointmentInfo'][0]['businesstype'],
        "batchid": test.batchid,
        "contractid": test.contractid,
        "pcode": "",
        "pname": "",
        # "jsonString":{"uploadFile":{"businesscode":'bill', "businessobjectid":'', "handletype":'1', "otherparam":'null', "version":'null'}},
        "file": ("test", open(path, "rb"), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')},
)

header['Content-Type'] = multipart_encoder.content_type

# file_url = test.CMS_Session.get(file_url, params=SIF_data).url
r = test.CMS_Session.post(file_url, headers=header, data = multipart_encoder)
r.text