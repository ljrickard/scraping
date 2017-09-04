#!/usr/bin/env python3
import logging, json
from data_access import DataAccess
from validator import Validator
from website_factory import Website

PRODUCT_TEMPLATE_FILE = 'product.json'
WEBSITES = ['kiehls']

#http://bugs.python.org/file4410/logging.py
logging.basicConfig(level=logging.INFO, format='%(asctime)s: (%(processName)s: %(process)d) %(levelname)-2s - %(module)-2s(%(lineno)d): %(message)s') 
logger = logging.getLogger(__name__)

product_template = json.loads(open(PRODUCT_TEMPLATE_FILE).read())

dataAccess = DataAccess()
validator = Validator(product_template)

for website in WEBSITES:
	site = Website.factory(product_template, website)
	if site:
		products = site.execute()
		products = list(filter(lambda product: product is not None, products))
		#validation_result = validator.validate_products(products)
		dataAccess.save_products(products)
		logger.info('Total products scraped: %s', len(products))
	else:
		logger.warn('Website not found: %s', website)

# TODO: 

##### general #######
#check if website still valid
#check for new products
#scrape and store new products
#limit data returned by ES - for example: dont return source urls

##### kiehls specific #####
#collect price and currency data
#need to get primary image
#improve get_tags to handle regex for - and /

#exclude collections - DONE
#save image to S3 bucket - DONE
#parse size data into 2 parts - DONE
#check urls to create male/female category - DONE
#add tags list - gender - words from the url - DONE
#check for additional images - DONE
#provide json to scraper - every site returns the same format - DONE
#move sites to factory - DONE
#add validation - DONE
#move persistence to data_access layer - DONE
