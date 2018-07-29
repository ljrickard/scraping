#!/usr/bin/env python3
import requests
import logging
import json
from http import HTTPStatus

logger = logging.getLogger(__name__)
FILTER_BRAND_BODY_FILE = 'components/data_access/json_files/es_filter_brand.json'
PRODUCT_SCHEMA_FILE = 'components/data_access/json_files/es_product_schema.json'
ELASTIC_SEARCH_ENDPOINT = 'http://52.87.204.186:9200'
INDEX = 'products'
TYPE = 'skincare'


class AwsEs():

    def __init__(self):
        self.es_url = ELASTIC_SEARCH_ENDPOINT

    def push_product_to_es(self, payload):
        response = self._post_payload_to_es(payload)
        if response.status_code == HTTPStatus.CREATED:
            return self._create_product_urls(response)

    def _create_product_urls(self, response):
        return ['%s/products/skincare/%s' % (ELASTIC_SEARCH_ENDPOINT, json.loads(response.text)['_id'])]

    def _post_payload_to_es(self, payload):
        logger.info(self.es_url + '/products/skincare/' + payload['id'])
        headers = {'content-type': 'application/json'}
        response = requests.post(
            (self.es_url + '/products/skincare/' + payload['id']), data=json.dumps(payload), headers=headers)
        logger.info('Response from eastic search post request %s', response.text)
        return response

    def _create_products_mapping(self):

        # curl -XPUT -H 'Content-Type: application/json' 'localhost:9200/products/'
        # curl -XPUT -H 'Content-Type: application/json' 'localhost:9200/products/_mapping/skincare' -d '{"properties":{"name":{"type":"text"}}}'

        payload = json.loads(open(PRODUCT_SCHEMA_FILE).read())
        headers = {'Content-Type': 'application/json'}
        response = requests.put((self.es_url + '/products/'))
        logger.info('Response from eastic search create_products_mapping %s', response.text)


        response = requests.put((self.es_url + '/products/_mapping/skincare'), data=json.dumps(payload), headers=headers)
        logger.info('Response from eastic search create_products_mapping %s', response.text)

    def clear_all_es_data(self):
        response = requests.delete(self.es_url + '/products')
        logger.info('Response from eastic search post request %s',
                    response.text)

    def get_existing_product_urls(self, brand):
        payload = json.loads(open(FILTER_BRAND_BODY_FILE).read())
        payload['query']['bool']['filter'][0]['term']['brand'] = brand
        logger.info('Sending payload %s', payload)
        response = requests.post(
            (self.es_url + '/products/_search?size=0'), data=json.dumps(payload))
        if response.status_code != 200:
            logger.warn('%s not found - http response:%s',
                        brand, response.status_code)
            return []
        hits = int(json.loads(response.text)['hits']['total'])
        logger.info('Total hits found %s', hits)
        response = requests.post(
            (self.es_url + '/products/_search?size=1000'), data=json.dumps(payload))
        logger.info('Response recieved %s', response.status_code)
        return [existing_product_url['_source']['source_url'] for existing_product_url in json.loads(response.text)['hits']['hits']]
