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

def make_soup(url):
	return bs(requests.get(url).text,  "html.parser")

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
product_details = soup.find_all('div', class_='l-product_details-wrapper')[-1].extract()


#data_trackinginfo = product_details.find_all(has_class_but_no_id)[-1].extract()
#data_trackinginfo2 = data_trackinginfo.get('data-trackinginfo')


ingredients_raw = soup.find_all('div', {'class':['ingredient ', 'ingredient ingredient-hidden']}) #[-1].extract() #class="ingredient "

ingredients = dict()

for ingredient in ingredients_raw:
	if ingredient.div and ingredient.div.h3 and ingredient.div.p:
		#ingredients.add(tuple({ingredient.div.h3.get_text() : ingredient.div.p.get_text()}.items()))
		ingredients[ingredient.div.h3.get_text()] = ingredient.div.p.get_text()

print(len(ingredients))



























