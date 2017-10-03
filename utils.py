#!/usr/bin/env python3
import requests, html5lib, logging
from bs4 import BeautifulSoup as bs

HTTPS = 'https'
HTTP = 'http'

logger = logging.getLogger(__name__)	

def make_soup(url):
	logger.info('Making soup from URL=%s', url)
	return bs(requests.get(url).text,  "html5lib")

def format_url(url, BASE_URL):
	logger.info('Formatting URL=%s', url)
	if _secure_url:
		url = _remove_security_from_url(url)
	if BASE_URL in url:
		return url
	else:
		return BASE_URL+url

def _secure_url(url):
	return HTTPS in url

def _remove_security_from_url(url):
	return url.replace(HTTPS, HTTP)