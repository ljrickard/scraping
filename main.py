#!/usr/bin/env python3
import logging, json, time
from components.data_access.data_access import DataAccess
from components.data_access.validators.validator import Validator
from components.comms.comms import Comms
from sites.site_factory import Site
from logging.config import fileConfig

BRANDS = ['kiehls']

#http://bugs.python.org/file4410/logging.py
logging.basicConfig(level=logging.INFO, format='%(asctime)s: (%(processName)s: %(process)d) %(levelname)-2s - %(module)-2s(%(lineno)d): %(message)s') 
logger = logging.getLogger(__name__)


def run(dry_run=False):
	start_time = time.time()
	dataAccess = DataAccess(dry_run)
	validator = Validator(dataAccess.get_product_template())
	comms = Comms()
	details = {}

	for index, brand in enumerate(BRANDS):
		site = Site.factory(dataAccess.get_product_template(), brand)
		details[index] = {}
		details[index]['brand'] = brand
		if site:
			product_urls = site.get_product_urls()
			logger.info('Total products found is %s', len(product_urls))
			details[index]['total_products_found'] = len(product_urls)
			new_product_urls = dataAccess.filter_existing_products(brand, product_urls)
			details[index]['total_new_products_found'] = len(new_product_urls)
			logger.info('Total new products found is %s', len(product_urls))
			products = site.scrape_product_urls(product_urls)
			details[index]['product_urls'] = dataAccess.save_products(products)
			logger.info('Total products scraped: %s', len(products))
		else:
			logger.error('Site not found: %s', site)

	logger.info('Sending report')
	comms.send(1, details)
	seconds = time.time() - start_time
	m, s = divmod(seconds, 60)
	h, m = divmod(m, 60)
	total_run_time = "%d:%02d:%02d" % (h, m, s)

	logger.info("Total run time is: %s", total_run_time)


if __name__ == "__main__":
	run(dry_run=False)

# TODO: 

##### general #######
#check if website still valid - general check prior to scraping site
#check for new products
#scrape and store new products
#put screen scrape into try/catch - only save if no error reported
#need to remove 1000 hardcoding from es - number of results returned - break number into buckets
#move to use env variables
#add validation to data access layer
#dataAccess.save_products(products) - should return urls to our site
#need to get new product id when pushing product to es
#wrap in try/catch to prevent persisting data when error thrown


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
