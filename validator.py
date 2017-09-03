import json, logging

logger = logging.getLogger(__name__)

class Validator():

	def __init__(self, product_template):
		self.product_template = product_template
		self.validation_message = ''

	def validate_products(self, products):
		self.validation_message = ''
		for product in products:
			if self.validate_product(product):
				self.validation_message
		return self.validation_message

	def validate_product(self, product):
		logger.info('Validating product URL=%s', product['source_url'][0])
		self.validation_message = ''
		if len(self.product_template) != len(product):
			self.validation_message = 'Product template mismatch'
			return self.validation_message

		for key, value in product.items():
			if not value:
				self.validation_message = 'key=%s has no value' % key
				return self.validation_message

		return self.validation_message

