import json, logging
from aws import Aws

logger = logging.getLogger(__name__)

class DataAccess():

	def __init__(self):
		self.aws = Aws()

	def save_products(self, products):
		for product in products:
			self.save_product(product)

	def save_product(self, product):

		s3_images = []
		for source_image in product['source_images']:
			s3_images.append(self.aws.save_image_to_s3(source_image))

		product['s3_images'] = s3_images

		logger.info('Writing to testfile.json')
		##### SAVE TO FILE #######
		with open('testfile.json', 'a') as file:
			json.dump(product, file)
			file.write('\n')		