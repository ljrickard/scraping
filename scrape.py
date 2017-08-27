#!/usr/bin/env python3
import logging
import requests
import json
from bs4 import BeautifulSoup as bs
from http import HTTPStatus
import sys, html5lib

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')
logger = logging.getLogger(__name__)

BASE_URL = "http://www.kiehls.co.uk"
SITE_MAP = "/site-map.html"

def make_soup(url):
	return bs(requests.get(url).text,  "html5lib")

def get_hrefs(soup, keyword):
	return [a.get('href') for a in soup.find_all('a') if keyword in a.get('href')]

def get_product_urls(skin_care_hrefs):
	products = set()

	for href in skin_care_hrefs:
		for product_href in [a.get('href') for a in make_soup(href).find_all('a', class_='product_name')]:
			if BASE_URL in product_href:
				products.add(product_href)
			else:
				products.add(BASE_URL+product_href)

	return products

#skin_care_hrefs = get_hrefs(make_soup(BASE_URL + SITE_MAP), 'skin-care') # create regex containing skin care + base url
#get_product_urls(skin_care_hrefs)

def has_class_but_no_id(tag):
    return tag.has_attr('data-trackinginfo')

#soup = make_soup("http://www.kiehls.co.uk/skin-care/category/serums/hydro-plumping-re-texturizing-serum-concentrate/255.html")
soup = make_soup("http://www.kiehls.co.uk/skin-care/category/facial-masks/ultra-facial-overnight-hydrating-masque/3601.html")

# first part locates the tags and the second extracts that particular attribute data
data_trackinginfo = soup.find_all(has_class_but_no_id)[-1].extract().get('data-trackinginfo')
ingredients_copy = soup.find_all('div', id='ing-copy')

#for copy in ingredients_copy:
#	print(copy.get_text())

product_details = soup.find_all('div', class_='l-product_details-wrapper')[-1].extract()
product_names = product_details.find_all('span', class_='product_name')

# for product_name in product_names:
# 	print(product_name.get_text())

product_subtitle_raw = product_details.find_all('h2', class_='product_subtitle')

# for product_subtitle in product_subtitle_raw:
# 	print(product_subtitle.get_text())


def remove_hrefs(tag):
	return not tag.a and not tag.has_attr('href')

product_details_description = product_details.\
									find_all('div', class_='product_detail_description')[-1].extract().\
									find_all(remove_hrefs)

product_description = ''

for copy in product_details_description:	
	copy = copy.get_text().strip().strip('\n').replace('\n', '.')

	while '  ' in copy:
		copy = copy.replace('  ', ' ')

	while '..' in copy:
		copy = copy.replace('..', '.')

	# print(copy.get_text().split('\n'))
	# copy = copy.get_text().replace('\n', '')
	# copy = copy.get_text().rstrip("\n")
	if copy not in product_description:
		product_description+=copy

print(product_description)

# for description in product_description.find_all(remove_hrefs):
# 	print(description.get_text())


#product_details = soup.find_all('div', class_='l-product_details-wrapper')[-1].extract()

























