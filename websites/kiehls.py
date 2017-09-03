import logging, datetime, requests, sys, html5lib
from bs4 import BeautifulSoup as bs
from http import HTTPStatus

BRAND = "Kiehls"
BASE_URL = "http://www.kiehls.co.uk"
SITE_MAP = "/site-map.html"
SITE_MAP_KEYWORD = 'skin-care' # create regex containing skin care + base url

logger = logging.getLogger(__name__)

class Kiehls():

	def __init__(self, product_template):
		self.product = product_template

	def execute(self):
		# skin_care_hrefs = self._get_hrefs(BASE_URL+SITE_MAP, SITE_MAP_KEYWORD) 
		# products = []
		# for url in self._get_product_urls(skin_care_hrefs):
		# 	products.append(self._scrape_product('http://www.kiehls.co.uk/skin-care/category/facial-masks/cilantro-orange-extract-pollutant-defending-masque/KHL4528.html'))
		# return products

		return [self._scrape_product('http://www.kiehls.co.uk/skin-care/category/facial-masks/cilantro-orange-extract-pollutant-defending-masque/KHL4528.html')]

	def _get_hrefs(self, url, keyword):
		logger.info('Scraping hrefs from URL=%s', url)
		return [a.get('href') for a in self._make_soup(url).find_all('a') if keyword in a.get('href')]

	def _get_product_urls(self, skin_care_hrefs):
		products = set()
		for href in skin_care_hrefs:
			logger.info('Scraping product hrefs from URL=%s', href)
			for product_href in [a.get('href') for a in self._make_soup(href).find_all('a', class_='product_name')]:
				if BASE_URL in product_href:
					products.add(product_href)
				else:
					products.add(BASE_URL+product_href)

		return products

	def _make_soup(self, url):
		return bs(requests.get(url).text,  "html5lib")

	def _scrape_product(self, url):

		################## scrape product #######################################

		logger.info('Scraping %s', url)

		soup = self._make_soup(url)

		######## is valid product #######
		def is_not_valid_product():
			return soup.find_all('a', class_='shop-individually ')

		if is_not_valid_product():
			logger.warn('Not a valid product')
			return None

		######## brand ############
		self.product['brand'] = BRAND

		######## product name #######
		product_details = soup.find_all('div', class_='l-product_details-wrapper')[-1].extract()
		product_names = product_details.find_all('span', class_='product_name')

		for name in product_names:
		  	self.product['name'] = name.get_text()

		###### tagline ###########
		product_subtitle_raw = product_details.find_all('h2', class_='product_subtitle')

		for product_subtitle in product_subtitle_raw:
			self.product['tagline'] = product_subtitle.get_text()

		##### description #######
		def remove_hrefs(tag):
			return not tag.a and not tag.has_attr('href')

		product_details_description = product_details.\
											find_all('div', class_='product_detail_description')[-1].extract().\
											find_all(remove_hrefs)

		product_description = ''

		for copy in product_details_description:	
			copy = copy.get_text().strip().strip('\n').replace('\n', '.')

			while '  ' in copy:
				copy = copy.replace('  ', ' ')

			while '..' in copy:
				copy = copy.replace('..', '.')

			if copy not in product_description:
				product_description+=copy

		self.product['description'] = product_description

		##### metadata #######
		def has_class_but_no_id(tag):
		    return tag.has_attr('data-trackinginfo')

		# first part locates the tags and the second extracts that particular attribute data
		self.product['metadata'] = soup.find_all(has_class_but_no_id)[-1].extract().get('data-trackinginfo')

		##### ingredients #######
		ingredients_raw = soup.find_all('div', id='ing-copy')

		def extract_text(input, start):
			right_index = input.index('</', start)
			return input[input[:right_index].rfind('>')+1:right_index]

		def extract_ingredient(ingredient_raw):
			ingredient = extract_text(str(ingredient_raw), 0)
			ingredient_description = extract_text(str(ingredient_raw), str(ingredient_raw).index('</')+1)
			return {ingredient.replace('u00a0', ''):ingredient_description}

		self.product['ingredients'] = [extract_ingredient(ingredient_raw) for ingredient_raw in ingredients_raw]

		##### size #######
		def has_item_prop(tag):
		    return tag.has_attr('itemprop')

		def has_data_pricevalue_and_data_pricemoney(tag):
		    return tag.has_attr('data-pricevalue') and tag.has_attr('data-pricemoney')

		product_size = product_details.find_all(has_data_pricevalue_and_data_pricemoney)
		self.product['size'] = [item.get_text().strip().strip('\n').split() for item in product_size]

		##### images #######
		images = product_details.find_all('img', class_='primary_image product_image')
		source_images = [image.get('data-hires-img') for image in images] 
		self.product['source_images'] = source_images

		##### source #######
		self.product['source_url'] = [url]

		##### gender #######
		def get_gender():
			if 'men' in url:
				return ['MALE']
			if 'women' in url:
				return ['FEMALE']
			return ['MALE', 'FEMALE']

		self.product['gender'] = get_gender()

		##### tags #######	
		def get_tags(url):
			return [tag for tag in ['masque', 'moisturizer', 'facial', 'masks', 'herbal', 'hydrating', 'spf'] if tag in url.lower()]

		self.product['tags'] = get_tags(url)

		##### created_on #######	
		self.product['created_on'] = str(datetime.datetime.utcnow())

		return self.product

