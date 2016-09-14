#------------------------------------------------------------------

#
#   Bayes Optimal Classifier
#
#   In this quiz we will compute the optimal label for a second missing word in a row
#   based on the possible words that could be in the first blank
#
#   Finish the procedurce, LaterWords(), below
#
#   You may want to import your code from the previous programming exercise!
#

sample_memo = '''
Milt, we're gonna need to go ahead and move you downstairs into storage B. We have some new people coming in, and we need all the space we can get. So if you could just go ahead and pack up your stuff and move it down there, that would be terrific, OK?
Oh, and remember: next Friday... is Hawaiian shirt day. So, you know, if you want to, go ahead and wear a Hawaiian shirt and jeans.
Oh, oh, and I almost forgot. Ahh, I'm also gonna need you to go ahead and come in on Sunday, too...
Hello Peter, whats happening? Ummm, I'm gonna need you to go ahead and come in tomorrow. So if you could be here around 9 that would be great, mmmk... oh oh! and I almost forgot ahh, I'm also gonna need you to go ahead and come in on Sunday too, kay. We ahh lost some people this week and ah, we sorta need to play catch up.
'''

corrupted_memo = '''
Yeah, I'm gonna --- you to go ahead --- --- complain about this. Oh, and if you could --- --- and sit at the kids' table, that'd be --- 
'''

data_list = sample_memo.strip().split()

words_to_guess = ["ahead","could"]

def NextWordProbability(sampletext,word):
    # Modules import
    import string
    
    # Preprocessing
    wordLIST = sampletext.split()
    wordLIST = [ii.strip("\n") for ii in wordLIST]
    for jj in string.punctuation:
        wordLIST = [ii.strip(jj) for ii in wordLIST]
    
    # Find words
    occurLIST = [ind for (ii, ind) in zip(wordLIST, range(0, len(wordLIST))) if ii==word]    
    wordDICT = {}
    for ind in occurLIST:
        if (ind + 1 < len(wordLIST)):
            nextWord = wordLIST[ind + 1]
        else:
            nextWord = '.'
        if not(nextWord in wordDICT.keys()):
            wordDICT[nextWord] = 1
        else:
            wordDICT[nextWord] += 1
            
    # Calculate Cond Prob(New; different from previous version)
    wordCount = sum([wordDICT[ii] for ii in wordDICT.keys()])
    ansDICT = {ii: float(wordDICT[ii]) / wordCount for ii in wordDICT.keys()}
    
    return ansDICT

def LaterWords(sample,word,distance):
    '''@param sample: a sample of text to draw from
    @param word: a word occuring before a corrupted sequence
    @param distance: how many words later to estimate (i.e. 1 for the next word, 2 for the word after that)
    @returns: a single word which is the most likely possibility
    '''
    
    # TODO: Given a word, collect the relative probabilities of possible following words
    # from @sample. You may want to import your code from the maximum likelihood exercise.
    
    # TODO: Repeat the above process--for each distance beyond 1, evaluate the words that
    # might come after each word, and combine them weighting by relative probability
    # into an estimate of what might appear next.

    level = []
    level.append({word:{'ProbAll':1.0, 'NextProb':NextWordProbability(sample, word)}})
    
    # 1.0: Create Bayes Net(Tree)
    for l in range(0, distance):
        level.append({})    # Add an empty dictionary for next layer
        for node in level[l].keys():
            for nodeChild in level[l][node]['NextProb'].keys():
                if not(nodeChild in level[l + 1].keys()):
                    level[l + 1][nodeChild] = {'ProbAll': 0.0, 'NextProb':NextWordProbability(sample, nodeChild)}

    # 2.0: Calculate Prob for each word in each level
    for l in range(0, distance):
        for dad in level[l].keys():
            for child in level[l + 1].keys():
                if child in level[l][dad]['NextProb'].keys():
                    level[l + 1][child][dad] = level[l][dad]['NextProb'][child] * level[l][dad]['ProbAll']

        for child in level[l + 1].keys():
            level[l + 1][child]['ProbAll'] = sum([level[l + 1][child][dad] for dad in level[l + 1][child].keys() if not('ProbAll' == dad or 'NextProb' == dad)])
    
    # 3.0: Select the word of the largest prob and output
    maxP = 0.0
    wordP = word
    for i in level[distance].keys():
        if (maxP < level[distance][i]['ProbAll']):
            maxP = level[distance][i]['ProbAll']
            wordP = i
    return wordP
