#
#  Tachyon
#  bodyObject.py
#
#  Created on 10/08/17
#  Ryan Maugin <ryan.maugin@adacollege.org.uk>
#

class BodyObject():
    """ Body Object

    This class will take a body ast from a conditional or iterative statement
    and create an executable string from it while handling all nesting

    init:
        body_ast (dict) : This will hold the body dict with all asts
    """

    def __init__(self, bod_ast):
        # This will hold the body ast dictionaries
        self.bod_ast = bod_ast