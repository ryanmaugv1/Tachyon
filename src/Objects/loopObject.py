#
#  Tachyon
#  loopObject.py
#
#  Created on 19/09/17
#  Ryan Maugin <ryan.maugin@ada.ac.uk>
#

class LoopObject(object):

	def __init__(self, ast):
		# This will hold the dictionary version of the AST
		self.ast = ast['ForLoop']
		# This will hold the python exec string being formed
		self.exec_string = ""