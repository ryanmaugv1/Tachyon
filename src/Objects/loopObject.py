#
#  Tachyon
#  loopObject.py
#
#  Created on 19/09/17
#  Ryan Maugin <ryan.maugin@ada.ac.uk>
#

from Objects.bodyObject import BodyObject

class LoopObject(object):

	def __init__(self, ast, nesting_count):
		# This will hold the dictionary version of the AST
		self.ast = ast['ForLoop']
		# This will hold the python exec string being formed
		self.exec_string = ""
		# This will keep track of the nestings of for loops
		self.nesting_count = nesting_count
		self.bodyObject = BodyObject(self.ast, 'ForLoop', nesting_count)


	def transpile(self):
		""" Transpile 
		
		This method will use the AST in order to create a python version of the tachyon
		generated dictionary AST.

		return:
			exec_string (str) : The python transpiled code
		"""

		# Variables that will store the AST value
		initValName = ""
		initVal     = ""
		comparison  = ""
		incrementer = ""
		endVal      = ""
		body        = []

		# Loop through the ast items and store them in the variables
		for val in self.ast:

			# Get the initialValueName
			try: initValName = val['initialValueName']
			except: pass

			# Get the initialValue
			try: initVal = val['initialValue']
			except: pass

			# Get the comparsion
			try: comparison = val['comparison']
			except: pass

			# Get the endValue
			try: endVal = val['endValue']
			except: pass

			# Get the incrementer
			try: incrementer = val['incrementer']
			except: pass

			# Get the body
			try: body = val['body']
			except: pass

		# This will check if incrementer has + at the first index and remove it if it does as it will cause python syntax error
		if incrementer[0] == "+": incrementer = incrementer[1:len(incrementer)]

		# Append the python for loop statement to the exect string seperate from the body
		self.exec_string += "for " + initValName + " in range(" + str(initVal) + ", " + str(endVal) + ", " + incrementer + "):\n"

		#TODO Add body to exec string with correct indentation

		return self.exec_string









