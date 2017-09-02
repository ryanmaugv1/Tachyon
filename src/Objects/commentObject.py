#
#  Tachyon
#  commentObject.py
#
#  Created on 02/09/17
#  Ryan Maugin <ryan.maugin@adacollege.org.uk>
#

class CommentObject():

	def __init__(self, ast):
		# This will hold the dictionary version of the AST
		self.ast = ast['Comment']
		# This will hold the python exec string being formed
		self.exec_string = ""


	def transpile(self):
		""" Transpile 
		
		This method will use the AST in order to create a python version of the tachyon
		generated dictionary AST.
		return:
			exec_string (str) : The python transpiled code
		"""

		# Generate python comment from comment AST
		self.exec_string += "# " + self.ast
		# Return the generated python exec string
		return self.exec_string