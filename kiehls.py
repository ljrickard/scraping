#!/usr/bin/env python3
import logging, datetime, requests, json, sys, html5lib
from bs4 import BeautifulSoup as bs
from http import HTTPStatus
from utils import aws

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')
logger = logging.getLogger(__name__)

BRAND = "kiehls"
BASE_URL = "http://www.kiehls.co.uk"
SITE_MAP = "/site-map.html"
aws = aws()

def make_soup(url):
	return bs(requests.get(url).text,  "html5lib")

def get_hrefs(soup, keyword):
	return [a.get('href') for a in soup.find_all('a') if keyword in a.get('href')]

def get_product_urls(skin_care_hrefs):
	products = set()

	for href in skin_care_hrefs:
		for product_href in [a.get('href') for a in make_soup(href).find_all('a', class_='product_name')]:
			if BASE_URL in product_href:
				products.add(product_href)
			else:
				products.add(BASE_URL+product_href)

	return products

def scrape_product(url):

	################## scrape product #######################################

	#soup = make_soup("http://www.kiehls.co.uk/skin-care/category/serums/hydro-plumping-re-texturizing-serum-concentrate/255.html")
	#soup = make_soup("http://www.kiehls.co.uk/skin-care/category/facial-masks/ultra-facial-overnight-hydrating-masque/3601.html")

	logger.info('Scraping %s', url)

	soup = make_soup(url)

	product = {}

	######## brand ############
	product['brand'] = BRAND

	######## product name #######
	product_details = soup.find_all('div', class_='l-product_details-wrapper')[-1].extract()
	product_names = product_details.find_all('span', class_='product_name')

	for name in product_names:
	  	product['name'] = name.get_text()

	###### tagline ###########
	product_subtitle_raw = product_details.find_all('h2', class_='product_subtitle')

	for product_subtitle in product_subtitle_raw:
		product['tagline'] = product_subtitle.get_text()

	##### description #######
	def remove_hrefs(tag):
		return not tag.a and not tag.has_attr('href')

	# product_details_description = product_details.\
	# 									find_all('div', class_='product_detail_description')[-1].extract().\
	# 									find_all(remove_hrefs)

	# product_description = ''

	# for copy in product_details_description:	
	# 	copy = copy.get_text().strip().strip('\n').replace('\n', '.')

	# 	while '  ' in copy:
	# 		copy = copy.replace('  ', ' ')

	# 	while '..' in copy:
	# 		copy = copy.replace('..', '.')

	# 	if copy not in product_description:
	# 		product_description+=copy

	product['description'] = ''

	##### metadata #######
	def has_class_but_no_id(tag):
	    return tag.has_attr('data-trackinginfo')

	# first part locates the tags and the second extracts that particular attribute data
	product['metadata'] = soup.find_all(has_class_but_no_id)[-1].extract().get('data-trackinginfo')

	##### ingredients #######
	ingredients_raw = soup.find_all('div', id='ing-copy')

	def extract_text(input, start):
		right_index = input.index('</', start)
		return input[input[:right_index].rfind('>')+1:right_index]

	def extract_ingredient(ingredient_raw):
		ingredient = extract_text(str(ingredient_raw), 0)
		ingredient_description = extract_text(str(ingredient_raw), str(ingredient_raw).index('</')+1)
		return {ingredient:ingredient_description}

	product['ingredients'] = [extract_ingredient(ingredient_raw) for ingredient_raw in ingredients_raw]

	##### size #######
	def has_item_prop(tag):
	    return tag.has_attr('itemprop')

	def has_data_pricevalue_and_data_pricemoney(tag):
	    return tag.has_attr('data-pricevalue') and tag.has_attr('data-pricemoney')

	product_size = product_details.find_all(has_data_pricevalue_and_data_pricemoney)
	product['size'] = [item.get_text().strip().strip('\n').split() for item in product_size]

	##### images #######
	images = product_details.find_all('img', class_='primary_image product_image')
	source_images = [image.get('data-hires-img') for image in images] 

	s3_images = []
	for source_image in source_images:
		s3_images.append(aws.save_to_s3(source_image))

	product['s3_images'] = s3_images
	product['source_images'] = source_images

	##### source #######
	product['source_url'] = [url]

	##### GENDER #######
	def get_gender():
		if 'men' in url:
			return ['MALE']
		if 'women' in url:
			return ['FEMALE']
		return ['MALE', 'FEMALE']

	product['gender'] = get_gender()

	##### CREATED ON #######	
	product['created_on'] = str(datetime.datetime.utcnow())

	##### SAVE TO FILE #######
	with open('testfile.json', 'a') as file:
		json.dump(product, file)
		file.write('\n')


#skin_care_hrefs = get_hrefs(make_soup(BASE_URL + SITE_MAP), 'skin-care') # create regex containing skin care + base url
#urls = get_product_urls(skin_care_hrefs)
#http://www.kiehls.co.uk/skin-care/category/serums/midnight-recovery-concentrate/819.html

urls = ['http://www.kiehls.co.uk/men-s/category/moisturisers-for-men/age-defender-moisturizer/KHL413.html']
		# , 
		# 'http://www.kiehls.co.uk/skin-care/category/facial-masks/cilantro-orange-extract-pollutant-defending-masque/KHL4528.html', 
		# 'http://www.kiehls.co.uk/skin-care/category/women-s-routines/wrinkle-fighting-routine/1103.html']


for url in urls:
	scrape_product(url)

logger.info('Total products scraped: %s', len(urls))

# TODO: 
#save image to S3 bucket
#parse size data into 2 parts
#collect price and currency data
#check for additional images
#check urls to create male/female category
#exclude collections
#need to get primary image


