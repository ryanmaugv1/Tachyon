# Lexical Analyzer

> May rewrite lexical analyser to loop through each character instead of split words from source code

# Patterns
| Type          | Token                  | Reference                       |
|---------------|------------------------|---------------------------------|
| identifier    | [IDENTIFIER if]        | [Identifiers](#Identifiers)     |
| string        | [STRING "Ryan Maugin"] | [Strings](#strings)             |
| datatype      | [DATATYPE str]         | [Data Types](#Data-Types)       |
| operator      | [OPERATOR +]           | [Operators](#Operators)         |
| integer       | [INTEGER 12]           | [Integers](#Integers)           |
| statement_end | [STATEMENT_END ;]      | [End Statement](#end-statements)|
| comparison_operator | [COMPARISON_OPERATOR ==] | [Comparison Operators](#comparison-operators) |
| scope_definer | [SCOPE_DEFINER {]      | [Scope Definer](#scope-definer) |


# Data Types

Currently the data types for tachyon language are minimal and simple so that it is easy to begin with but more will be added as time goes on, in the meanwhile these are the ones I have:

    DATATYPE = ["bool", "int", "str"]

The way that I create tokens for data types is very easy because they will usually be in their own item as they won't be attached to any other character when calling split function on the source code string in python. This means I can create a data type token like this:

    # Identify all of the Data Types
    elif word in self.DATATYPE: tokens.append("[DATATYPE " + word + "]")
    

# Identifiers

There are not many keywords (identifiers) for the tachyon language at the moment for the same reasons there are not a lot of data types is in order to keep it minimal and the keywords the language has as of now are:

    KEYWORDS = ["function", "class", "if", "true", "false", "nil", "print"]
    
The way that I create tokens for data types is very easy because they will usually be in their own item as they won't be attached to any other character when calling split function on the source code string in python. This means I can create a data type token like this:

     # Identify all the indentifiers which are all in 'KEYWWORDS' const
     elif word in self.KEYWORDS: tokens.append("[IDENTIFIER " + word + "]")
     
     
# Operators

These are analysed the same way in which the keywords and data types are analysed (for reference these are documented above). But this is the way I token analyse them:

    # Identify all aithmetic operations in source code
    elif word in "*-/+%": tokens.append("[OPERATOR " + word + "]")
    
The only operators tachyon has for the moment is:

- `*` multiplication
- `-` subtractions
- `/` division
- `+` addition
- `%` modulus
- `=` equals to


# Comparison Operators

The same way in whic i search for normal operators I used to search for comparison operators. The way I did this was:

    # Identify all comparison symbols in source code
    elif word in "==" or word in "!=" or word in ">" or word in "<": tokens.append("[COMPARISON_OPERATOR " + word + "]")

The reason I had to do different `or` checks is because I was looking for a specific pair of operators together and not one like this `+/-*%` where any of the ones in there could be found and that would be an operator token.

I kept the comparison operators to the minimal and cucial ones but I am planning on adding the rest later on. In the meanwhle these are the comparison editors I have added token analysis for:

- `==` equals to
- `!=` not equal to
- `>` greater than
- `<` less than

# Integers

When analysing integers I had to make use of two sperate regular expressions in order to retrieve integer items that look like this `255` and this `255;` and turn them into integers.

In the first case if the item I get has this integer inside it `255` then it will be tokenized by this condition:

    # Identify all integer (number) values
    elif re.match(".[0-9]", word): tokens.append("[INTEGER " + word + "]")
    
But if I was to to get an integer item like `255;`, it will be tokenized by this function:

    # Identify all integer (number) values
    elif re.match(".[0-9$;]", word): tokens.append("[INTEGER " + word[:-1] + "]")

The difference is that the consition which tokenizes the integer item which looks like this `255;` will remove the end statement (semi colon).


# Scope Definer

The scope definer will handle the scope of code for example if statement:

    if condition { scope }

The definers of that scope will be the opening `{` and closing `}` and anyhting between that will be a scope, the way I defined this token was like this:

    # Identify all scope definers '{ }' in source code
    elif word in "{}": tokens.append("[SCOPE_DEFINER " + word + "]")


# Strings

### Implementation of string token analysis

The following code snippet simple calls the getMatcher function to get the string and returns it but what this snippet does extra is check the return to see how to behave.

      # Identify any strings which are surrounded in  ""
      elif ('"') in word: 

          # Call the getMatcher() method to get the full string
          matcherReturn = self.getMatcher('"', source_index, source_code)

          # If the string was in one source code item then we can just append it
          if matcherReturn[1] == '': tokens.append("[STRING " + matcherReturn[0] + "]")

          # If the string was spread out across multiple source code item
          else:

              # Append the string token
              tokens.append("[STRING " + matcherReturn[0] + "]")
                    
              # Check for a semicolon at the end of thee string and if there is one then add end statament
              if ';' in matcherReturn[1]: tokens.append("[STATEMENT_END ;]")

              # Skip all the already checked string items so there are no duplicates
              source_index += matcherReturn[2]

              # Skip every other check and loop again
              pass


Strings however are a bit more difficult to parse as in some cases you will need to look through multiple source code items to find a whole string, for example:

`['"Ryan'], ['is'], ['coding'], ['something"']`
`--^---------------------------------------^--`

This shows where the string begins and then ends and illustrates that the closing quote will not be in the same item so a simple regular expression wouldn't be able to find the string. Therefore, I created a new function `getMatcher()` which is shown below.

----
> ### GetMatcher(matcher, current_index, source_code)
What this function will do is loop from current source code index where the first quote was found and iterate through the rest of the source code until it finds the closing quote.

**`Arguments`** the arguments are:
- `matcher` this is the quote we found or in other cases a `(` or `{`.
- `current_index` is the index at which we found the character we need to find a matcher for.
- `source_code` is the source code we are looping through to find matcher.

**`return`** this will return:
- The full string
- Number of indexes at which second matcher was found at. This is used to skip all the checked indexes and not have to rechecks them.
- The symbol at the end of string

**`Source code`**:

    def getMatcher(self, matcher, current_index, source_code):

        # Check if matcher is in the same source_code item
        if source_code[current_index].count('"') == 2:

            # this will partition the string and return a tuple like this
            # ('word', '"', ';')
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
                        word.partition('"')[-1].partition('"'[0])[2], # The extra character
                        iter_count - 1
                    ]

                    # Break out the loop as the whole string was found
                    break
                  
**`Things to fix`**:
This is not perfect and still has improvements that need to be done and some bugs are:

- In order to work quote has to be at the beggining of the item like this `"Ryan` and not like this `("Ryan` or else it won't work.

- There can only be one character at the end of the matching quote item or else it will output invalid tokens for example:

  - `buzz"` would also be valid
  - `fizz";` would be a valid
  - `fizzbuzz";)` would be invalid

# END STATEMENTS

The way I analyse end statements is quite simple and the way I do this is by simply checking every already checked token for a ';' semicolon at the last index of a source code item to see if there was an end statement there. I do this like this:

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
    
However, I have to check the last item for an end statement too because if the last token was not a string token the end statement symbol (;) would have been added to it. Therefore, what I do is remove it and then update the last token.

# **Bugs to fix**

- Entering a number like '1', '9' or '3' cause a mess up in the lexer but naything longer than one decimal such as '10' or '287' is fine.
