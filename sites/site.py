import logging, time
from components.data_access.data_access import DataAccess
from sites.lib.utils import calculate_run_time

logger = logging.getLogger(__name__)

class Site(object):

	def __init__(self, dry_run):
		self.data_access = DataAccess(dry_run)
		self.product_template = self.data_access.get_product_template()

	def execute(self):
		report = {}
		report['site'] = {}
		report['site']['url'] = self.base_url
		start_time = time.time()
		product_urls = self.get_product_urls()

		logger.info('Total products found is %s', len(product_urls))
		report['site']['total_products_found'] = len(product_urls)
		new_product_urls = self.data_access.filter_existing_products(self.brand, product_urls)
		report['site']['total_new_products_found'] = len(new_product_urls)
		logger.info('Total new products found is %s', len(new_product_urls))
		if len(new_product_urls) < 1:
			report['site']['product_urls'] = []
			logger.info('Total products scraped: %s', len(new_product_urls))
		
		else:
			products = self.scrape_product_urls(new_product_urls)
			report['site']['product_urls'] = self.data_access.save_products(products)
			logger.info('Total products scraped: %s', len(products))

		total_run_time = calculate_run_time(start_time)
		logger.info("Total run time is: %s", total_run_time)
		return report
