#!/usr/bin/env python3
import logging
import datetime
import copy
import time
from sites.lib.utils import make_soup, format_url
from components.data_access.data_access import DataAccess
from sites.website import Website

BRAND = "kiehls"
BASE_URL = "http://www.kiehls.co.uk"
SITE_MAP = "/site-map.html"
SITE_MAP_KEYWORD = 'skin-care'  # create regex containing skin care + base url

logger = logging.getLogger(__name__)


class Kiehls(Website):

    def __init__(self, dry_run):
        super(Kiehls, self).__init__(dry_run)
        self.base_url = BASE_URL
        self.brand = BRAND

    def execute(self):
        return super(Kiehls, self).execute()

    def get_product_urls(self):
        # get hrefs that contain base url , site and keyword - for example: https://www.kiehls.co.uk/skin-care/category/best-sellers-skincare
        hrefs = self._get_hrefs(BASE_URL + SITE_MAP, SITE_MAP_KEYWORD)
        return [product_url for product_url in self._get_product_urls(hrefs) if self._is_valid_product_url(product_url)]

    def scrape_product_urls(self, product_urls):
        products = []
        for url in product_urls:
            products.append(copy.deepcopy(self._scrape_product(url)))
        return products

    ################## scrape homepage #######################################

    def _get_hrefs(self, url, keyword):
        return {a.get('href') for a in make_soup(url).find_all('a') if keyword in a.get('href')}

    def _get_product_urls(self, skin_care_hrefs):
        product_urls = set()
        for href in skin_care_hrefs:
            for product_href in [a.get('href') for a in make_soup(href).find_all('a', class_='product_name')]:
                product_urls.add(format_url(product_href, BASE_URL))

        return product_urls

    def _is_valid_product_url(self, url):
        return not make_soup(url).find_all('a', class_='shop-individually ')

    ################## scrape product #######################################

    def _scrape_product(self, url):
        product = self.product_template
        soup = make_soup(url)

        ######## brand ############
        product['brand'] = BRAND

        ######## product name #######
        product_details = soup.find_all(
            'div', class_='l-product_details-wrapper')[-1].extract()
        product_names = product_details.find_all('span', class_='product_name')

        for name in product_names:
            product['name'] = name.get_text()

        ###### tagline ###########
        product_subtitle_raw = product_details.find_all(
            'h2', class_='product_subtitle')

        for product_subtitle in product_subtitle_raw:
            product['tagline'] = product_subtitle.get_text()

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
                product_description += copy

        product['description'] = product_description

        ##### metadata #######
        def has_class_but_no_id(tag):
            return tag.has_attr('data-trackinginfo')

        # first part locates the tags and the second extracts that particular attribute data
        product['metadata'] = soup.find_all(
            has_class_but_no_id)[-1].extract().get('data-trackinginfo')

        ##### ingredients #######
        ingredients_raw = soup.find_all('div', id='ing-copy')

        def extract_text(input, start):
            right_index = input.index('</', start)
            return input[input[:right_index].rfind('>') + 1:right_index]

        def extract_ingredient(ingredient_raw):
            ingredient = extract_text(str(ingredient_raw), 0)
            ingredient_description = extract_text(
                str(ingredient_raw), str(ingredient_raw).index('</') + 1)
            return {ingredient.replace('u00a0', ''): ingredient_description}

        product['ingredients'] = [extract_ingredient(
            ingredient_raw) for ingredient_raw in ingredients_raw]

        ##### size #######
        def has_item_prop(tag):
            return tag.has_attr('itemprop')

        def has_data_pricevalue_and_data_pricemoney(tag):
            return tag.has_attr('data-pricevalue') and tag.has_attr('data-pricemoney')

        product_size = product_details.find_all(
            has_data_pricevalue_and_data_pricemoney)
        product['size'] = [item.get_text().strip().strip('\n').split()
                           for item in product_size]

        ##### images #######
        images = product_details.find_all(
            'img', class_='primary_image product_image')
        source_images = [image.get('data-hires-img') for image in images]
        product['source_images'] = source_images

        ##### source #######
        product['source_url'] = url

        ##### gender #######
        def get_gender():
            if 'men' in url:
                return ['MALE']
            if 'women' in url:
                return ['FEMALE']
            return ['UNISEX']

        product['gender'] = get_gender()

        ##### tags #######
        def get_tags(url):
            return [tag for tag in ['masque', 'moisturizer', 'facial', 'masks', 'herbal', 'hydrating', 'spf'] if tag in url.lower()]

        product['tags'] = get_tags(url)

        ##### created_on #######
        product['created_on'] = str(datetime.datetime.utcnow())

        return product
