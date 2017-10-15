#!/usr/bin/env python3
from sites.clarins import Clarins
from sites.kiehls import Kiehls
import logging
import logging.config

# handler = logging.handlers.RotatingFileHandler('sandbox3.log', mode='a', maxBytes=1000, backupCount=12) #3145728
#logging.basicConfig(level=logging.INFO, format='%(asctime)s: (%(processName)s: %(process)d) %(levelname)-2s - %(module)-2s(%(lineno)d): %(message)s')
# logging.config.fileConfig('logging.conf')


from logging.config import dictConfig

logging_config = dict(
    version=1,
    formatters={
        'f': {'format':
              '%(asctime)s: (%(processName)s: %(process)d) %(levelname)-2s - %(module)-2s(%(lineno)d): %(message)s'}
    },
    handlers={
        'h': {'class': 'logging.StreamHandler',
              'formatter': 'f',
              'level': logging.INFO
              },

        'logfile': {
            'level': logging.INFO,
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': "/logs/log.log",
            'maxBytes': 50000,
            'backupCount': 12,
            'mode': 'w'
        }
    },
    root={
        'handlers': ['h'],
        'level': logging.DEBUG,
    },
)

dictConfig(logging_config)

logger = logging.getLogger(__name__)

# Logger.findCaller()

#logger = logger.addHandler(handler)

# 'level':'DEBUG',
# 'class':'logging.handlers.RotatingFileHandler',
# 'filename': BASE_DIR + "/logs/logfile",
# 'maxBytes': 50000,
# 'backupCount': 2,
# 'formatter': 'standard',

#PRODUCT_TEMPLATE_FILE = 'product.json'
#site = Kiehls(PRODUCT_TEMPLATE_FILE)
#product_urls = site.get_product_urls()

from components.comms.aws_email import AwsEmail

#email_service = AwsEmail()
# email_service.send_email()

from components.comms.comms import Comms

details = {'sites': {'0': {
    'brand': 'kiehls',
    'total_products_found': 95,
    'total_new_products_found': 12,
    'product_urls': ['elastic.com/0', 'elastic.com/1', 'elastic.com/2']
},

    '1': {
    'brand': 'clarins',
    'total_products_found': 195,
    'total_new_products_found': 112,
    'product_urls': ['elastic.com/0', 'elastic.com/1', 'elastic.com/2']
},

    '2': {
    'brand': 'nivea',
    'total_products_found': 951,
    'total_new_products_found': 121,
    'product_urls': ['elastic.com/0', 'elastic.com/1', 'elastic.com/2']
}, }
}

details['report_summary'] = {}
details['report_summary']['total_run_time'] = 'some_run_time'
details['report_summary']['number_of_sites_scraped'] = 12

# print(details)

comms = Comms()
print(comms._generate_html(details))
comms.send(1, details)


#from components.data_access.data_access import DataAccess
#dataAccess = DataAccess(True)

# dataAccess._write_product_to_file(None)


# if __name__ == "__main__":
#   logging.basicConfig(level=logging.INFO, format='%(asctime)s: (%(processName)s: %(process)d) %(levelname)-2s - %(module)-2s(%(lineno)d): %(message)s')
#   es = ElasticSearch()
#   result = es.get_existing_product_urls('kiehls')
#   logger.info('Found %s products', len(result))
#   #logger.info('Found %s', result)
