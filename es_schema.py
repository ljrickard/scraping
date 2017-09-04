#!/usr/bin/env python3
import requests, json

URL = 'https://search-myesdomain-6nzvchl3slhk2di6fpbdb3i3zq.us-east-1.es.amazonaws.com/products'

def create_schema():
	es_schema = json.loads(open('es_product_schema.json').read())
	response = requests.put(URL, data=json.dumps(es_schema), headers={'Content-Type':'application/json'})
	print(response.text)


def remove_everything():
	response = requests.delete(URL)
	print(response.text)

#create_schema()

remove_everything()