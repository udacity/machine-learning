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

import re

import sys


def NextWordProbability(sample, word):
    count = {}
    words = sample.split()

    for i, j in enumerate(words):
        if j == word and i < len(words) - 1:
            count[words[i + 1]] = count.get(words[i + 1], 0) + 1
    # if word != "ahead":
    #     print count.values()
    #     sys.exit()
    sum_cnt = float(sum(count.values()))
    for key, value in count.items():
        # if word != "ahead":
        #     print float(sum(count.values()))
        count[key] = value / sum_cnt

    # if word != "ahead":
    #     print word
    #     print count
    #     sys.exit()
    return count


def LaterWordsProbability(sample, prob_dict):
    new_prob = {}
    for k1 in prob_dict.keys():
        # print k1

        temp_prob = NextWordProbability(sample, k1)
        # print temp_prob
        # sys.exit()
        for k2 in temp_prob.keys():
            # print new_prob.get(k2, 0)
            # print prob_dict[k1]
            # print temp_prob[k2]
            # print prob_dict
            # print temp_prob
            # sys.exit()
            new_prob[k2] = new_prob.get(k2, 0) + prob_dict[k1] * temp_prob[k2]
    # print new_prob
    # sys.exit()
    return new_prob


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

    prob = NextWordProbability(sample, word)
    for i in range(0, distance):
        prob = LaterWordsProbability(sample, prob)
    # print "final"
    # print prob
    # sys.exit()
    return max(prob, key=prob.get)


print LaterWords(sample_memo, "ahead", 2)