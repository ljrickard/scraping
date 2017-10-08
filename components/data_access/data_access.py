#!/usr/bin/env python3
import json, logging
from components.data_access.aws_s3 import AwsS3
from components.data_access.aws_es import AwsEs

logger = logging.getLogger(__name__)
DRY_RUN_LOCAL_FILE = 'testfile.json'
PRODUCT_TEMPLATE_FILE = 'components/data_access/json_files/product.json'

class DataAccess():

	def __init__(self, dry_run=False):
		self.aws_s3 = AwsS3()
		self.dry_run = dry_run
		if not self.dry_run:
			self.aws_es = AwsEs()
		else:
			logger.warn("Writing to file only as dry_run=%s", self.dry_run)

	def get_product_template(self):
		return json.loads(open(PRODUCT_TEMPLATE_FILE).read())

	def save_products(self, products):
		# add validation for products here
		response=[]
		for product in products:
			product_urls = self._save_product(product)
			response.append(response)
		return response

	def filter_existing_products(self, brand, product_urls):
		if self.dry_run:
			return product_urls
		existing_product_urls = self.aws_es.get_existing_product_urls(brand)
		return self._filter_out_existing_products_urls(product_urls, existing_product_urls)

	def _filter_out_existing_products_urls(self, product_urls, existing_product_urls):
		return [product_url for product_url in product_urls if product_url not in existing_product_urls]

	def _save_product(self, product):
		if self.dry_run:
			self._write_product_to_file(product)
		else:
			self._save_images(product)	
			return self._push_product_to_es(product)

	def _save_images(self, product):
		s3_images = []
		source_images = product['source_images']
		for source_image in source_images:
			s3_images.append(self.aws_s3.save_image_to_s3(source_image))
		product['s3_images'] = s3_images

	def _write_product_to_file(self, product):
		with open(DRY_RUN_LOCAL_FILE, 'a') as file:
			json.dump(product, file)
			file.write('\n')	

	def _push_product_to_es(self, product):
		return self.aws_es.push_product_to_es(product)

	def clear_all_data(self):
		logger.warn("Removing all data via data_access layer")
		self.aws_es.clear_all_es_data()
		self.aws_s3.clear_all_images()



