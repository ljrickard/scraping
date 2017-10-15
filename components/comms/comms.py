#!/usr/bin/env python3
import json, logging, pprint
from components.comms.aws_email import AwsEmail
import dominate
from dominate.tags import *

HTML_DOC_TYPE = "<!DOCTYPE html PUBLIC '-//W3C//DTD XHTML 1.0 Transitional //EN' 'http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd'>"
template = 'components/comms/templates/scraping_report.json'
logger = logging.getLogger(__name__)

class Comms():

	def __init__(self):
		self.emailer = AwsEmail()

	def send_scrape_report(self, report):
		print(report)
		pass

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
		doc.doctype = HTML_DOC_TYPE

		with doc.head:
		    link(rel='stylesheet', href='style.css')
		    script(type='text/javascript', src='script.js')

		with doc:
			with div(id='summary'):
				h3('Report Summary')
				line1 = 'Total runtime: %s' % details['report_summary']['total_run_time']
				line2 = 'Total number of sites scraped: %s' % details['report_summary']['number_of_sites_scraped']
				h5('%s \n%s' % (line1, line2))
			with div(id='details'):
			    for key, value in details['sites'].items():
			        h4(value['url'])
			        line1 = 'total_products_found: %s' % value['total_products_found']
			        line2 = 'total_new_products_found: %s' % value['total_new_products_found']
			        p('%s \n%s' % (line1, line2))
			        for url in value['product_urls']:
			        	a(url, href=url) 
			        	br()
		return str(doc)



