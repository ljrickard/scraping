import requests, logging, json

logger = logging.getLogger(__name__)

class ElasticSearch():

	def __init__(self, es_url):
		self.es_url = es_url
		self._delete_existing()

	def push_product_to_es(self, product):
		response = requests.post((self.es_url+'/products/product'), data=json.dumps(product))
		logger.info('Response from eastic search post request %s', response.text)
		return response

	def _delete_existing(self):
		response = requests.delete(self.es_url+'/products')
		logger.info('Response from eastic search post request %s', response.text)

