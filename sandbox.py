#!/usr/bin/env python3
from sites.clarins import Clarins
from sites.kiehls import Kiehls
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s: (%(processName)s: %(process)d) %(levelname)-2s - %(module)-2s(%(lineno)d): %(message)s') 
logger = logging.getLogger(__name__)
#PRODUCT_TEMPLATE_FILE = 'product.json'
#site = Kiehls(PRODUCT_TEMPLATE_FILE)
#product_urls = site.get_product_urls()

from components.comms.aws_email import AwsEmail

#email_service = AwsEmail()
#email_service.send_email()

from components.comms.comms import Comms

details = {'0': {
					'brand': 'kiehls', 
					'total_products_found': 95,
					'total_new_products_found': 12,
					'product_urls': [['source.com/1', 'elastic.com/1'], ['source.com/2', 'elastic.com/2'], 
										['source.com/3', 'elastic.com/3'], ['source.com/4', 'elastic.com/4']]	
				},
			
			'1': {
					'brand': 'clarins', 
					'total_products_found': 195,
					'total_new_products_found': 112,
					'product_urls': [['source.com/1', 'elastic.com/1'], ['source.com/2', 'elastic.com/2'], 
										['source.com/3', 'elastic.com/3'], ['source.com/4', 'elastic.com/4']]		
				},

			'2': {
					'brand': 'nivea', 
					'total_products_found': 951,
					'total_new_products_found': 121,
					'product_urls': [['source.com/1', 'elastic.com/1'], ['source.com/2', 'elastic.com/2'], 
										['source.com/3', 'elastic.com/3'], ['source.com/4', 'elastic.com/4']]	
				},
			}

comms = Comms()
#print(comms._generate_html(details))
comms.send(1, details)


#from components.data_access.data_access import DataAccess
#dataAccess = DataAccess(True)

#dataAccess._write_product_to_file(None)


# if __name__ == "__main__":
# 	logging.basicConfig(level=logging.INFO, format='%(asctime)s: (%(processName)s: %(process)d) %(levelname)-2s - %(module)-2s(%(lineno)d): %(message)s')
# 	es = ElasticSearch()
# 	result = es.get_existing_product_urls('kiehls')
# 	logger.info('Found %s products', len(result))
# 	#logger.info('Found %s', result)



	