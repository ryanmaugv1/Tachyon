# Lexical Analyzer

> Lexical Analysis is done word by word which can be quite incovnvenient sometimes when you have things like this `identifier;` instead of `identifier` because the `;` (semicolon) comes with the word too instead of being seperated as they are both different tokens.

# Patterns
| Type          | Token                       | Reference                       |
|---------------|-----------------------------|---------------------------------|
| identifier    | ["IDENTIFIER", "if"]        | [Identifiers](#Identifiers)     |
| string        | ["STRING". '"Ryan Maugin"'] | [Strings](#strings)             |
| datatype      | ["DATATYPE", "str"]         | [Data Types](#Data-Types)       |
| operator      | ["OPERATOR", "+"]           | [Operators](#Operators)         |
| integer       | ["INTEGER", "12"]           | [Integers](#Integers)           |
| statement_end | ["STATEMENT_END", ";"]      | [End Statement](#end-statements)|
| comparison_operator | ["COMPARISON_OPERATOR", "=="] | [Comparison Operators](#comparison-operators) |
| scope_definer | ["SCOPE_DEFINER", "{"]      | [Scope Definer](#scope-definer) |

---

# Data Types

Currently the data types for tachyon are minimal and simple so that it is easy to begin with but more will be added as time goes on, in the meanwhile these are the ones I have:

    DATATYPE = ["bool", "int", "str"]                                    <-- Current
    DATATYPE = ["bool". "int", "str", "float", "double", "arr", "dict"]  <-- Goal

The way that I create tokens for data types is very easy because they will usually be in their own word item when the source code is split in python using `string.split()` therefore whenever we come across a DATATYPE word in an item we create a token for it which is as such (for example cases the type is `str`):

    ['DATATYPE', 'str']
    
The way we identify this token is by simply looking through our `DATATYPE` array in `constants.py` which is why we import the file in the lexer. If the source code item matches any of the data types then we add it as a data type token. Here is the code on how it's done:

    elif word in constants.DATATYPE: 
        tokens.append(["DATATYPE", word])

---

# Identifiers

There are not many keywords (identifiers) for tachyon at the moment for the same reasons there are not a lot of data types is in order to keep it minimal and the keywords the language has, as of now are:

    KEYWORDS = ["function", "class", "if", "True", "False", "nil", "print"]
    
The way I get tokens for identifiers are identical to the way I get the data type tokens from the `constants.py` file but instead I search through a `KEYWORD` array instead then create the following token:

     ['IDENTIFIER', 'if']

The code for this as you will see is the same as checking for data types but the variable being looked through is different:

    elif word in constants.DATATYPE: 
        tokens.append(["DATATYPE", word])
    
---
     
# Operators

When checking for operator tokens I could have gone for a similar technique as getting [data types](#Data-Types) and [identifiers](#Data-Types). However, I didn't use that technique as I was trying to consume as less memory as possible so what I did instead of creating an array of operators I just created a string inside the if statement like this `*-/+%` to check if words was one of them and if so I created an operator token like such:

    ["OPERATOR", "+"]
    
The operators tachyon currently support:

- `*` multiplication
- `-` subtractions
- `/` division
- `+` addition
- `%` modulus

Code for how I find and generate operator tokens:

    elif word in "*-/+%=": 
        tokens.append(["OPERATOR", word])

---
# Comparison & Binary Operators

The way in which I search for operators is similar to the way which the comparison & bianry operators are looked for. The tokens this produced looked like this:

    ["COMPARISON_OPERATOR", "!="]
    ["BINARY_OPERATOR",     "&&"]

Supported comparison & binary operators in tachyon:

| Comparison Operator    | Binary Operator      |
|------------------------|----------------------|
| ==                     | &&                   |
| !=                     | '||'                 |
| >                      |                      |
| <                      |                      |
| <=                     |                      |
| >=                     |                      | 


The code for this as I said is simlar to the way I get operators however I couldn't implement it the exact same way because I wasn't performing comparison checks on single characters but character pairs too:


**Comparison Operators**

    elif word in "==" or word in "!=" or word in ">" or word in "<" or word in "<=" or word in ">=": 
        tokens.append(["COMPARISON_OPERATOR", word])
    
**Binary Operators**

    elif word == "&&" or word == "||": 
        tokens.append(["BINARY_OPERATOR", word])

---
# Integers

When analysing integers I made use of a regex expression which allowed for me to easily find tokens with only integers in them however this would pickup two types of integer `21` & `21;` which is why in the code when apending the token I had to disregard when adding the token and this is how it was done:

    elif re.match("[0-9]", word):
        if word[len(word) - 1] == ';': 
            tokens.append(["INTEGER", word[:-1]])
        else: 
            tokens.append(["INTEGER", word])
            
The important thing to note her is that I don't completely take the `;` off the word so when the word (int) continues through the loop as `21;` and not `21`. This is because later on in the loop a check will look through all words for a `;` in the last character of the word so it can add a `STATEMENT_END` token for it. The token sequence generated from a integer like `21;` is:

    ["INTEGER", "21"], ["STATEMENT_END", ";"]

and for a normal integer is simply: `["INTEGER", "21"]`

---
# Scope Definer

The scope definers are the opening `{` and closing `}` braces which in tachyon are for defining scopes for a function, conditional statement and more. The tokens for scope definers look like this:

    ["SCOPE_DEFINER", "{"]

The code for this is super simple as all I do is look through a string `{}` and see if the word being checked is the same as one of the characters in the string.

    elif word in "{}": tokens.append("[SCOPE_DEFINER " + word + "]")
---

# Strings

### Implementation of string token analysis

The following code snippet is a call to the getMatcher method to get the string and return it but what this snippet does extra is check the return to see how to behave.

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
    
However, I have to check the last item for an end statement too because if the last token was not a string token the end statement symbol (;) would have been added to it because strings skip other checks when formed. Therefore, what I do is remove it and then update the last token.


