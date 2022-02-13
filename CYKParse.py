# Yunfan Geng
# Uyen Dinh 
# CS295P - Winter 2022

import Tree

verbose = False
def printV(*args):
    if verbose:
        print(*args)

# A Python implementation of the CYK-Parse algorithm
def CYKParse(words, grammar):
    T = {}
    P = {}
    # Instead of explicitly initializing all P[X, i, k] to 0, store
    # only non-0 keys, and use this helper function to return 0 as needed.
    def getP(X, i, k):
        key = str(X) + '/' + str(i) + '/' + str(k)
        if key in P:
            return P[key]
        else:
            return 0
    # Insert lexical categories for each word
    for i in range(len(words)):
        if getGrammarUnexpected(grammar, words[i]):
            P['Unexpected' + '/' + str(i) + '/' + str(i)] = 1.0
            T['Unexpected' + '/' + str(i) + '/' + str(i)] = Tree.Tree('Unexpected', None, None, lexiconItem=words[i])
            P['NP' + '/' + str(i) + '/' + str(i)] = 1.0
            T['NP' + '/' + str(i) + '/' + str(i)] = Tree.Tree('NP', T['Unexpected' + '/' + str(i) + '/' + str(i)], None)
        else:
            for X, p in getGrammarLexicalRules(grammar, words[i]):
                P[X + '/' + str(i) + '/' + str(i)] = p
                T[X + '/' + str(i) + '/' + str(i)] = Tree.Tree(X, None, None, lexiconItem=words[i])
                 # Chomsky Form:  X1 -> Y [pX1Y], chomskyForm index is 1
                for X1, Y, PX1Y in getGrammarSyntaxRules(grammar, 1):
                    if (Y == X):
                        P[X1 + '/' + str(i) + '/' + str(i)] = PX1Y * p
                        # Tree(category name is X1, left child is T[X + '/' + str(i) + '/' + str(i)], right child is None, lexiconItem default is None)
                        T[X1 + '/' + str(i) + '/' + str(i)] = Tree.Tree(X1, T[X + '/' + str(i) + '/' + str(i)], None)

    printV('P:', P)
    printV('T:', [str(t)+':'+str(T[t]) for t in T])
    # Construct X_i:j from Y_i:j + Z_j+i:k, shortest spans first
    for i, j, k in subspans(len(words)):
        for X, Y, Z, p in getGrammarSyntaxRules(grammar, 0):
            printV('i:', i, 'j:', j, 'k:', k, '', X, '->', Y, Z, '['+str(p)+']', 
                    'PYZ =' ,getP(Y, i, j), getP(Z, j+1, k), p, '=', getP(Y, i, j) * getP(Z, j+1, k) * p)
            PYZ = getP(Y, i, j) * getP(Z, j+1, k) * p
            if PYZ > getP(X, i, k):
                printV('     inserting from', i, '-', k, ' ', X, '->', T[Y+'/'+str(i)+'/'+str(j)], T[Z+'/'+str(j+1)+'/'+str(k)],
                            'because', PYZ, '=', getP(Y, i, j), '*', getP(Z, j+1, k), '*', p, '>', getP(X, i, k), '=',
                            'getP(' + X + ',' + str(i) + ',' + str(k) + ')')
                P[X + '/' + str(i) + '/' + str(k)] = PYZ
                T[X + '/' + str(i) + '/' + str(k)] = Tree.Tree(X, T[Y+'/'+str(i)+'/'+str(j)], T[Z+'/'+str(j+1)+'/'+str(k)])
    printV('T:', [str(t)+':'+str(T[t]) for t in T])
    return T, P

# 1-based indexing: i starts at 0 instead of 1
def subspans(N):
    for length in range(2, N+1):
        for i in range(N+1 - length):
            k = i + length - 1
            for j in range(i, k):
                yield i, j, k

# These two getXXX functions use yield instead of return so that a single pair can be sent back,
# and since that pair is a tuple, Python permits a friendly 'X, p' syntax
# in the calling routine.
def getGrammarLexicalRules(grammar, word):
    for rule in grammar['lexicon']:
        if rule[1] == word:
            yield rule[0], rule[2]

# Input handling unexpected word
def getGrammarUnexpected(grammar, word):
    for rule in grammar['lexicon']:
        if rule[1] == word:
            return False
    return True

