#!/usr/bin/env python3
import logging, json
from data_access import DataAccess
from validator import Validator
from website_factory import Website
from logging.config import fileConfig

PRODUCT_TEMPLATE_FILE = 'product.json'
BRANDS = ['kiehls']

#http://bugs.python.org/file4410/logging.py
logging.basicConfig(level=logging.INFO, format='%(asctime)s: (%(processName)s: %(process)d) %(levelname)-2s - %(module)-2s(%(lineno)d): %(message)s') 
logger = logging.getLogger(__name__)


def run(dry_run=False):
	product_template = json.loads(open(PRODUCT_TEMPLATE_FILE).read())

	dataAccess = DataAccess(dry_run)
	validator = Validator(product_template)

	for brand in BRANDS:
		site = Website.factory(product_template, brand)
		if site:
			product_urls = site.get_product_urls()
			logger.info('Total products found is %s', len(product_urls))
			product_urls = dataAccess.filter_existing_products(brand, product_urls)
			logger.info('Total new products found is %s', len(product_urls))
			#validation_result = validator.validate_products(products)
			products = site.scrape_product_urls(product_urls)
			dataAccess.save_products(products)
			#logger.info('Total products scraped: %s', len(products))
		else:
			logger.error('Website not found: %s', website)


if __name__ == "__main__":
	run(dry_run=True)


# TODO: 

##### general #######
#check if website still valid
#check for new products
#scrape and store new products
#put screen scrape into try/catch - only save if no error reported
#need to remove 100 hardcoding from es - number of results returned

##### ES specific #####
#limit data returned by ES - for example: dont return source urls
#remove one of product/products from url

##### kiehls specific #####
#collect price and currency data
#need to get primary image
#improve get_tags to handle regex for - and /
#update size to measurements
#update size/measurement to dict {'ml': ['30', '75']}

#bugs:
	#"http://www.kiehls.co.uk/skin-care/category/eyes-lips/scented-lip-balm--1/696.html"
		#"size": [
        #["Pear"],
        #["Mango"],
        #["Mint"],
        #["Cranberry"],
        #["15", "ml"]

	#"http://www.kiehls.co.uk/men-s/category/moisturisers-for-men/age-defender-moisturizer/KHL413.html"
		#ingredients:
			#"The strengthening protein blend": "in the formula helps firm skin and improve its resiliency and elasticity."

	#"http://www.kiehls.co.uk/skin-care/collection/activated-sun/activated-sun-protector-lotion-for-body-spf-50/1806.html"
		#"Patented Sun Filter Technology": "Avobenzone (UVA Filter), Homosalate (UVB Filter), Octisalate (UVB Filter), Octocrylene (UVB Filter), Oxybenzone (UVA/UVB Filter)"

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

#remove None from products - remove lamda expression above! - DONE