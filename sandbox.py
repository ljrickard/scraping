#!/usr/bin/env python3
from websites.clarins import Clarins
from websites.kiehls import Kiehls
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s: (%(processName)s: %(process)d) %(levelname)-2s - %(module)-2s(%(lineno)d): %(message)s') 
logger = logging.getLogger(__name__)
#PRODUCT_TEMPLATE_FILE = 'product.json'
#site = Kiehls(PRODUCT_TEMPLATE_FILE)
#product_urls = site.get_product_urls()

from aws_email import AwsEmail

email_service = AwsEmail()

email_service.send_email()

