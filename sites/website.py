import logging
import time
from components.data_access.data_access import DataAccess
from sites.lib.utils import calculate_run_time

logger = logging.getLogger(__name__)

class Website(object):

	def __init__(self, dry_run):
		self.data_access = DataAccess(dry_run)
		self.product_template = self.data_access.get_product_template()

	def execute(self):
		report = {}
		report['url'] = self.base_url
		start_time = time.time()
		product_urls = self.get_product_urls()

		logger.info('Products found: %s', len(product_urls))
		report['products_found'] = len(product_urls)
		new_product_urls = self.data_access.filter_existing_products(self.brand, product_urls)
		report['new_products_found'] = len(new_product_urls)
		logger.info('New products found: %s', len(new_product_urls))

		if len(new_product_urls) > 1:
			products = self.scrape_product_urls(new_product_urls)
			report['product_urls'] = self.data_access.save_products(products)

		runtime = calculate_run_time(start_time)
		report['runtime'] = runtime
		logger.info("Runtime: %s", runtime)
		return report

