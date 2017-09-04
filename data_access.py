import json, logging
from aws import Aws
from elastic_search import ElasticSearch

logger = logging.getLogger(__name__)
ELASTIC_SEARCH_ENDPOINT = 'https://search-myesdomain-6nzvchl3slhk2di6fpbdb3i3zq.us-east-1.es.amazonaws.com'

class DataAccess():

	def __init__(self):
		self.aws = Aws()
		self.es = ElasticSearch(ELASTIC_SEARCH_ENDPOINT)

	def save_products(self, products):
		for product in products:
			self.save_product(product)

	def save_product(self, product):
		self._save_images(product)
		self._write_product_to_file(product)	
		self._push_product_to_es(product)

	def _save_images(self, product):
		s3_images = []
		source_images = product['source_images']
		for source_image in source_images:
			s3_images.append(self.aws.save_image_to_s3(source_image))
		product['s3_images'] = s3_images

	def _write_product_to_file(self, product):
		with open('testfile.json', 'a') as file:
			json.dump(product, file)
			file.write('\n')	

	def _push_product_to_es(self, product):
		self.es.push_product_to_es(product)
