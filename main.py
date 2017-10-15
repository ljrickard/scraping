#!/usr/bin/env python3
import logging, json, time, pprint
from components.comms.comms import Comms
from sites.brand_factory import Brands

BRANDS = ['kiehls']

#http://bugs.python.org/file4410/logging.py
logging.basicConfig(level=logging.INFO, format='%(asctime)s: (%(processName)s: %(process)d) %(levelname)-2s - %(module)-2s(%(lineno)d): %(message)s') 
logger = logging.getLogger(__name__)


def run(dry_run=False):
	for url in BRANDS:
		site = Brands(dry_run).factory(url)
		site.execute()


if __name__ == "__main__":
	run(dry_run=True)

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
