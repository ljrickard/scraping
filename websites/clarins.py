import logging, datetime, requests, sys, html5lib
from bs4 import BeautifulSoup as bs
from http import HTTPStatus

BRAND = "Clarins"
BASE_URL = "http://int.clarins.com"
SITE_MAP = ""
SITE_MAP_KEYWORD = '' 

logger = logging.getLogger(__name__)

class Clarins():

	def __init__(self, product_template):
		self.product = product_template

	def execute(self):
		logger.info('Scraping a Clarins site')
		return True


	def _make_soup(self, url):
		return bs(requests.get(url).text,  "html5lib")

	def _scrape_product(self, url):

		################## scrape product #######################################

		logger.info('Scraping %s', url)

		return self.product

