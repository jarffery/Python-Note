import requests
import urllib
import json
import re
from bs4 import BeautifulSoup
import pandas as pd
import googlemaps
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
    query = school_name
    query = query.replace(' ', '+')
    gmaps = googlemaps.Client(key='AIzaSyA2p0RV-5We0ZvFSu1rGd_IPe82R32zld0')
    geocode_result = gmaps.geocode(school_name)
    
for i in pd_school:
    str(i).replace(" ","_")


school_name = "Tuskegee_University"
school_name = "Tuskegee University"
google_search(school_name)
wiki_search(school_name)
