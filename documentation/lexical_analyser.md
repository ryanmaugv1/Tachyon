# Lexical Analyzer

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

Currently the data types for tachus language are minimal and simple so that it is easy to begin with but more will be added as time goes on, in the meanwhile these are the ones I have:

    DATATYPE = ["bool", "int", "str"]

The way that I create tokens for data types is very easy because they will usually be in their own item as they won't be attached to any other character when calling split function on the source code string in python. This means I can create a data type token like this:

    # Identify all of the Data Types
    elif word in self.DATATYPE: tokens.append("[DATATYPE " + word + "]")
    

# Identifiers

There are not many keywords (identifiers) for the tachus language at the moment for the same reasons there are not a lot of data types is in order to keep it minimal and the keywords the language has as of now are:

    KEYWORDS = ["function", "class", "if", "true", "false", "nil", "print"]
    
The way that I create tokens for data types is very easy because they will usually be in their own item as they won't be attached to any other character when calling split function on the source code string in python. This means I can create a data type token like this:

     # Identify all the indentifiers which are all in 'KEYWWORDS' const
     elif word in self.KEYWORDS: tokens.append("[IDENTIFIER " + word + "]")
     
     
# Operators

These are analysed the same way in which the keywords and data types are analysed (for reference these are documented above). But this is the way I token analyse them:

    # Identify all aithmetic operations in source code
    elif word in "*-/+%": tokens.append("[OPERATOR " + word + "]")
    
The only operators tachus has for the moment is:

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

In this code snippet I look for a double quote inside each source code item to identify the start of a string. What I then do is check if there are two quotes in the source code item I am look through like this:

    if word.count('"') == 2:

This means that the opening and closing quotes to the string is within the same source code item which means we don't have to run `getMatcher()` function to find the closing quote.

However, If we don't find the quote then what we have to do is call the `getMatcher()` function to loop through and find the closing quote for us and return the full string and the number of index's from from current index whre the quote was found.

From the `getMatcher()` function sometimes it will return a string with an `END_STATEMENT` (semicolon) at the end which we need to remove and to do so when we create the token we add:

    getString[0:len(getString) - 1]

This will remove the `;` from the string which would usually look something like this `"Ryan Maugin";` rather than `"Ryan Maugin"`.

      # Identify any strings which are surrounded in '' or ""
      elif ('"') in word: 

          # If there are two quotes this means there is no need to search for closing matcher (quote "")
          if word.count('"') == 2: tokens.append("[STRING " + word[0:len(word) - 1] + "]")
                
          # If there is only one quote then we need to search for next one to close and form the string
          else:

              # Call the method and get the return response data
              getMatcherMethod = self.getMatcher('"', source_index, source_code)  # Calls function
              getString = getMatcherMethod[0]                                     # Gets the full string return
              getIndexToSkip = getMatcherMethod[1]                                # Gets the index apart (index to skip)

              # Check for STATEMENT_END at end of string
              if getString[len(getString) - 1] == ";":
              
                  # Append string without STATEMENT_END and add the STATEMENT_END seperately as another token
                  tokens.append("[STRING " + getString[0:len(getString) - 1] + "]") 
                  tokens.append("[STATEMENT_END ;]")                                
                  
              else:
                  
                  # Simply append string token if there is no STATEMENT_END
                  tokens.append("[STRING " + getString + "]")

              # Skip a certain amount of indexes that have already been analysed to get string
              source_index += getIndexToSkip
                    
              # Start loop again rather than run other checks and increments
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
- Number of indexes at which second matcher was found at. This is used to skip all the checked indexes and not have to rechecks them. `Minus 1 from the index_tracker when returning it or else it skips the next source code item`

**`Source code`**:

        def getMatcher(self, matcher, current_index, source_code):

          # This will track how much iterations it took to find the matcher
          iterator_tracker = 0

          # Will loop through source code from current index forward to find the matcher
          for item in range(current_index, len(source_code)):

              # Add 1 to iterator tracker everytime it loops through source code item and doesn't find matcher
              iterator_tracker += 1

              # This checks if the matcher is in the item being looped
              if source_code[item].find(matcher):

                  # If the matcher was found then return the string and amount of indexes it was away from first matcher
                  return [ " ".join(source_code[current_index:current_index + iterator_tracker]), iterator_tracker - 1]
                  
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
    if ";" in word[len(word) - 1]: tokens.append("[STATEMENT_END ;]")
    
The reason I make it only to check the last index is in order to prevent any errors where it will create an end statement if there was a semicolon inside an item and not at the end.