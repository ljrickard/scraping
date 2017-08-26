#!/usr/bin/env python3

import requests
import json
from bs4 import BeautifulSoup as bs
request = requests.get("http://www.kiehls.co.uk/skin-care/category/view-all-skincare")
print(request.status_code)
soup = bs(request.text,  "html.parser") 
#print(soup)
#some_elements = soup.find_all("a", class_="product_name")

result_list = soup.find_all("div", class_="search_result_items")
#print(len(result_list))

all_products = soup.find_all("div", class_="product_tile_wrapper b-product_tile-wrapper ")
#print(len(all_products))
#print(all_products)

product_ids = soup.find_all("div", class_="b-custom-product_tile-wrapper js-product-details")
#print(len(product_ids))

def has_class_but_no_id(tag):
    return tag.has_attr('data-product-url')

product_urls = soup.find_all(has_class_but_no_id)

for product_url in product_urls:
	print(product_url['data-product-url'])
#data-product-url

#for product in product_ids:
#	print(json.loads(product['data-trackinginfo'])['productID'])
#	print(json.loads(product['data-trackinginfo'])['productName'])

# exclude duplicate products / collections

#{'itemtype':'http://schema.org/GeoCoordinates'}
# some_elements = soup.find_all("a", class_="product_name")
#from urllib.request import urlopen
#page = urlopen("http://www.kiehls.co.uk/skin-care/category/view-all-skincare")
#soup = bs(page, "html.parser") 

#itemtype="http://schema.org/Product"
#some_elements = soup.find_all('div', {'itemtype':'http://schema.org/Product'})
#print(len(some_elements))
#for element in some_elements:
#	print(element)


#some_elements = soup.find_all("div", itemtype="http://schema.org/Product")
#print(len(some_elements))