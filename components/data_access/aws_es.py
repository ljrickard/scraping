#!/usr/bin/env python3
import requests, logging, json
from http import HTTPStatus

logger = logging.getLogger(__name__)
FILTER_BRAND_BODY_FILE = 'es_filter_brand.json'
ELASTIC_SEARCH_ENDPOINT = 'https://search-myesdomain-6nzvchl3slhk2di6fpbdb3i3zq.us-east-1.es.amazonaws.com'

class AwsEs():

	def __init__(self):
		self.es_url = ELASTIC_SEARCH_ENDPOINT
		#self._delete_existing()

	def post_payload_to_es(self, payload):
		response = requests.post((self.es_url+'/products/product'), data=json.dumps(payload))
		logger.info('Response from eastic search post request %s', response.text)

	def _delete_existing(self):
		response = requests.delete(self.es_url+'/products')
		logger.info('Response from eastic search post request %s', response.text)

	def get_existing_product_urls(self, brand):
		payload = json.loads(open(FILTER_BRAND_BODY_FILE).read())
		payload['query']['bool']['filter'][0]['term']['brand'] = brand
		logger.info('Sending payload %s', payload)
		response = requests.post((self.es_url+'/products/_search?size=0'), data=json.dumps(payload))
		hits = int(json.loads(response.text)['hits']['total'])
		logger.info('Total hits found %s', hits) 
		response = requests.post((self.es_url+'/products/_search?size=1000'), data=json.dumps(payload))
		logger.info('Response recieved %s', response.status_code)
		return [existing_product_url['_source']['source_url'] for existing_product_url in json.loads(response.text)['hits']['hits']]


if __name__ == "__main__":
	logging.basicConfig(level=logging.INFO, format='%(asctime)s: (%(processName)s: %(process)d) %(levelname)-2s - %(module)-2s(%(lineno)d): %(message)s')
	es = ElasticSearch()
	result = es.get_existing_product_urls('kiehls')
	logger.info('Found %s products', len(result))
	#logger.info('Found %s', result)
