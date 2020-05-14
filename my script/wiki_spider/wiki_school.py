import requests
import urllib
import json
import re
from bs4 import BeautifulSoup
import pandas as pd
# import googlemaps
from datetime import datetime



file = pd.read_csv("client_info.csv")

pd_school = file.drop_duplicates(subset='Company name', keep="last")[
    "Company name"]

def wiki_search(school_name):
    main_url = "https://en.wikipedia.org/wiki/"
    search_url = main_url + school_name
    html = requests.get(search_url)
    r = BeautifulSoup(html.text, features='lxml')
    information = r.find("table", {"class": "infobox vcard"})
    return information

def google_map_search(school_name):
    school_dict = dict()
    url_json = "https://maps.googleapis.com/maps/api/place/textsearch/json?query="
    query = school_name
    query = query.replace(' ', '+')
    my_key = '&key=AIzaSyCpMizkSRRC72cymY_75vIvXU88M9at_Fo'
    text_search = url_json + query + my_key
    text_search_result = requests.get(text_search)
    try:
        place_id = text_search_result.json()["results"][0]["place_id"]
        address = text_search_result.json()["results"][0]["formatted_address"]
        zip_code = re.search('\d{5}(-\d{4})?', address).group(0)
        school_dict.update(
            {school_name:
                {"place_id":place_id, 
                "address":address,
                "zip_code":zip_code,
                }})
    except (RuntimeError, TypeError, NameError, AttributeError):
        pass
    url_detail = "https://maps.googleapis.com/maps/api/place/details/json?"
    place_id_result = "place_id=" + school_dict[school_name]["place_id"]
    Field = "&fields=name,formatted_phone_number"
    detail_search = url_detail + place_id_result +Field + my_key
    
    try:
        detail_search_result = requests.get(detail_search)
        phone = detail_search_result.json()["result"]["formatted_phone_number"]
        school_dict[school_name].update({"phone": phone})
    except (RuntimeError, TypeError, NameError):
        pass
    
    return text_search_result, detail_search_result, school_dict


x, y, z = google_map_search("Tuskegee University")
