from sites.clarins import Clarins
from sites.kiehls import Kiehls

class Site(object):
    def factory(product_template, type):
	    if type == "clarins": 
	        return Clarins(product_template)
	    if type == "kiehls": 
	        return Kiehls(product_template)
	    return None