# Chomsky Normal Form:  X -> word[p]
#                       X -> Y Z [p] 
# Chomsky Form:     X -> Y [p] 

# ChomskyForm index is 0 for Chomsky Normal Form
#                      1 for Chomsky Form 
# the idex depend on the syntax dictionary of grammar with CNF syntax list at the index 0,
# and C1F syntax list at the index 1
def getGrammarSyntaxRules(grammar, chomskyForm):
    # CNF
    if chomskyForm == 0:
        for rule in grammar['syntax'][chomskyForm]:
            yield rule[0], rule[1], rule[2], rule[3]
    # C1F
    else:
        for rule in grammar['syntax'][chomskyForm]:
            yield rule[0], rule[1], rule[2]


# 'Grammar' here is used to include both the syntax part and the lexicon part.
# Grammar for the chatbot
def getGrammar():
    return {
        'syntax' :
        [
            [
                #['S', 'QPart', 'NP', 0.5], #1.1
                #['S', 'VP', 'NP', 0.5], #2.1
                
                #['QPart', 'WQuestion', 'NP', 0.5], #1.2
                
                
                #['NP', 'Number', 'Adverb', 0.2], # 7 pm
                #['NP', 'Pre', 'AdverbPharse', 0.2], #1.3
                #['NP', 'Preposition', 'NP', 0.2],
                #['NP', 'Article', 'Noun', 0.2], #1.5
                #['NP', 'Adjective', 'Noun', 0.2], # action movie
    
                #['VP', 'Verb', 'Pronoun', 1.0], #2.2
                
                #['AdverbPhrase', 'Verb', 'Preposition', 0.5],
                #['AdverbPhrase', 'Preposition', 'Name', 0.5], #1.6 #2.3
                #['NP', 'NP', 'AdverbPhase', 0.2], #1.4
                ['S', 'QPart', 'NP', 0.5],
                ['QPart', 'WQ', 'VP', 0.5],
                ['WQ', 'WQuestion', 'Preposition', 0.2], #1.3
                ['VP', 'Verb', 'AdverbPhrase', 0.2],
                ['AdverbPhrase', 'AdverbPhrase', 'AdverbPhrase', 0.2],
                ['AdverbPhrase', 'Preposition', 'NP', 0.2],
                ['AdverbPhrase', 'Preposition', 'Noun', 0.2],
                ['NP', 'Article', 'Noun', 0.2],
                
            ],
            [
                #['NP', 'Noun', 1.0], # sushi
                ['Noun', 'Location', 1.0],
                ['Adjective', 'Type', 1.0],
            ]
        ],
        'lexicon' : [
            ['WQuestion', 'where', 1.0],
                            
            ['Verb', 'go', 0.5],
            ['Verb', 'show', 0.5],
            
            ['Pronoun', 'me', 1.0],
            
            ['Noun', 'menu', 0.25],
            ['Noun', 'movie', 0.25],
            ['Noun', 'dinner', 0.25],
            ['Noun', 'sushi', 0.25],
            
            ['Type', 'action', 1.0],
            
            ['Number', '7', 0.5],
            ['Number', '8', 0.5],
            
            ['Location', 'Irvine', 1.0],
            
            ['Article', 'the', 0.5],
            ['Article', 'a', 0.5],
            
            ['Adverb', 'night', 0.33],
            ['Adverb', 'pm', 0.33],
            ['Adverb', 'am', 0.33],
            
            ['Preposition', 'to', 1.0],
            ['Preposition', 'for', 0.5],
            ['Preposition', 'in', 0.5],
         ]
    }

# Unit testing code
if __name__ == '__main__':
    verbose = True
    
    # Movie theater
    #CYKParse(['where', 'to', 'go', 'for', 'a', 'movie', 'in', 'Irvine'], getGrammar())
    CYKParse(['action', 'movie'], getGrammar())
    #CYKParse(['7', 'pm'], getGrammar())
    
    # Restaurant
    #CYKParse(['where', 'to', 'go', 'for', 'a', 'dinner', 'in', 'Irvine'], getGrammar())
    #CYKParse(['sushi'], getGrammar())
    #CYKParse(['show', 'me', 'the', 'menu'], getGrammar())
    
   
