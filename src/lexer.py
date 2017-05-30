#
#  Tachus
#  lexer.py
#
#  Created on 26/05/17
#  Ryan Maugin <ryan.maugin@adacollege.org.uk>
#

import re # for performing regex expressions

class Lexer(object):

    # Reserved keywords for programming language
    KEYWORDS = ["function", "class", "if", "true", "false", "nil", "print"]
    DATATYPE = ["bool", "int", "str"]


    def getMatcher(self, matcher, current_index, source_code):
        """ Get Matcher
        
        This method will find a matcher like an ending quote in other indexes of the
        source code and form the string.

        Args:
            matcher (str)       : The matcher we are looking for
            current_index (int) : The index we began the search for the matcher from
            source_code (list)  : This is the source_code we will iterate through

        Returns:
            List:
                Contents between 1st matcher to 2nd matcher e.g "Ryan Maugin"
                index count from current_index to the index where 2nd matcher was found e.g 10
        """

        # This will track how much iterations it took to find the matcher
        iterator_tracker = 0

        # Will loop through source code from current index forward to find the matcher
        for item in range(current_index, len(source_code)):

            # Add 1 to iterator tracker everytime it loops through source code item and doesn't find matcher
            iterator_tracker += 1

            # This checks if the matcher is in the item being looped
            if source_code[item].find(matcher):

                # If the matcher was found then return the string and amount of indexes it was away from first matcher
                return [ " ".join(source_code[current_index:current_index + iterator_tracker]), iterator_tracker]
            


    def tokenize(self, source_code):
        """ Tokenize

        This method will tokenize the source code and return them the the parser in order
        to form the syntax tree

        Args:
            source_code (str) : This is the tachus source code to be tokenized

        Returns:
            tokens (list) : It will return a lost of all the tokens
        """

        # This will hold a record of all the tokens
        tokens = []

        # Cleanup code by removing extra line breaks
        source_code = source_code.split()

        # Current character position we are parsing
        source_index = 0

        # Will loop through each word in 
        while source_index < len(source_code):
            
            # This will be the word that is retrieved from source code
            word = source_code[source_index]

            # Check for new lines and ignore them
            if word in "\n": pass

            # Identify all of the Data Types
            elif word in self.DATATYPE: tokens.append("[DATATYPE " + word + "]")

            # Identify all the indentifiers which are all in 'KEYWWORDS' const
            elif word in self.KEYWORDS: tokens.append("[IDENTIFIER " + word + "]")

            # Identify all aithmetic operations in source code
            elif word in "*-/+%=": tokens.append("[OPERATOR " + word + "]")

            # Identify all comparison symbols in source code
            elif word in "==" or word in "!=" or word in ">" or word in "<": tokens.append("[COMPARISON_OPERATOR " + word + "]")

            # Identify all integer (number) values
            elif re.match(".[0-9]", word): tokens.append("[INTEGER " + word + "]")

            # Identifiy integer with a ';' at the end which terminates a statement and creates a token for the statement ender and number
            elif re.match(".[0-9$;]", word): tokens.append("[INTEGER " + word[:-1] + "]") 

            # Identify any strings which are surrounded in '' or ""
            elif ('"') in word: 

                # If there are two quotes this means the is no need to search for closing partner
                if word.count('"') == 2: tokens.append("[STRING " + word[0:len(word) - 1] + "]")
                
                # If there is only one quote then we need to search for next one to close string
                else:

                    # Call the method and get the return response data
                    getMatcherMethod = self.getMatcher('"', source_index, source_code)
                    getString = getMatcherMethod[0]
                    getIndexToSkip = getMatcherMethod[1]

                    # Check for STATEMENT_END
                    if getString[len(getString) - 1] == ";":
                        tokens.append("[STRING " + getString[0:len(getString) - 1] + "]") # Append string token without statement_end
                        tokens.append("[STATEMENT_END ;]")                                # Add statement end seperatrly
                    else: tokens.append("[STRING " + getString + "]")                     # Simply append string token

                    # Skip a certain amount of indexes that have been already sorted for getting string
                    source_index += getIndexToSkip
                    
                    # Start loop again rather than run other checks and increments
                    pass
            
            # Checks for the end of a statement ';'
            if ";" in word[len(word) - 1]: tokens.append("[STATEMENT_END ;]")
            
            # Increment to the next word in tachus source code
            source_index += 1

        print(tokens) # TODO Change this to return statement