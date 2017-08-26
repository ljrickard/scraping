#!/usr/bin/env python3
import logging
import requests
import json
from bs4 import BeautifulSoup as bs
from http import HTTPStatus
import sys

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')
logger = logging.getLogger(__name__)

BASE_URL = "http://www.kiehls.co.uk"
SITE_MAP = "/site-map.html"

def get_hrefs(soup, keyword):
	return [a.get('href') for a in soup.find_all('a') if keyword in a.get('href')]


logging.info("Scraping site %s", BASE_URL)

site_map_response = requests.get(BASE_URL + SITE_MAP)

#logging.info("http status_code=%s recieved from %s", site_map_response.status_code, BASE_URL + SITE_MAP)

soup = bs(site_map_response.text,  "html.parser")

skin_care_hrefs = get_hrefs(soup, 'skin-care') # create regex containing skin care

print(skin_care_hrefs)




