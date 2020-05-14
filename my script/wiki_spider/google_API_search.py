import requests
import urllib
import json
import re
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import csv


class google_search(object):
    def __init__(self, filename, column_name, API_key):
        self.filename = filename
        self.column_name = column_name
        self.API_key = API_key
    def read_csv(self):
        pd_file = pd.read_csv(self.filename)
        pd_school = pd_file.drop_duplicates(subset=self.column_name, keep="last")[
            self.column_name]
        self.school = pd_school[~pd_school.isnull()]
        self.school_dict = dict()
        self.noschool_list = list()
    def google_map_search(self, school_name):
        url_json = "https://maps.googleapis.com/maps/api/place/textsearch/json?query="
        query = school_name
        query = query.replace(' ', '+')
        my_key = '&key=' + self.API_key
        text_search = url_json + query + my_key
        text_search_result = requests.get(text_search)
        #assign the blank value
        place_id = str()
        address = str()
        state = str()
        zip_code = str()
        phone = str()
        try:
            place_id = text_search_result.json()["results"][0]["place_id"]
            address = text_search_result.json()["results"][0]["formatted_address"]
            state = re.search(' [A-Z][A-Z] ', address).group(0).strip()
            zip_code = re.search('\d{5}(-\d{4})?', address).group(0)
        except (KeyError, RuntimeError, TypeError, NameError, AttributeError, IndexError):
            pass
        self.school_dict.update({school_name:{"place_id": place_id,"address": address,"zip_code": zip_code,"state": state,}})
        url_detail = "https://maps.googleapis.com/maps/api/place/details/json?"
        place_id_result = "place_id=" + self.school_dict[school_name]["place_id"]
        Field = "&fields=name,formatted_phone_number"
        detail_search = url_detail + place_id_result +Field + my_key
        try:
            detail_search_result = requests.get(detail_search)
            phone = detail_search_result.json()["result"]["formatted_phone_number"]
        except (KeyError, RuntimeError, TypeError, NameError, IndexError, AttributeError):
            pass
        self.school_dict[school_name].update({"phone": phone})


if __name__ == "__main__":
    # main_script
    file_name = input("Please input your file name and path (./example.csv): ")
    column_name = input("Please input the Column name that you want to process: ")
    Google_API = input("Please input your google map API: ")
    search = google_search(file_name, column_name, Google_API)
    # search = google_search('client_info_2.csv', 'School', 'AIzaSyCpMizkSRRC72cymY_75vIvXU88M9at_Fo')
    search.read_csv()
    for i in search.school:
        print(i)
        try:
            search.google_map_search(i)
        except KeyError:
            search.noschool_list.append(i)
            pass 

    #write to csv
    school_dataframe = pd.DataFrame.from_dict(search.school_dict, orient='index', dtype=None, columns=None)
    noschool_dataframe = pd.DataFrame({'school_not_found': search.noschool_list})
    school_dataframe.to_csv("./school_info.csv")
    noschool_dataframe.to_csv("./noschool_info.csv")
