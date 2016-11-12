sample_memo = '''
Milt, we're gonna need to go ahead and move you downstairs into storage B. We have some new people coming in, and we need all the space we can get. So if you could just go ahead and pack up your stuff and move it down there, that would be terrific, OK?
Oh, and remember: next Friday... is Hawaiian shirt day. So, you know, if you want to, go ahead and wear a Hawaiian shirt and jeans.
Oh, oh, and I almost forgot. Ahh, I'm also gonna need you to go ahead and come in on Sunday, too...
Hello Peter, whats happening? Ummm, I'm gonna need you to go ahead and come in tomorrow. So if you could be here around 9 that would be great, mmmk... oh oh! and I almost forgot ahh, I'm also gonna need you to go ahead and come in on Sunday too, kay. We ahh lost some people this week and ah, we sorta need to play catch up.
'''

#
#   Maximum Likelihood Hypothesis
#
#
#   In this quiz we will find the maximum likelihood word based on the preceding word
#
#   Fill in the NextWordProbability procedure so that it takes in sample text and a word,
#   and returns a dictionary with keys the set of words that come after, whose values are
#   the number of times the key comes after that word.
#   
#   Just use .split() to split the sample_memo text into words separated by spaces.

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
        nextWord = wordLIST[ind + 1]
        if not(nextWord in wordDICT.keys()):
            wordDICT[nextWord] = 1
        else:
            wordDICT[nextWord] += 1
    
    return wordDICT
