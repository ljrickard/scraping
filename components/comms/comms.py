#!/usr/bin/env python3
import json, logging, pprint
from components.comms.aws_email import AwsEmail
import dominate
from dominate.tags import *

template = 'components/comms/templates/scraping_report.json'
logger = logging.getLogger(__name__)

class Comms():

	def __init__(self):
		self.emailer = AwsEmail()

	def send(self, template_id, details):
		self.data=self._generate_email(template_id, details)
		self.emailer.send_email(self.data)

	def _generate_email(self, template_id, details):
		if template_id == 1:
			email = self._load_template(template_id)
			email['body'] = self._generate_html(details)
			return email
		else:
			logger.error("Template id=%s not found. Email not sent", template_id)

	def _load_template(self, template_id):
		return json.loads(open(template).read())

	def _generate_html(self, details):
		doc = dominate.document(title='Report')
		doc.doctype = "<!DOCTYPE html PUBLIC '-//W3C//DTD XHTML 1.0 Transitional //EN' 'http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd'>"

		with doc.head:
		    link(rel='stylesheet', href='style.css')
		    script(type='text/javascript', src='script.js')

		with doc:
			with div(id='header').add(ul()):
			    for key, value in details.items():
			        h4(value['brand'])
			        p('total_products_found: %s' % value['total_products_found'])
			        p('total_new_products_found: %s' % value['total_new_products_found'])
			        for url in value['product_urls']:
			        	li(
			        		a('new', href=url[0]),
			        		a('source', href=url[1])
			        		)
		return str(doc)