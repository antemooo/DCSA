from nltk.tokenize import TweetTokenizer
import re
from string import punctuation
from nltk.corpus import stopwords

'''This script is a helper script used to clean TwitterData'''


'''
Tokenize_Tweet method is a method that is casting TweetTokenizer package to tokenize tweets
Takes a string tweet sentance
removes all users name and links
splits the sentance into a list of words and punctuation
returns the list
'''
def tokenize_tweet(tweet):
    tknzr = TweetTokenizer(reduce_len=True,strip_handles=True)
    return tknzr.tokenize(tweet)

'''
Helper method to remoce URLs using regular expressions.
It is aware of http/https.
Takes a string tweet sentance
return string tweet without URLs
'''
def remove_urls(tweet):
    return re.sub(r'(https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%)*\b', '', tweet, flags=re.MULTILINE)

'''
remove_stop_words_and_punctuation method.
Takes a list of splitted tweet words.
Rempves the punctuation as specified in String class.
Removes all words contains digits through isAlpha method.
remove all stop words defined in NLTK.CORPUS stopwords.
Returns a new list of clean tweets.

NOTE: it is better to use this method on the output of (tokenize_tweet) method
'''
def remove_stop_words_and_punctuation(tweet):
    translator = str.maketrans('', '', punctuation)
    english_stopwords = stopwords.words('english')
    return [word.translate(translator) for word in tweet
            if word.isalpha()
            and word.lower() not in english_stopwords
            and word.translate(translator) != '']