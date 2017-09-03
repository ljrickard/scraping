from websites.clarins import Clarins
from websites.kiehls import Kiehls

class Website(object):
    def factory(product_template, type):
	    if type == "clarins": 
	        return Clarins(product_template)
	    if type == "kiehls": 
	        return Kiehls(product_template)
	    return None
