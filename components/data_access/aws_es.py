#!/usr/bin/env python3
import requests
import logging
import json
from http import HTTPStatus

logger = logging.getLogger(__name__)
FILTER_BRAND_BODY_FILE = 'components/data_access/json_files/es_filter_brand.json'
ELASTIC_SEARCH_ENDPOINT = 'https://search-myesdomain-rxwevag666yfxh6bjvt5au62iq.us-east-1.es.amazonaws.com'


class AwsEs():

    def __init__(self):
        self.es_url = ELASTIC_SEARCH_ENDPOINT

    def push_product_to_es(self, payload):
        response = self._post_payload_to_es(payload)
        if response.status_code == HTTPStatus.CREATED:
            return self._create_product_urls(response)

    def _create_product_urls(self, response):
        return ['%s/products/product/%s' % (ELASTIC_SEARCH_ENDPOINT, json.loads(response.text)['_id'])]

    def _post_payload_to_es(self, payload):
        response = requests.post(
            (self.es_url + '/products/product'), data=json.dumps(payload))
        logger.info('Response from eastic search post request %s',
                    response.text)
        return response

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
