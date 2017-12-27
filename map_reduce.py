from mrjob.job import MRJob
from mrjob.step import MRStep
import re

# regular expression that used to process the words (all the words in general)
WORD_RE = re.compile(r"[\w']+")


class MRMostUsedWord(MRJob):
    # defining the steps of MRjob class by overriding the method.
    # different mappers and combiners can be defined.
    # we will be using mapper, combiner and 2 reducer (intermediate and final)
    def steps(self):
        return [
            MRStep(mapper=self.mapper_get_words,
                   combiner=self.combiner_count_words,
                   reducer=self.reducer_count_words),
            MRStep(reducer=self.reducer_find_max_10_word)
        ]

    def mapper_get_words(self, _, line):
        # yield each word in the line with 1 value
        for word in WORD_RE.findall(line):
            yield (word.lower(), 1)

    def combiner_count_words(self, word, counts):
        # counts the 1's of each word, and send them to the same reduce
        yield (word, sum(counts))

    def reducer_count_words(self, word, counts):
        # gets the (word,counts) pair from the combiner
        # sum all the counts for the same word and make a new pair for the value (num_occurrences,word)
        # send all (num_occurrences, word) pairs to the same reducer.
        # we ignore the key for the final pairs as it is stored in the value, that will make it easier to process them further
        yield None, (sum(counts), word)

    # discard the key; it is just None
    def reducer_find_max_10_word(self, _, word_count_pairs):
        # each item of word_count_pairs is (num_occurrences, word).
        # we create a list of all pairs
        # descending sort for the list
        # return the most 10 occurred words (first 10 in the list)
        top10 = list(word_count_pairs)
        top10.sort(reverse=True)
        for i in range(10):
            yield top10[i]


if __name__ == '__main__':
    MRMostUsedWord.run()