import operator

# SIMPLE BAG OF WORDS FUNCTION
def count_words(s, n):
    """Return the n most frequently occuring words in s."""

    list_of_words = s.split()
    words_dict = {}

    # TODO: Count the number of occurences of each word in s
    for word in list_of_words:
        if (word in words_dict):
            words_dict[word] = words_dict[word] + 1
        else:
            words_dict[word] = 1

    # TODO: Sort the occurences in descending order (alphabetically in case of ties)

    # first sort the dictionary alphabetically
    sorted1 = sorted(words_dict.items(), key=operator.itemgetter(0))

    # sort the list of tuples in descending order of values
    words_counter_list = sorted(sorted1, key=lambda tup: tup[1], reverse=True)

    # TODO: Return the top n words as a list of tuples (<word>, <count>)
    return words_counter_list[0:n]


def test_run():
    """Test count_words() with some inputs."""
    print count_words("OFFER IS SECRET CLICK SECRET LINK SECRET SPORTS LINK PLAY SPORTS TODAY WENT PLAY SPORTS SECRET SPORTS EVENT "
                      "SPORTS IS TODAY SPORTS COSTS MONEY", 100)
    #print count_words("cat bat mat cat bat maa cat mab", 3)
    #print count_words("betty bought a bit of butter but the butter was bitter", 3)


if __name__ == '__main__':
    test_run()
