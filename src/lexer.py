#
#  Tachyon
#  lexer.py
#
#  Created on 26/05/17
#  Ryan Maugin <ryan.maugin@adacollege.org.uk>
#
try:
    import re # for performing regex expressions
    from src.constants import *# for constants like tachyon keywords and datatypes

except ImportError:
    # Chances are, this was accessed by using `python main.py`
    from constants import *


class Lexer(object):

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

        # Check if matcher is in the same source_code item
        if source_code[current_index].count('"') == 2:

            # this will partition the string and return a tuple like this
            # ('word', 'matcher(")', ';')
            word = source_code[current_index].partition('"')[-1].partition('"'[0])

            # This will return the string and any extra characters such as end statement
            if word[2] != '': return [ '"' + word[0] + '"', '', word[2] ]

            # This will return just the string and empty fields that represent `undefined` or `nil`
            else:  return [ '"' + word[0] + '"', '', '' ]
        
        else:

            # Cut off the parts of the source code behind the matcher
            source_code = source_code[current_index:len(source_code)]

            # This will keep track of the string as it is being built up
            word = ""

            # This will keep count of the interations
            iter_count = 0

            # This will loop through the source code to find each part of the string and matcher
            for item in source_code:

                # Increment the iteration count every iteration
                iter_count += 1

                # Append the word that has been found to the string
                word += item + " "

                # If the word has the matcher in it and it is not the first matcher
                if matcher in item and iter_count != 1: 

                    # return the whole string, iteration count and extra characters like a statement end
                    return [
                        '"' + word.partition('"')[-1].partition('"'[0])[0] + '"', # The string
                        word.partition('"')[-1].partition('"'[0])[2],             # The extra character
                        iter_count - 1                                            # Number of iterations it took to get string
                    ]

                    # Break out the loop as the whole string was found
                    break
            


    def tokenize(self, source_code):
        """ Tokenize

        This method will tokenize the source code and return them the the parser in order
        to form the syntax tree

        Args:
            source_code (str) : This is the tachyon source code to be tokenized

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
            elif word in DATATYPE: tokens.append(["DATATYPE", word])

            # Identify all the indentifiers which are all in 'KEYWWORDS' const
            elif word in KEYWORDS: tokens.append(["IDENTIFIER", word])

            # Identify all custom identifers like variable names in source code
            elif re.match("[a-z]", word) or re.match("[A-Z]", word): 
                if word[len(word) - 1] != ';': tokens.append(["IDENTIFIER", word])
                else: tokens.append(["IDENTIFIER", word[0:len(word) - 1]])

            # Identify all arithmetic operations in source code
            elif word in "*-/+%=": tokens.append(["OPERATOR", word])

            # Identify all bianry operators
            elif word == "&&" or word == "||": tokens.append(["BINARY_OPERATOR", word])

            # Identify all comparison symbols in source code
            elif word in "==" or word in "!=" or word in ">" or word in "<" or word in "<=" or word in ">=": tokens.append(["COMPARISON_OPERATOR", word])

            # Identify all scope definers '{ }' in source code
            elif word in "{}": tokens.append(["SCOPE_DEFINER", word])

            # Identify all integer (number) values
            elif re.match("[0-9]", word): 
                
                # This will check if there is an end statement at the end of an integer and remove it if there is
                if word[len(word) - 1] == ';': tokens.append(["INTEGER", word[:-1]])
                else: tokens.append(["INTEGER", word])

            # Identify any strings which are surrounded in '' or ""
            elif ('"') in word: 

                # Call the getMatcher() method to get the full string
                matcherReturn = self.getMatcher('"', source_index, source_code)

                # If the string was in one source code item then we can just append it e.g '"Hello"'
                if matcherReturn[1] == '': tokens.append(["STRING", matcherReturn[0]])

                # If the string was spread out across multiple source code item e.g '"Hello', 'world"' 
                else:

                    # Append the string token
                    tokens.append(["STRING", matcherReturn[0] ])
                    
                    # Check for a semicolon at the end of thee string and if there is one then add end statament
                    if ';' in matcherReturn[1]: tokens.append(["STATEMENT_END", ";"])

                    # Skip all the already checked string items so there are no duplicates
                    source_index += matcherReturn[2]

                    # Skip every other check and loop again
                    pass

            # Checks for the end of a statement ';'
            if ";" in word[len(word) - 1]: 

                # Will hold the value of the last token which may have the end statemnt ';' still in it
                last_token = tokens[source_index - 1][1]

                # If there is an end statement still in that token then ...
                if last_token[len(last_token) - 1] == ';':
    
                    # ... We remove the end_statement ';' from the token ...
                    new = last_token[:len(last_token) - 1] + '' + last_token[len(last_token):]

                    # ... and then we simply add the new made token to the place of the old one which had the end_statement ';'
                    tokens[len(tokens) - 1][1] = new
                
                # Append the statement end token as a end stataemtn was found
                tokens.append(["STATEMENT_END", ";"])

            
            # Increment to the next word in tachyon source code
            source_index += 1
        return tokens