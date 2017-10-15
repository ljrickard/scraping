from sites.clarins import Clarins
from sites.kiehls import Kiehls

class Brands(object):

	def __init__(self, dry_run):
		self.dry_run = dry_run

	def factory(self, brand):

		if brand == "clarins": return Clarins(self.dry_run)
		if brand == "kiehls": return Kiehls(self.dry_run)

		raise ValueError('{} not found'.format(brand))