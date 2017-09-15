# ------------------------------------------------------------------

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

words_to_guess = ["ahead", "could"]
import sys
from collections import Counter
def LaterWords(sample, word, distance):
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
    probabilities = NextWordProbabilities(sample, word)
    print probabilities
    sys.exit()
    for i in range(0, distance):
        probabilities = LaterWordsProbabilities(sample, probabilities)

    return max(probabilities, key=probabilities.get)



def LaterWordsProbabilities(sample, probabilities):
    new_probabilities = {}
    for p1 in probabilities.keys():
        tmp_probabilities = NextWordProbabilities(sample, p1)
        for p2 in tmp_probabilities.keys():
            new_probabilities[p2] = new_probabilities.get(p2, 0) + probabilities[p1] * tmp_probabilities[p2]

    return new_probabilities

def NextWordFrequencies(sampletext, word):
    text_words = sampletext.split()
    next_words = list()
    for key, text_word in enumerate(text_words):
        if text_word == word and key + 1 < len(text_words):
            next_words.append(text_words[key + 1])
    # if word != "ahead":
    #    print dict(Counter(next_words))
    return dict(Counter(next_words))

def SumFrequencies(frequencies):
    sum_of_frequencies = 0
    for word, frequency  in frequencies.iteritems():
        sum_of_frequencies += frequency
    return sum_of_frequencies

def NextWordProbabilities(sampletext, word):
    frequencies = NextWordFrequencies(sampletext, word)

    sum_of_frequencies = 0
    probabilities = {}
    sum_of_frequencies = SumFrequencies(frequencies)
    for following_word, frequency in frequencies.iteritems():
        probabilities[following_word] =  frequency / float(sum_of_frequencies)
    return probabilities

print LaterWords(sample_memo, "ahead", 2)